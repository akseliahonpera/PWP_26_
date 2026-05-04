import streamlit as st

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
    st.header("All users here")
