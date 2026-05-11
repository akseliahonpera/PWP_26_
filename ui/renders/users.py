'''
Contains all UI renders related to user content
'''
import streamlit as st

from api_client import APIClient #pylint: disable=import-error

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

def render_public_profile(username):
    '''
    Rendering function for a public profile
    '''
    st.header(f"{username}'s profile")

def render_owned_profile():
    '''
    Rendering function for a users own profile, with private information
    '''
    st.header("Your profile")

def render_signup():
    '''
    Rendering function for a signup page
    '''
    st.header("User creation")
    clicked = st.button("Create a new account")
    if clicked:
        add_user()

def render_user_search(search_query):
    '''
    Rendering function for a user search function
    '''
    st.header(f"Search result for {search_query}")
    # TODO: implement
    # Show user profiles which were found by the query (or just the exact match)

def render_all_users():
    '''
    Rendering function for seeing all users on the site
    '''
    st.header("All users")
    users = client.get_users_public().json()
    for user in users:
        c = st.container()
        c.write(f"Username: {user['username']}")
        c.write(f"Description: {user['description']}")
        c.write(f"Email: {user['email']}")
        c.write(f"Time of creation: {user['created']}")
        st.space("small")

def render_login():
    '''
    Rendering function for login functionlality
    '''
    # TODO: implement

@st.dialog("Create a new user")
def add_user():
    '''
    Rendering function for adding/posting a new user to the database
    '''
    st.write("Please fill out all the following fields")
    username = st.text_input("Username", "")
    email = st.text_input("Email", "")
    password = st.text_input("Password*", type="password")
    phone_number = st.text_input("Phone number", "")
    description = st.text_input("Profile description", "")
    address = st.text_input("Address", "")

    payload = {
        "username": username,
        "password": password,
        "email": email,
        "phone_number": phone_number,
        "description": description,
        "address": address
    }
    if st.button("Create account"):
        response = client.post_user(payload)
        st.info(response)
