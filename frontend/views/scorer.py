from typing import Optional

import requests
import streamlit as st

from frontend.services import api_client
from frontend.components.dashboard import display_results_dashboard


def _read_jd(jd_file, jd_text: str) -> str:
    """
    Turn whatever the user provided into a plain JD string for the backend.

    For .txt files we decode in-process — that's a trivial operation, no need
    for a backend round-trip. For PDF/DOCX, we'd need the backend's parser;
    we don't have a public endpoint for that, so we ask the user to paste text
    instead for non-txt JDs.
    """
    if jd_text:
        return jd_text.strip()

    if jd_file is None:
        return ""

    if jd_file.name.lower().endswith(".txt"):
        return jd_file.getvalue().decode(
            "utf-8",
            errors="ignore"
        )

    st.warning(
        "Job description files must be `.txt` for now — paste the JD text instead "
        "if you have a PDF or DOCX."
    )

    return ""


def _show_backend_error(exc: Exception) -> None:
    """Translate a `requests` exception into a friendly Streamlit error."""

    if isinstance(exc, requests.ConnectionError):

        st.error(
            "Could not reach the backend. Is "
            "`uvicorn backend.main:app` running on port 8000?"
        )

    elif isinstance(exc, requests.Timeout):

        st.error(
            "The backend took too long to respond. "
            "Try a smaller resume or check the server logs."
        )

    elif isinstance(exc, requests.HTTPError) and exc.response is not None:

        try:
            detail = exc.response.json().get(
                "detail",
                exc.response.text
            )

        except ValueError:
            detail = exc.response.text

        st.error(
            f"Backend returned "
            f"{exc.response.status_code}: {detail}"
        )

    else:

        st.error(
            f"Unexpected error: {exc}"
        )


def _summary_text(analysis: dict) -> str:
    """Tiny client-side text summary for the Download button."""

    score = analysis.get(
        "ATS_score",
        analysis.get("ats_score", 0)
    )

    lines = [
        f"ATS Score: {score:.0f}/100",
        ""
    ]

    if analysis.get("strengths"):

        lines.append("STRENGTHS:")

        lines.extend(
            f"  - {s}"
            for s in analysis["strengths"]
        )

        lines.append("")

    if analysis.get("critical_issues"):

        lines.append("CRITICAL ISSUES:")

        lines.extend(
            f"  - {s}"
            for s in analysis["critical_issues"]
        )

        lines.append("")

    if analysis.get("suggestions"):

        lines.append("SUGGESTIONS:")

        lines.extend(
            f"  - {s}"
            for s in analysis["suggestions"]
        )

    return "\n".join(lines)


def _render_upload_area(analysis_mode: str):
    """Two-column upload widgets. Returns (resume_file, jd_file, jd_text)."""

    left, right = st.columns(2)


    # ==========================================
    # RESUME UPLOAD
    # ==========================================

    with left:

        st.markdown("### 📄 Upload Resume")

        resume_file = st.file_uploader(
            "Choose your resume file",
            type=["pdf", "doc", "docx"],
            help="Supported: PDF, DOC, DOCX (max 5 MB)",
            key="resume_upload",
        )

        if resume_file:

            st.success(
                f"✅ {resume_file.name} "
                f"({resume_file.size / 1024:.1f} KB)"
            )


    jd_file: Optional[object] = None
    jd_text = ""


    # ==========================================
    # JOB DESCRIPTION
    # ==========================================

    with right:

        if analysis_mode == "Job Description Comparison":

            st.markdown("### 📋 Job Description")

            jd_method = st.radio(
                "Input method:",
                ["Paste Text", "Upload .txt File"],
                horizontal=True,
                key="jd_input_method",
            )

            if jd_method == "Upload .txt File":

                jd_file = st.file_uploader(
                    "Choose JD file (.txt only)",
                    type=["txt"],
                    key="jd_upload",
                )

                if jd_file:

                    st.success(
                        f"✅ {jd_file.name}"
                    )

            else:

                jd_text = st.text_area(
                    "Paste job description text:",
                    height=200,
                    placeholder="Paste the JD here...",
                    key="jd_text",
                )

                if jd_text:

                    st.success(
                        f"✅ {len(jd_text)} characters"
                    )

        else:

            st.markdown("### 📋 Job Description")

            st.info(
                "Switch to 'Job Description Comparison' mode "
                "to enable JD matching."
            )


    return resume_file, jd_file, jd_text


