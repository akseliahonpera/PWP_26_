'''
Contains all UI renders related to job content
'''
import streamlit as st

from api_client import APIClient #pylint: disable=import-error

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

def render_jobs(category = None):
    '''
    Rendering function for all jobs
    Category can be used to limit the rendered jobs
    '''
    # testing adding a job through a pop up
    if st.button("Add a new job (temporary test)"):
        add_job()

    if category:
        # Reset category so that next call wont incorrectly include old input
        category = None
        st.header("show all jobs that match the string in category here")
    else:
        st.header("All Jobs")
        jobs = client.get_all_jobs().json()
        for i, job in enumerate(jobs):
            job_item(job, i)
            st.space("small")

def render_job_search(search_query):
    '''
    Rendering function for a job search with a query
    '''
    st.header(f"Search result for {search_query}")
    # Show jobs which were found by the query (or just the exact match)

def render_job():
    '''
    Rendering function for the specific data of a specific job
    '''
    st.header("get all job data and display prettily here")

def job_item(job, key):
    '''
    Rendering function for short introductory data for a job
    '''
    c = st.container(border=True)
    c.write(f"Username: {job['username']}")
    c.write(f"Job name: {job['job_name']}")
    c.write(f"Description: {job['job_description']}")

    if c.button("View More", key=key):
        job_info(job)

@st.dialog("About job:")
def job_info(job):
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
    map_aux_params = f"http://localhost:5173?lon={job['longitude']}" \
    f"&lat={job['latitude']}&label={job['job_name']}"

    st.iframe(src=map_aux_params, height=600)#korjaa, on hieman paska atm, offset



def timetables(job):
    '''
    Get and show timetables
    '''
    timetable_objects = client.get_timetables(job['job_name']).json()

    if len(timetable_objects) == 0:
        st.write("No timetables found for the job.")
    else:
        st.write("Timetables:")
        for timetable in timetable_objects:
            c = st.container(border=True)
            c.write(f"Title: {timetable['title']}")
            c.write(f"{timetable['start_time']} - {timetable['end_time']}")

            if timetable['is_booked']:
                c.write("Status: Not Available")
            else:
                c.write("Status: Available.")

@st.dialog("Add a job:")
def add_job():
    '''
    test
    '''
    username = st.text_input("Username", "")
    job_name = st.text_input("Job Name", "")
    job_desc = st.text_input("Description", "")
    latitude = st.text_input("Latitude:", "")
    longitude = st.text_input("Longitude:", "")
    location = st.text_input("Location:", "")
    opening_hours = st.text_input("Opening Hours:", "")
    category = st.text_input("Category:", "")

    if st.button("Add"):
        new_job = {
            "username": username,
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
