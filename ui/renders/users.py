'''
Contains all UI renders related to user content
'''
import streamlit as st

from api_client import APIClient #pylint: disable=import-error
from renders.jobs import job_item

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
    response = client.get_user(client.user)

    match response.status_code:
        case 200:
            # TODO: make a pretty menu of all things relevant here,
            # update user data, delete user, post jobs, route to said jobs, delete jobs etc.
            user_data = response.json()
            profile, jobs, settings = st.tabs(["profile", "jobs", "settings"])

            ####################################
            ### Profile page                 ###
            ####################################

            profile.write(f"Username: {user_data.get('username')}")
            profile.write(f"Email: {user_data.get('email')}")
            profile.write(f"Phone number: {user_data.get('phone_number')}")
            profile.write(f"Address: {user_data.get('address')}")
            profile.space("xsmall")
            profile.write(f"Your description: {user_data.get('description')}")
            profile.space("xsmall")
            profile.write(f"You created this account at: {user_data.get('created')}")

            ####################################
            ### Jobs page                    ###
            ####################################

            user_jobs = client.get_all_jobs().json()
            for i, job in enumerate(user_jobs):
                if client.user == job["username"]:
                    job_item(job, i, jobs)
            #    st.space("small")

            ####################################
            ### Settings page                ###
            ####################################
        case 403:
            st.write("API authentication key did not have valid permissions for this action")
            st.write("Missing either matching user key or admin key")

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
    st.header("Login page")
    clicked = st.button("Log into your account")
    if clicked:
        log_in()

@st.dialog("Log in with existing credentials")
def log_in():
    '''Rendering function for logging in, dialogue'''
    st.write("Please provide your credentials")
    username = st.text_input("Username", "")
    password = st.text_input("Password", type="password")

    if st.button("Log in"):
        # The .get_user call requires admin permissions
        # Db/API should maybe have a service where passwords can be checked against usernames for validity
        # without exposing said password through the API
        response = client.get_user(username)

        match response.status_code:
            case 403:
                st.write("You are not authorized for this action")
                st.write("Set the correct API key from the main menu")
            case 404:
                st.write("The account does not exist")
            case 200:
                user = response.json()
                if user["password"] == password:
                    # TODO: Get and set the user API key from the user object to client state
                    # once the auth implementation works
                    client.set_user(username)
                    st.write("Login successful!")
                else:
                    st.write("Password was incorrect")
            case _:
                response.raise_for_status()

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
        match response.status_code:
            case 201:
                client.set_user(username)
                st.write("Account was created successfully!")
            case 400:
                st.write("Server couldn't validate the request (400)")
            case 409:
                st.write("A conflict occurred")
            case 415:
                st.write("Fields were not filled properly")
            case _:
                response.raise_for_status()
