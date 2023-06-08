import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False
    
    col1, col2, col3 = st.columns([1,1,1])

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        col2.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        col2.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        col2.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True