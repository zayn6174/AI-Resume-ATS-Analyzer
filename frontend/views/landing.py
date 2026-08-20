import streamlit as st


def render():

    # ==========================================
    # LANDING PAGE CSS
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
           MAIN HEADER
           ========================================== */

        .main-header {
            text-align: center;
            padding: 3rem 2rem;
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

        .main-header h1 {
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color:#DAA464;
        }
    

        /* ==========================================
           FEATURES SECTION
           ========================================== */

        .features-section {
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

        .features-title {
            text-align: center;
            color: white;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 30px;
        }


        /* ==========================================
           CARDS CONTAINER
           ========================================== */

        .features-container {
            display: flex;
            gap: 25px;
            align-items: stretch;
            
        }


        /* ==========================================
           KEY FEATURES CARDS
           ========================================== */

        .feature-card {
            flex: 1;
            width: 100%;
            height: 330px;
            box-sizing: border-box;

            background: #060D1F;
            padding: 28px;
            border-radius: 16px;

            border: 1px solid #16295C;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.25);

            overflow: hidden;
        }

        .feature-card h3 {
            color:#DAA464;
            font-size: 1.4rem;
            margin-top: 0;
            margin-bottom: 18px;
        }

        .feature-card p {
            color: darkgrey;
            line-height: 1.7;
            font-size: 1rem;
        }

        .feature-card li {
            color: darkgrey;
            margin-bottom: 10px;
            line-height: 1.5;
        }

        .feature-card strong {
            color: darkgrey;
        }


        /* ==========================================
           HOW IT WORKS CARDS
           ========================================== */

        .how-card {
            flex: 1;
            width: 100%;
            height: 220px;
            box-sizing: border-box;

            background: #060D1F;
            padding: 28px;
            border-radius: 16px;

            border: 1px solid #16295C;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.25);

            overflow: hidden;
        }

        .how-card h3 {
            color:#DAA464;
            font-size: 1.4rem;
            margin-top: 0;
            margin-bottom: 18px;
        }

        .how-card p {
            color: darkgrey;
            line-height: 1.7;
            font-size: 1rem;
        }


        /* ==========================================
           STREAMLIT DIVIDER
           ========================================== */

        hr {
            border-color: #16295C !important;
        }


        /* ==========================================
           STREAMLIT PRIMARY BUTTON
           ========================================== */

        .stButton > button[kind="primary"] {
            background-color: #0F1C3F;
            border: 1px solid #16295C;
            color: white;
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #16295C;
            border-color: #0F1C3F;
            color: white;
        }

    </style>
    """, unsafe_allow_html=True)


    # ==========================================
    # HERO SECTION
    # ==========================================

    st.markdown("""
    <div class="main-header">
        <h1>📄 ATS Resume Scorer</h1>
        <h3>Optimize Your Resume for Applicant Tracking Systems</h3>
        <p>
            Get instant feedback on your resume's ATS compatibility
            with AI-powered analysis
        </p>
    </div>
    """, unsafe_allow_html=True)


    # ==========================================
    # CALL-TO-ACTION BUTTON
    # ==========================================

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button(
            "⏱️ Start Analyzing Your Resume",
            use_container_width=True,
            type="primary"
        ):
            st.session_state.current_view = "scorer"
            st.rerun()


    st.markdown("---")


    # ==========================================
    # KEY FEATURES
    # ==========================================

    st.html("""
<div class="features-section">

    <div class="features-title">
        ✨ KEY FEATURES
    </div>

    <div class="features-container">

        <div class="feature-card">

            <h3>📊 Comprehensive Scoring</h3>

            <p>
                Get detailed scores across 5 key dimensions:
            </p>

            <ul>
                <li>Formatting (20%)</li>
                <li>Keywords &amp; Skills (25%)</li>
                <li>Content Quality (25%)</li>
                <li>Skill Validation (15%)</li>
                <li>ATS Compatibility (15%)</li>
            </ul>

        </div>


        <div class="feature-card">

            <h3>🔍 Skill Validation</h3>

            <p>
                Verify that your claimed skills are demonstrated
                in your projects and experience using AI-powered
                semantic analysis.
            </p>

            <p>
                <strong>No more empty claims!</strong>
            </p>

        </div>


        <div class="feature-card">

            <h3>🔒 Privacy First</h3>

            <p>
                All analysis runs locally with no external API calls.
                Your resume data never leaves your system.
            </p>

            <p>
                <strong>100% Private &amp; Secure</strong>
            </p>

        </div>

    </div>

</div>
""")


    # ==========================================
    # SEPARATOR
    # ==========================================

    st.markdown("---")


    # ==========================================
    # HOW IT WORKS
    # ==========================================

    st.html("""
<div class="features-section">

    <div class="features-title">
        🔎 HOW IT WORKS
    </div>

    <div class="features-container">

        <div class="how-card">

            <h3>📋 Upload Your Resume</h3>

            <p>
                Support for PDF, DOC, and DOCX formats.
            </p>

        </div>


        <div class="how-card">

            <h3>🤖 AI Analysis</h3>

            <p>
                Our local AI models analyze your resume
                across multiple dimensions.
            </p>

        </div>


        <div class="how-card">

            <h3>📈 Get Actionable Feedback</h3>

            <p>
                Receive detailed recommendations to improve
                your resume and increase its ATS compatibility.
            </p>

        </div>

    </div>

</div>
""")