def _render_export_buttons(analysis: dict) -> None:

    st.markdown("### 📥 Export Results")

    c1, c2 = st.columns(2)


    # ==========================================
    # PDF EXPORT
    # ==========================================

    with c1:

        # Lazy: only call the backend the first time
        # the user clicks expand.

        if st.button(
            "📑 Generate PDF Report",
            use_container_width=True,
            type="primary"
        ):

            try:

                with st.spinner(
                    "Generating PDF on backend..."
                ):

                    pdf_bytes = api_client.generate_pdf(
                        analysis,
                        access_token=st.session_state["access_token"],
                    )

                st.session_state["scorer_pdf_bytes"] = pdf_bytes

            except requests.RequestException as exc:

                _show_backend_error(exc)


        if "scorer_pdf_bytes" in st.session_state:

            st.download_button(
                "⬇️ Download PDF",
                data=st.session_state["scorer_pdf_bytes"],
                file_name="ats_resume_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="download_pdf_report",
            )


    # ==========================================
    # TEXT SUMMARY
    # ==========================================

    with c2:

        st.download_button(
            "📄 Download Summary (.txt)",
            data=_summary_text(analysis),
            file_name="ats_summary.txt",
            mime="text/plain",
            use_container_width=True,
            key="download_summary",
        )


