import streamlit as st

from api_client import APIClient #pylint: disable=import-error

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

def render_public_profile(username):
    st.header(f"{username}'s profile")

def render_owned_profile():
    st.header("Your profile")

def render_signup():
    st.header("Spots for user input, grab user data")
    # Then compile a JSON, send on over to api_client.py func that calls API that adds new user to db

def render_user_search(search_query):
    st.header(f"Search result for {search_query}")
    # Show user profiles which were found by the query (or just the exact match)

def render_all_users():
    st.header("All users")
    users = client.get_users_public().json()
    for user in users:
        c = st.container()
        c.write(f"Username: {user['username']}")
        c.write(f"Description: {user['description']}")
        c.write(f"Email: {user['email']}")
        c.write(f"Time of creation: {user['created']}")
        st.space("small")
