import requests
import streamlit as st

from frontend.services import api_client


def _show_backend_error(exc: Exception) -> None:
    if isinstance(exc, requests.ConnectionError):
        st.error("Could not reach the backend. Is it running on port 8000?")
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        st.error(
            f"Backend returned {exc.response.status_code}: "
            f"{exc.response.text}"
        )
    else:
        st.error(f"Unexpected error: {exc}")


def render() -> None:

    # ==========================================
    # HISTORY PAGE CSS
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

        .history-subtitle {
            color: darkgrey;
            font-size: 1.05rem;
            margin-bottom: 25px;
        }


        /* ==========================================
           ANALYSIS COUNT
           ========================================== */

        .history-count {
            color: #DAA464;
            font-size: 1rem;
            font-weight: 600;
        }


        /* ==========================================
           EXPANDER / HISTORY BOX
           ========================================== */

        div[data-testid="stExpander"] {
            background-color: #0F1C3F !important;

            border: 1px solid #16295C !important;

            border-radius: 16px !important;

            margin-bottom: 18px !important;

            box-shadow:
                0 5px 15px rgba(0, 0, 0, 0.25) !important;

            overflow: hidden !important;
        }


        /* Expander header */

        div[data-testid="stExpander"] summary {
            background-color: #0F1C3F !important;

            color: #DAA464 !important;

            border-radius: 16px !important;
        }


        /* Expander header text */

        div[data-testid="stExpander"] summary p {
            color: #DAA464 !important;

            font-weight: 600 !important;
        }


        /* Expander content */

        div[data-testid="stExpander"] details {
            background-color: #0F1C3F !important;
        }


        /* ==========================================
           METRIC BOXES
           ========================================== */

        div[data-testid="stMetric"] {
            background-color: #060D1F !important;

            border: 1px solid #16295C !important;

            border-radius: 12px !important;

            padding: 15px !important;

            box-shadow:
                0 4px 12px rgba(0, 0, 0, 0.20) !important;
        }


        /* Metric label */

        div[data-testid="stMetric"] label {
            color: darkgrey !important;
        }


        /* Metric value */

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            color: #DAA464 !important;
        }


        /* Metric delta */

        div[data-testid="stMetric"] [data-testid="stMetricDelta"] {
            color: darkgrey !important;
        }


        /* ==========================================
           JD MATCH
           ========================================== */

        .jd-match {
            background-color: #060D1F;

            border: 1px solid #16295C;

            border-radius: 12px;

            padding: 15px 18px;

            margin-top: 20px;

            margin-bottom: 15px;

            color: #DAA464;

            font-weight: 600;
        }


        /* ==========================================
           DELETE BUTTON
           ========================================== */

        .stButton > button {
            background-color: #0F1C3F !important;

            color: #DAA464 !important;

            border: 1px solid #16295C !important;

            border-radius: 10px !important;
        }

        .stButton > button:hover {
            background-color: #16295C !important;

            color: #DAA464 !important;

            border-color: #DAA464 !important;
        }


        /* ==========================================
           DIVIDER
           ========================================== */

        hr {
            border-color: #16295C !important;
        }


        /* ==========================================
           WARNING / INFO BOX
           ========================================== */

        div[data-testid="stAlert"] {
            background-color: #0F1C3F !important;

            border: 1px solid #16295C !important;

            color: darkgrey !important;

            border-radius: 12px !important;
        }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.title("📊 Analysis History")

    st.markdown(
        '<div class="history-subtitle">'
        'Past analyses saved against your account.'
        '</div>',
        unsafe_allow_html=True
    )


    # ==========================================
    # AUTHENTICATION
    # ==========================================

    access_token = st.session_state.get("access_token")

    if not access_token:
        st.warning(
            "⚠️ Sign in from the sidebar to view your history."
        )
        return


    # ==========================================
    # GET HISTORY
    # ==========================================

    try:
        history = api_client.get_history(access_token)

    except requests.RequestException as exc:
        _show_backend_error(exc)
        return


    # ==========================================
    # EMPTY HISTORY
    # ==========================================

    if not history:

        st.info(
            "No analyses yet for this account. "
            "Run a scoring on the ATS Scorer page first."
        )

        if st.button("🎯 Go to ATS Scorer"):

            st.session_state.current_view = "scorer"

            st.rerun()

        return


    # ==========================================
    # TOTAL ANALYSES
    # ==========================================

    st.markdown(
        f'<div class="history-count">'
        f'Total analyses: {len(history)}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")


    # ==========================================
    # HISTORY ENTRIES
    # ==========================================

    for idx, entry in enumerate(history):

        filename = entry.get("filename", "resume")

        ats_score = float(
            entry.get("ats_score", 0)
        )

        created_at = entry.get(
            "created_at",
            ""
        )

        analysis = (
            entry.get("analysis_result", {})
            or {}
        )

        component_scores = (
            analysis.get("component_scores", {})
            or {}
        )

        jd_comparison = (
            analysis.get("jd_comparison")
            or analysis.get("jd_match_analysis")
        )


        # ==========================================
        # HISTORY CARD
        # ==========================================

        with st.expander(
            f"📄 {filename} — "
            f"Score: {ats_score:.0f}/100 — "
            f"{created_at}"
        ):

            # ==========================================
            # SCORE METRICS
            # ==========================================

            c1, c2, c3 = st.columns(3)


            with c1:

                st.metric(
                    "Overall",
                    f"{ats_score:.0f}/100"
                )

                st.metric(
                    "Formatting",
                    f"{component_scores.get('formatting', 0):.0f}/20"
                )


            with c2:

                st.metric(
                    "Keywords",
                    f"{component_scores.get('keywords', 0):.0f}/25"
                )

                st.metric(
                    "Content",
                    f"{component_scores.get('content', 0):.0f}/25"
                )


            with c3:

                st.metric(
                    "Skill Validation",
                    f"{component_scores.get('skill_validation', 0):.0f}/15"
                )

                st.metric(
                    "ATS Compatibility",
                    f"{component_scores.get('ats_compatibility', 0):.0f}/15"
                )


            # ==========================================
            # JD MATCH
            # ==========================================

            if jd_comparison:

                st.markdown(
                    f"""
                    <div class="jd-match">
                        🎯 JD Match:
                        {jd_comparison.get('match_percentage', 0):.0f}%
                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # ==========================================
            # DELETE
            # ==========================================

            entry_id = entry.get("id")

            if entry_id:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{idx}"
                ):

                    try:

                        api_client.delete_history_entry(
                            str(entry_id),
                            access_token
                        )

                        st.success("Deleted.")

                        st.rerun()

                    except requests.RequestException as exc:

                        _show_backend_error(exc)