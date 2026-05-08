import streamlit as st

from api_client import APIClient #pylint: disable=import-error

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

def render_main_menu():
    st.header("Main menu")
    # include stuff like a short usage guide, ip change (client.set_ip) to a ui element
    # and maybe a login page and a link to signup page?
    # API auth key should also be set here (client.set_api_key)

    with st.expander(f"Current IP address for API calls: {client.ip}"):
        new_ip = st.text_input("New address: ")
        clicked = st.button("Apply new IP")
        if clicked:
            st.write(f"Setting new IP of {new_ip}")
            client.set_ip(new_ip)
        default_clicked = st.button("Reset to localhost address")
        if default_clicked:
            st.write("Defaulting IP to localhost")
            client.set_ip(localhost=True)

    login = st.button("Log in")
    signup = st.button("Sign up")

    if login:
        st.session_state.page = "login"
    if signup:
        st.session_state.page = "signup"
