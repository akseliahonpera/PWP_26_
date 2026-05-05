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
