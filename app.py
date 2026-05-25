import streamlit as st

# Configure the web page
st.set_page_config(page_title="michaelabart BMI Calculator", layout="centered")

# Initialize a fake database using session state (persists during the browser session)
if "user_database" not in st.session_state:
    st.session_state.user_database = {"admin": "1234"}
if "screen" not in st.session_state:
    st.session_state.screen = "signup"

# Navigation helpers
def navigate_to(screen_name):
    st.session_state.screen = screen_name
    st.rerun()

# --- 1. SIGNUP SCREEN ---
if st.session_state.screen == "signup":
    st.title("Karibu, it's BMI Calculator")
    st.subheader("Create a new account")
    
    signup_user = st.text_input("Choose Username", key="su_user")
    signup_pass = st.text_input("Choose Password", type="password", key="su_pass")
    
    if st.button("Sign Up", use_container_width=True):
        if not signup_user or not signup_pass:
            st.warning("Fields cannot be empty!")
        elif signup_user in st.session_state.user_database:
            st.error("Username already exists!")
        else:
            st.session_state.user_database[signup_user] = signup_pass
            st.success("Account created! You can now Sign In.")
            
    if st.button("Already have an account? Sign In", use_container_width=True):
        navigate_to("signin")

# --- 2. SIGNIN SCREEN ---
elif st.session_state.screen == "signin":
    st.title("michaelabart")
    st.subheader("Welcome back!")
    
    signin_user = st.text_input("Username", key="si_user")
    signin_pass = st.text_input("Password", type="password", key="si_pass")
    
    if st.button("Sign In", use_container_width=True):
        if signin_user in st.session_state.user_database and st.session_state.user_database[signin_user] == signin_pass:
            navigate_to("bmi")
        else:
            st.error("Invalid Username or Password")
            
    if st.button("New here? Create an account", use_container_width=True):
        navigate_to("signup")

# --- 3. BMI CALCULATOR SCREEN ---
elif st.session_state.screen == "bmi":
    st.title("BMI Calculator")
    st.subheader("Enter your metrics below")
    
    weight = st.number_input("Weight (kg)", min_value=0.0, step=0.1, value=70.0)
    height = st.number_input("Height (meters)", min_value=0.0, step=0.01, value=1.75)
    
    if st.button("Calculate BMI", use_container_width=True):
        if height > 0:
            bmi = weight / (height ** 2)
            
            if bmi < 18.5:
                category, color = "Underweight", "orange"
            elif 18.5 <= bmi < 25:
                category, color = "Normal weight", "green"
            elif 25 <= bmi < 30:
                category, color = "Overweight", "orange"
            else:
                category, color = "Obese", "red"
                
            st.markdown(f"### Your BMI: **{bmi:.1f}**")
            st.markdown(f"Category: :{color}[**{category}**]")
        else:
            st.error("Height must be greater than zero!")
            
    st.divider()
    if st.button("Log Out", use_container_width=True):
        navigate_to("signin")
