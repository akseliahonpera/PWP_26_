'''
Contains all UI renders related to job content
'''
import streamlit as st
from api_client import APIClient #pylint: disable=import-error
from renders.timetables import timetables

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

def render_jobs(category = None):
    '''
    Rendering function for all jobs
    Category can be used to limit the rendered jobs
    '''

    if client.user != "":
        if st.button("Add a new job"):
            add_job()

    if category:
        # Reset category so that next call wont incorrectly include old input
        category = None
        st.header("show all jobs that match the string in category here")
    else:
        st.header("All Jobs")
        jobs = client.get_all_jobs().json()
        for i, job in enumerate(jobs):
            job_item(job, i, st)
            st.space("small")

def render_job_search():
    '''
    Rendering function for a job search with a query
    '''
    st.header("Search bar for jobs")
    query =  st.text_input("Type a job name here", "")
    if st.button("Search"):
        if query == "":
            st.write("Input a search parameter first")
        else:
            response = client.get_job(query)
            match response.status_code:
                case 200:
                    c = st.container()
                    job_item(response.json(), 1, c)
                case 404:
                    st.write("Job not found")
                    st.write("Try another parameter, only specific matches show up")


def render_job():
    '''
    Rendering function for the specific data of a specific job
    '''
    st.header("get all job data and display prettily here")

def job_item(job, key, draw_place):
    '''
    Rendering function for short introductory data for a job
    '''
    c = draw_place.container(border=True)
    c.write(f"Username: {job['username']}")
    c.write(f"Job name: {job['job_name']}")
    c.write(f"Description: {job['job_description']}")

    column1, column2, column3 = c.columns(3)

    if column1.button("View More", key=f"view-{key}"):
        job_info(job, key)

    if client.user == job['username']:
        if column2.button("Edit", key=f"edit-{key}"):
            edit_job(job)
        if column3.button("Delete", key=f"delete-{key}"):
            delete_job(job)

@st.dialog("About job:")
def job_info(job, key):
    '''
    A pop up to show more information about the job
    '''
    st.write(f"Username: {job['username']}")
    st.write(f"Job name: {job['job_name']}")
    st.write(f"Description: {job['job_description']}")
    st.write(f"Location: {job['location']}")
    st.write(f"Created: {job['created']}")
    st.write(f"Opening hours: {job['opening_hours']}")
    st.write(f"Category: {job['category']}")
    st.write("")
    timetables(job)
    ##muuta deploymenttiin oikea serveri
    map_aux_params = f"http://84.250.22.64:80/map_aux/?lon={job['longitude']}&lat={job['latitude']}&label={job['job_name']}"

    st.iframe(src=map_aux_params, height=600)#korjaa, on hieman paska atm, offset

@st.dialog("Add a job:")
def add_job():
    '''
    A pop up to add a new job
    '''
    job_name = st.text_input("Job Name", "")
    job_desc = st.text_input("Description", "")
    latitude = st.text_input("Latitude:", "")
    longitude = st.text_input("Longitude:", "")
    location = st.text_input("Location:", "")
    opening_hours = st.text_input("Opening Hours:", "")
    category = st.text_input("Category:", "")

    if st.button("Add"):
        new_job = {
            "username": client.user,
            "job_name": job_name,
            "job_description": job_desc,
            "latitude": latitude,
            "longitude": longitude,
            "location": location,
            "opening_hours": opening_hours,
            "category": category
        }
        response = client.post_job(new_job)
        st.info(response)

@st.dialog("Edit a job:")
def edit_job(job):
    '''
    A pop up to edit a job
    '''
    job_desc = st.text_input("Description", job["job_description"])
    latitude = st.text_input("Latitude:", job["latitude"])
    longitude = st.text_input("Longitude:", job["longitude"])
    location = st.text_input("Location:", job["location"])
    opening_hours = st.text_input("Opening Hours:", job["opening_hours"])
    category = st.text_input("Category:", job["category"])

    if st.button("Edit"):
        new_job = {
            "username": job['username'],
            "job_name": job['job_name'],
            "job_description": job_desc,
            "latitude": latitude,
            "longitude": longitude,
            "location": location,
            "opening_hours": opening_hours,
            "category": category
        }
        response = client.update_job(new_job)
        st.info(response)

@st.dialog("Are you sure you want to delete this job?")
def delete_job(job):
    '''
    A pop up to delete a job
    '''
    st.warning(f"Deleting: {job['job_name']}")

    column1, column2 = st.columns(2)

    if column1.button("Delete"):
        response = client.delete_job(job["job_name"])
        st.info(response)
        st.rerun()

    if column2.button("Cancel"):
        st.rerun()
