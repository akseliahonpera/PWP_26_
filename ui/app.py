from api_client import APIClient
import streamlit as st
# Add render function imports to pages/__init__.py, then import that function here
from renders import *

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

st.title("Väinämöinen Employment UI Client")

if "page" not in st.session_state:
    st.session_state.page = "main_menu"

st.sidebar.title("Navigation")

#########################
### Initializations   ###
#########################
st.session_state["category"] = None
st.session_state["search_query"] = ""

#########################
### Sidebar code      ###
#########################

if st.sidebar.button("Main menu"):
    st.session_state.page = "main_menu"

if st.sidebar.button("Profile"):
    st.session_state.page = "own_profile"

if st.sidebar.button("See all users"):
    st.session_state.page = "all_users"

if st.sidebar.button("User search"):
    st.session_state.page = "user_search"

if st.sidebar.button("See all jobs"):
    st.session_state.page = "jobs"

if st.sidebar.button("Job search"):
    st.session_state.page = "job_search"

if st.sidebar.button("Jobs by category"):
    category = st.text_input("Category")
    st.session_state["category"] = category
    st.session_state.page = "jobs"



if st.session_state.page == "main_menu":
    render_main_menu()

# Call public route
if st.session_state.page == "own_profile":
    render_owned_profile()

# !!To get UI to update to correct profile, update the state variable from UI input right before switching page to public_profile!!
if st.session_state.page == "public_profile":
    render_public_profile(st.session_state["current_public_profile"])

if st.session_state.page == "all_users":
    render_all_users()

# !!To get UI to update to correct search, update the state variable from UI input right before switching page to user_search!!
if st.session_state.page == "user_search":
    render_user_search(st.session_state["search_query"])

# Same as above, right before changing page to job_search, update category
# render_jobs sets category back to None in case user doesn't search with a category
# Calling job search with no category set renders all jobs
if st.session_state.page == "jobs":
    render_jobs(st.session_state["category"])

if st.session_state.page == "job_search":
    render_job_search(st.session_state["search_query"])
