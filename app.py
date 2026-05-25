import streamlit as st

# Configure the web page
st.set_page_config(page_title="michaelabart BMI Calculator",
                   page_icon="⚖️", layout="centered")

# Custom CSS styling for a cleaner dark/modern theme interface
st.markdown("""
    <style>
    .stButton>button {
        border-radius: 8px;
        height: 3em;
        font-weight: bold;
    }
    .main-card {
        background-color: #1e1e1e;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize fake database using session state
if "user_database" not in st.session_state:
    st.session_state.user_database = {"admin": "1234"}
if "screen" not in st.session_state:
    st.session_state.screen = "signup"

# Navigation helper


def navigate_to(screen_name):
    st.session_state.screen = screen_name
    st.rerun()


# --- 1. SIGNUP SCREEN ---
if st.session_state.screen == "signup":
    st.title("⚖️ Karibu, it's BMI Calculator")
    st.markdown("### **Create a new account**")

    # Using a visual container block
    with st.container(border=True):
        signup_user = st.text_input(
            "Choose Username", placeholder="e.g., john_doe", key="su_user")
        signup_pass = st.text_input(
            "Choose Password", type="password", placeholder="••••••••", key="su_pass")

        st.write("")  # Spacer
        if st.button("🚀 Sign Up", use_container_width=True, type="primary"):
            if not signup_user or not signup_pass:
                st.warning("⚠️ Fields cannot be empty!")
            elif signup_user in st.session_state.user_database:
                st.error("❌ Username already exists!")
            else:
                st.session_state.user_database[signup_user] = signup_pass
                st.success(
                    "✅ Account created successfully! Click 'Sign In' below.")

    st.write("")
    if st.button("Already have an account? Sign In", use_container_width=True):
        navigate_to("signin")

# --- 2. SIGNIN SCREEN ---
elif st.session_state.screen == "signin":
    st.title("👤 michaelabart")
    st.markdown("### **Welcome back!**")

    with st.container(border=True):
        signin_user = st.text_input(
            "Username", placeholder="Enter your username", key="si_user")
        signin_pass = st.text_input(
            "Password", type="password", placeholder="Enter your password", key="si_pass")

        st.write("")  # Spacer
        if st.button("🔑 Sign In", use_container_width=True, type="primary"):
            if signin_user in st.session_state.user_database and st.session_state.user_database[signin_user] == signin_pass:
                navigate_to("bmi")
            else:
                st.error("❌ Invalid Username or Password")

    st.write("")
    if st.button("New here? Create an account", use_container_width=True):
        navigate_to("signup")

# --- 3. BMI CALCULATOR SCREEN ---
elif st.session_state.screen == "bmi":
    st.title("📊 BMI Calculator, By michaelalbart")
    st.markdown("### **Enter your metrics below**")

    with st.container(border=True):
        # Interactive sliders alongside number inputs for an premium feel
        weight = st.slider("Weight (kg)", min_value=10.0,
                           max_value=200.0, value=70.0, step=0.1)
        height = st.slider("Height (meters)", min_value=0.5,
                           max_value=2.5, value=1.75, step=0.01)

        st.write("")
        if st.button("⚡ Calculate BMI", use_container_width=True, type="primary"):
            if height > 0:
                bmi = weight / (height ** 2)

                # Determine BMI conditions, colors, and specific feedback
                if bmi < 18.5:
                    category, color, progress_val, advice = "Underweight", "orange", 0.2, "Consider consulting a healthcare provider about balanced nutritional intake."
                elif 18.5 <= bmi < 25:
                    category, color, progress_val, advice = "Normal weight", "green", 0.5, "Great job! Keep maintaining your healthy lifestyle, balanced diet, and active routine."
                elif 25 <= bmi < 30:
                    category, color, progress_val, advice = "Overweight", "orange", 0.75, "Consider engaging in regular physical activity and adjusting calorie targets."
                else:
                    category, color, progress_val, advice = "Obese", "red", 1.0, "It is recommended to seek nutritional or medical guidance for weight management support."

                st.divider()

                # Visual Metric Boxes
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Your BMI Score", value=f"{bmi:.1f}")
                with col2:
                    st.metric(label="Status Category", value=category)

                # Progress bar visualization
                st.progress(
                    progress_val, text=f"Category Range Placement: {category}")

                # Highlighted customized advice box
                st.info(f"💡 **Health Suggestion:** {advice}")

            else:
                st.error("❌ Height must be greater than zero!")

    st.write("")
    st.divider()
    if st.button("🚪 Log Out", use_container_width=True):
        navigate_to("signin")
