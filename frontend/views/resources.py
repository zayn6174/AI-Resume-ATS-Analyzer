import streamlit as st


def render():
    """Render the resources page"""

    # ==========================================
    # RESOURCE PAGE CSS
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
           PAGE HEADER
           ========================================== */

        .resource-header {
            text-align: center;
            padding: 2.5rem 2rem;
            background: linear-gradient(
                135deg,
                #0F1C3F 0%,
                #16295C 50%,
                #10B981 100%
            );
            color: darkgrey;
            border-radius: 16px;
            margin-bottom: 2rem;
            box-shadow: 0 10px 40px rgba(15, 28, 63, 0.3);
        }

        .resource-header h1 {
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: #DAA464;
        }

        .resource-header p {
            color: darkgrey;
            font-size: 1.1rem;
        }


        /* ==========================================
           RESOURCE SECTION
           ========================================== */

        .resource-section {
            background: #0F1C3F;
            padding: 40px;
            border-radius: 20px;
            margin: 30px 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.25);
            border: 1px solid #16295C;
        }


        /* ==========================================
           SECTION TITLE
           ========================================== */

        .resource-title {
            text-align: center;
            color: #DAA464;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 30px;
        }


        /* ==========================================
           RESOURCE CARDS
           ========================================== */

        .resource-container {
            display: flex;
            gap: 25px;
            align-items: stretch;
        }

        .resource-card {
            flex: 1;
            width: 100%;
            min-height: 300px;
            box-sizing: border-box;

            background: #060D1F;
            padding: 28px;
            border-radius: 16px;

            border: 1px solid #16295C;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.25);

            overflow: hidden;
        }

        .resource-card h3 {
            color: #DAA464;
            font-size: 1.4rem;
            margin-top: 0;
            margin-bottom: 18px;
        }

        .resource-card p {
            color: darkgrey;
            line-height: 1.7;
            font-size: 1rem;
        }

        .resource-card li {
            color: darkgrey;
            margin-bottom: 10px;
            line-height: 1.5;
        }

        .resource-card strong {
            color: #DAA464;
        }


        /* ==========================================
           INDUSTRY TAB BUTTONS
           ========================================== */

        .industry-tab-button .stButton > button {
            width: 100%;
            height: 52px;

            background-color: #0F1C3F !important;
            color: #DAA464 !important;

            border: 1px solid #16295C !important;
            border-radius: 10px !important;

            font-size: 1rem !important;
            font-weight: 600 !important;

            box-shadow: none !important;
        }

        .industry-tab-button .stButton > button:hover {
            background-color: #16295C !important;
            color: #DAA464 !important;
            border-color: #DAA464 !important;
        }

        .industry-tab-button .stButton > button p {
            color: #DAA464 !important;
        }


        /* ==========================================
           SELECTED INDUSTRY TAB
           ========================================== */

        .industry-tab-selected .stButton > button {
            background-color: #16295C !important;
            color: #DAA464 !important;

            border: 1px solid #DAA464 !important;
            border-radius: 10px !important;

            font-size: 1rem !important;
            font-weight: 700 !important;

            box-shadow: 0 0 12px rgba(218, 164, 100, 0.15) !important;
        }

        .industry-tab-selected .stButton > button:hover {
            background-color: #16295C !important;
            color: #DAA464 !important;
        }

        .industry-tab-selected .stButton > button p {
            color: #DAA464 !important;
        }


        /* ==========================================
           TAB CONTENT
           ========================================== */

        .industry-content {
            margin-top: 25px;
        }


        /* ==========================================
           TEMPLATE CARD
           ========================================== */

        .template-card {
            background: #060D1F;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #16295C;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.25);
            text-align: center;
        }

        .template-card h3 {
            color: #DAA464;
            margin-bottom: 15px;
        }

        .template-card p {
            color: darkgrey;
            line-height: 1.7;
        }


        /* ==========================================
           DIVIDER
           ========================================== */

        hr {
            border-color: #16295C !important;
        }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # PAGE HEADER
    # ==========================================

    st.markdown("""
    <div class="resource-header">

    <h1>📚 Resources & Tips</h1>

     <p>
            Learn how to optimize your resume for ATS systems
    </p>

    </div>
    """, unsafe_allow_html=True)


    # ==========================================
    # ATS OPTIMIZATION TIPS
    # ==========================================

    st.html("""
<div class="resource-section">

    <div class="resource-title">
        📄 ATS Optimization Tips
    </div>

    <div class="resource-container">

        <div class="resource-card">

            <h3>✅ Do's</h3>

            <ul>
                <li>Use standard section headings</li>
                <li>Include relevant keywords from job description</li>
                <li>Use simple, clean formatting</li>
                <li>List skills explicitly</li>
                <li>Quantify achievements with numbers</li>
                <li>Use standard fonts (Arial, Calibri, Times New Roman)</li>
                <li>Save as PDF or DOCX</li>
            </ul>

        </div>


        <div class="resource-card">

            <h3>❌ Don'ts</h3>

            <ul>
                <li>Avoid tables and text boxes</li>
                <li>Don't use headers/footers for important info</li>
                <li>Avoid images and graphics</li>
                <li>Don't use unusual fonts</li>
                <li>Avoid columns (use single column layout)</li>
                <li>Don't keyword stuff</li>
                <li>Avoid abbreviations without spelling out first</li>
            </ul>

        </div>

    </div>

</div>
""")


    # ==========================================
    # SEPARATOR
    # ==========================================

    st.markdown("---")


    # ==========================================
    # COMMON ATS KEYWORDS
    # ==========================================

    st.html("""
<div class="resource-section">

    <div class="resource-title">
        🔑 Common ATS Keywords by Industry
    </div>

</div>
""")


    # ==========================================
    # INDUSTRY SELECTION
    # ==========================================

    if "selected_industry" not in st.session_state:
        st.session_state.selected_industry = "Tech"


    # ==========================================
    # INDUSTRY BUTTONS
    # ==========================================

    tab1, tab2, tab3 = st.columns(3)


    with tab1:

        if st.session_state.selected_industry == "Tech":

            st.markdown(
                '<div class="industry-tab-selected">',
                unsafe_allow_html=True
            )

            if st.button(
                "💻 Tech ✓",
                use_container_width=True,
                key="tech_button"
            ):
                st.session_state.selected_industry = "Tech"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.markdown(
                '<div class="industry-tab-button">',
                unsafe_allow_html=True
            )

            if st.button(
                "💻 Tech",
                use_container_width=True,
                key="tech_button"
            ):
                st.session_state.selected_industry = "Tech"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


    with tab2:

        if st.session_state.selected_industry == "Business":

            st.markdown(
                '<div class="industry-tab-selected">',
                unsafe_allow_html=True
            )

            if st.button(
                "💼 Business ✓",
                use_container_width=True,
                key="business_button"
            ):
                st.session_state.selected_industry = "Business"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.markdown(
                '<div class="industry-tab-button">',
                unsafe_allow_html=True
            )

            if st.button(
                "💼 Business",
                use_container_width=True,
                key="business_button"
            ):
                st.session_state.selected_industry = "Business"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


    with tab3:

        if st.session_state.selected_industry == "Creative":

            st.markdown(
                '<div class="industry-tab-selected">',
                unsafe_allow_html=True
            )

            if st.button(
                "🎨 Creative ✓",
                use_container_width=True,
                key="creative_button"
            ):
                st.session_state.selected_industry = "Creative"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

        else:

            st.markdown(
                '<div class="industry-tab-button">',
                unsafe_allow_html=True
            )

            if st.button(
                "🎨 Creative",
                use_container_width=True,
                key="creative_button"
            ):
                st.session_state.selected_industry = "Creative"
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================
    # INDUSTRY CONTENT
    # ==========================================

    st.markdown(
        '<div class="industry-content">',
        unsafe_allow_html=True
    )


    # ==========================================
    # TECH
    # ==========================================

    if st.session_state.selected_industry == "Tech":

        st.html("""
<div class="resource-card">

    <h3>Software Development</h3>

    <ul>
        <li>Programming languages (Python, Java, JavaScript)</li>
        <li>Frameworks (React, Django, Spring)</li>
        <li>Tools (Git, Docker, Kubernetes)</li>
        <li>Methodologies (Agile, Scrum, CI/CD)</li>
    </ul>

</div>
""")


    # ==========================================
    # BUSINESS
    # ==========================================

    elif st.session_state.selected_industry == "Business":

        st.html("""
<div class="resource-card">

    <h3>Business &amp; Management</h3>

    <ul>
        <li>Project management</li>
        <li>Stakeholder engagement</li>
        <li>Budget management</li>
        <li>Strategic planning</li>
        <li>Team leadership</li>
    </ul>

</div>
""")


    # ==========================================
    # CREATIVE
    # ==========================================

    elif st.session_state.selected_industry == "Creative":

        st.html("""
<div class="resource-card">

    <h3>Creative &amp; Design</h3>

    <ul>
        <li>Adobe Creative Suite</li>
        <li>UI/UX Design</li>
        <li>Wireframing &amp; Prototyping</li>
        <li>Brand identity</li>
        <li>Visual communication</li>
    </ul>

</div>
""")


    st.markdown("</div>", unsafe_allow_html=True)


    # ==========================================
    # SEPARATOR
    # ==========================================

    st.markdown("---")


    # ==========================================
    # RESUME TEMPLATES
    # ==========================================

    st.html("""
<div class="resource-section">

    <div class="resource-title">
        🧾 ATS-Friendly Resume Templates
    </div>

    <div class="template-card">

        <h3>📄 Coming Soon</h3>

        <p>
            Downloadable ATS-optimized resume templates
            will be available here soon.
        </p>

    </div>

</div>
""")