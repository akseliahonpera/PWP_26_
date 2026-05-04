import streamlit as st

def render_jobs(category = None):
    if category:
        # Reset category so that next call wont incorrectly include old input
        category = None
        st.header("show all jobs that match the string in category here")
    else:
        st.header("Show all jobs here")

def render_job_search(search_query):
    st.header(f"Search result for {search_query}")
    # Show jobs which were found by the query (or just the exact match)

def render_job():
    st.header("get all job data and display prettily here")
