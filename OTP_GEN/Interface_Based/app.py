import streamlit as st
import random
import os

# Define the path for the OTP file
OTP_FILE_PATH = "M:/All Projects/Mini Projects/python projects/OTP_GEN/otp.txt"
# Should be changed

def generate_otp():
    return random.randint(1000, 9999)


def write_otp(otp, filepath):
    with open(filepath, 'w') as otp_file:
        otp_file.write(str(otp))


def read_otp(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as otp_file:
            return otp_file.read()
    else:
        return None


def main():
    st.title("OTP-Based Login System")

    # Initialize session state variables for tracking attempts
    if 'attempts_left' not in st.session_state:
        st.session_state['attempts_left'] = 3
    if 'otp_generated' not in st.session_state:
        st.session_state['otp_generated'] = False

    username = st.text_input("Enter your Username")

    if st.button("Generate OTP") and username:
        otp = generate_otp()
        write_otp(otp, OTP_FILE_PATH)
        st.session_state['otp_generated'] = True
        st.success("OTP generated and sent successfully!")
        st.write(f"Generated OTP: {otp}")  # Display the OTP for demonstration purposes

    user_otp = st.text_input("Enter the OTP you received", type="password")

    if st.button("Login"):
        if st.session_state['otp_generated']:
            otp_sent = read_otp(OTP_FILE_PATH)
            if otp_sent:
                if user_otp == otp_sent:
                    st.success(f"Login Successful")
                    st.success(f"Welcome, {username}!")
                else:
                    st.session_state['attempts_left'] -= 1
                    if st.session_state['attempts_left'] > 0:
                        st.error(f"Invalid OTP. You have {st.session_state['attempts_left']} more attempts.")
                    else:
                        st.error("You have entered the wrong OTP too many times. Please try again later.")
                        st.session_state['otp_generated'] = False  # Disable further OTP entries
        else:
            st.error("OTP not generated. Please generate an OTP first.")

    if st.session_state['attempts_left'] == 0:
        st.stop()


if __name__ == "__main__":
    main()
