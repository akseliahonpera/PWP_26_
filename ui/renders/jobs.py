import streamlit as st

from api_client import APIClient #pylint: disable=import-error

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

def render_jobs(category = None):
    if category:
        # Reset category so that next call wont incorrectly include old input
        category = None
        st.header("show all jobs that match the string in category here")
    else:
        st.header("All Jobs")
        jobs = client.get_all_jobs().json()
        for job in jobs:
            c = st.container()
            c.write(f"Username: {job["username"]}")
            c.write(f"Job name: {job["job_name"]}")
            c.write(f"Description: {job["job_description"]}")
            st.space("small")

def render_job_search(search_query):
    st.header(f"Search result for {search_query}")
    # Show jobs which were found by the query (or just the exact match)

def render_job():
    st.header("get all job data and display prettily here")