def render() -> None:


    # ==========================================
    # ATS SCORER PAGE CSS
    # ==========================================

    st.markdown("""
    <style>

        /* ==========================================
           MAIN APP BACKGROUND
           ========================================== */

        .stApp {
            background-color: #060D1F;
        }

        [data-testid="stAppViewContainer"] {
            background-color: #060D1F;
        }

        [data-testid="stHeader"] {
            background-color: #060D1F;
        }


        /* ==========================================
           PAGE TITLE
           ========================================== */

        h1 {
            color: #DAA464 !important;
        }


        /* ==========================================
           GENERAL TEXT
           ========================================== */

        p {
            color: darkgrey;
        }


        /* ==========================================
           HEADINGS
           ========================================== */

        h2,
        h3 {
            color: #DAA464 !important;
        }


        /* ==========================================
           DIVIDERS
           ========================================== */

        hr {
            border-color: #16295C !important;
        }


        /* ==========================================
           ANALYSIS MODE BOX
           ========================================== */

        div[data-testid="stRadio"] {

            background-color: #0F1C3F !important;

            border: 1px solid #16295C !important;

            border-radius: 14px !important;

            padding: 15px 20px !important;

            margin: 10px 0 !important;

            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.20);
        }


        /* Radio labels */

        div[data-testid="stRadio"] label {
            color: darkgrey !important;
        }


        /* Radio text */

        div[data-testid="stRadio"] p {
            color: darkgrey !important;
        }


        /* ==========================================
           FILE UPLOADER
           ========================================== */

        div[data-testid="stFileUploader"] {

            background-color: #0F1C3F !important;

            border: 1px solid #16295C !important;

            border-radius: 14px !important;

            padding: 18px !important;

            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.20);
        }


        /* File uploader text */

        div[data-testid="stFileUploader"] label {
            color: darkgrey !important;
        }


        div[data-testid="stFileUploader"] p {
            color: darkgrey !important;
        }


        /* ==========================================
           TEXT AREA
           ========================================== */

        textarea {

            background-color: #060D1F !important;

            color: darkgrey !important;

            border: 1px solid #16295C !important;

            border-radius: 10px !important;
        }


        textarea:focus {

            border-color: #DAA464 !important;

            box-shadow:
                0 0 8px rgba(218, 164, 100, 0.15) !important;
        }


        /* ==========================================
           INPUT LABELS
           ========================================== */

        label {
            color: darkgrey !important;
        }


        /* ==========================================
           INFO / SUCCESS / WARNING BOXES
           ========================================== */

        div[data-testid="stAlert"] {

            background-color: #0F1C3F !important;

            border: 1px solid #16295C !important;

            border-radius: 12px !important;

            color: darkgrey !important;
        }


        div[data-testid="stAlert"] p {
            color: darkgrey !important;
        }


        /* ==========================================
           SUCCESS TEXT
           ========================================== */

        div[data-testid="stAlert"] strong {
            color: #DAA464 !important;
        }


        /* ==========================================
           PRIMARY BUTTONS
           ========================================== */

        .stButton > button[kind="primary"] {

            background-color: #0F1C3F !important;

            color: #DAA464 !important;

            border: 1px solid #16295C !important;

            border-radius: 10px !important;

            font-weight: 600 !important;

            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.20);
        }


        .stButton > button[kind="primary"]:hover {

            background-color: #16295C !important;

            color: #DAA464 !important;

            border-color: #DAA464 !important;
        }


        /* Force primary button text */

        .stButton > button[kind="primary"] p,
        .stButton > button[kind="primary"] span {

            color: #DAA464 !important;

            -webkit-text-fill-color: #DAA464 !important;
        }


        /* ==========================================
           DOWNLOAD BUTTONS
           ========================================== */

        .stDownloadButton > button {

            background-color: #0F1C3F !important;

            color: #DAA464 !important;

            border: 1px solid #16295C !important;

            border-radius: 10px !important;

            font-weight: 600 !important;

            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.20);
        }


        .stDownloadButton > button:hover {

            background-color: #16295C !important;

            color: #DAA464 !important;

            border-color: #DAA464 !important;
        }


        /* Download button text */

        .stDownloadButton > button p,
        .stDownloadButton > button span {

            color: #DAA464 !important;

            -webkit-text-fill-color: #DAA464 !important;
        }


        /* ==========================================
           SIDEBAR
           ========================================== */

        [data-testid="stSidebar"] {

            background-color: #060D1F !important;

            border-right: 1px solid #16295C;
        }


        [data-testid="stSidebar"] h2 {

            color: #DAA464 !important;
        }


        [data-testid="stSidebar"] p {

            color: darkgrey !important;
        }


        /* ==========================================
           SPINNER
           ========================================== */

        div[data-testid="stSpinner"] {

            color: #DAA464 !important;
        }


        /* ==========================================
           CODE
           ========================================== */

        code {

            background-color: #060D1F !important;

            color: #DAA464 !important;
        }


        /* ==========================================
           FILE UPLOAD SUCCESS
           ========================================== */

        div[data-testid="stFileUploaderFile"] {

            background-color: #060D1F !important;

            border: 1px solid #16295C !important;

            border-radius: 10px !important;
        }


        /* ==========================================
           FILE NAME
           ========================================== */

        div[data-testid="stFileUploaderFile"] span {

            color: #DAA464 !important;
        }


        /* ==========================================
           RADIO CIRCLE
           ========================================== */

        div[data-testid="stRadio"] input:checked + div {

            border-color: #DAA464 !important;
        }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # PAGE TITLE
    # ==========================================

    st.title("📄 ATS Resume Scorer")

    st.markdown(
        "Upload your resume — and optionally a job description — "
        "for a comprehensive analysis."
    )


    # ==========================================
    # SIDEBAR
    # ==========================================

    with st.sidebar:

        st.markdown("---")

        st.markdown("## 📊 Analysis Options")

        st.info(
            "**General ATS Score**: resume only — overall compatibility.\n\n"
            "**JD Comparison**: resume + job description — targeted match analysis."
        )


    # ==========================================
    # SEPARATOR
    # ==========================================

    st.markdown("---")


    # ==========================================
    # ANALYSIS MODE
    # ==========================================

    analysis_mode = st.radio(
        "Select Analysis Mode:",
        [
            "General ATS Score",
            "Job Description Comparison"
        ],
        horizontal=True,
    )


    # ==========================================
    # SEPARATOR
    # ==========================================

    st.markdown("---")


    # ==========================================
    # UPLOAD AREA
    # ==========================================

    resume_file, jd_file, jd_text = _render_upload_area(
        analysis_mode
    )


    # ==========================================
    # SEPARATOR
    # ==========================================

    st.markdown("---")


    # ==========================================
    # NO RESUME
    # ==========================================

    if not resume_file:

        st.info(
            "👆 Upload your resume to begin."
        )

        # If we have a prior result in session,
        # render it again.

        if st.session_state.get("scorer_analysis"):

            display_results_dashboard(
                st.session_state["scorer_analysis"]
            )

        return


    # ==========================================
    # ACCESS TOKEN
    # ==========================================

    access_token = st.session_state.get(
        "access_token"
    )

    if not access_token:

        st.warning(
            "⚠️ Sign in from the sidebar to analyze a resume."
        )

        return


    # ==========================================
    # ANALYZE BUTTON
    # ==========================================

    _, mid, _ = st.columns([1, 2, 1])

    with mid:

        analyze = st.button(
            "🚀 Analyze Resume",
            use_container_width=True,
            type="primary"
        )


    # ==========================================
    # WAIT FOR ANALYSIS
    # ==========================================

    if not analyze:

        # Re-show previous result on rerun
        # (e.g. after PDF generation).

        if st.session_state.get("scorer_analysis"):

            display_results_dashboard(
                st.session_state["scorer_analysis"]
            )

            _render_export_buttons(
                st.session_state["scorer_analysis"]
            )

        return


    # ==========================================
    # FRESH ANALYSIS
    # ==========================================

    st.session_state.pop(
        "scorer_pdf_bytes",
        None
    )

    st.session_state.pop(
        "scorer_analysis",
        None
    )


    # ==========================================
    # JOB DESCRIPTION
    # ==========================================

    job_description = (
        _read_jd(jd_file, jd_text)
        if analysis_mode == "Job Description Comparison"
        else ""
    )


    # ==========================================
    # ANALYZE RESUME
    # ==========================================

    try:

        with st.spinner(
            "Analyzing your resume... "
            "this can take 10–30 seconds."
        ):

            analysis = api_client.analyze_resume(
                resume_file=resume_file,
                access_token=access_token,
                job_description=job_description,
            )

    except requests.RequestException as exc:

        _show_backend_error(exc)

        return


    # ==========================================
    # SAVE RESULT
    # ==========================================

    st.session_state["scorer_analysis"] = analysis


    # ==========================================
    # SUCCESS
    # ==========================================

    st.success(
        "✅ Analysis complete!"
    )


    # ==========================================
    # DISPLAY RESULTS
    # ==========================================

    display_results_dashboard(
        analysis
    )


    # ==========================================
    # EXPORT RESULTS
    # ==========================================

    _render_export_buttons(
        analysis
    )