'''
Contains all UI renders related to job content
'''
import streamlit as st
from datetime import datetime
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
    timetables(job, f"tt-{key}")
    ##muuta deploymenttiin oikea serveri
    map_aux_params = f"http://84.250.22.64:80/map_aux/?lon={job['longitude']}&lat={job['latitude']}&label={job['job_name']}"

    st.iframe(src=map_aux_params, height=600)#korjaa, on hieman paska atm, offset



def timetables(job, key):
    '''
    Get and show timetables
    '''
    timetable_objects = client.get_timetables(job['job_name']).json()

    if len(timetable_objects) == 0:
        st.write("No timetables found for the job.")
    else:
        st.write("Timetables:")
        for i, timetable in enumerate(timetable_objects):
            c = st.container(border=True)
            c.write(f"Title: {timetable['title']}")
            c.write(f"{timetable['start_time']} - {timetable['end_time']}")

            if timetable['is_booked']:
                c.write("Status: Not Available")
            else:
                c.write("Status: Available.")

            col1, col2 = c.columns(2)

            if client.user == job['username']:
                if col1.button("Edit", key=f"tt-edit-{i}"):
                    edit_timetable(job, timetable)
                if col2.button("Delete", key=f"tt-delete-{i}"):
                    delete_timetable(job, timetable)


    if "show_add_timetable" not in st.session_state:
        st.session_state.show_add_timetable = False

    if st.button("Add timetable"):
        st.session_state.show_add_timetable = True

    if st.session_state.show_add_timetable:
        add_timetable(job)



@st.dialog("Add a job:")
def add_job():
    '''
    test
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
    Edit
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
    Delete
    '''
    st.warning(f"Deleting: {job['job_name']}")

    column1, column2 = st.columns(2)

    if column1.button("Delete"):
        response = client.delete_job(job["job_name"])
        st.info(response)
        st.rerun()

    if column2.button("Cancel"):
        st.rerun()

def add_timetable(job):
    '''
    Add a timetable
    '''
    form = st.form("add_timetable_form")

    title = form.text_input("Title", "")
    #start_time = form.text_input("Start time:", "")
    #end_time = form.text_input("End time:", "")

    start_date = form.date_input("Start date")
    start_time = form.time_input("Start time")

    end_date = form.date_input("End date")
    end_time = form.time_input("End time")

    is_booked = form.checkbox("Booked")

    if form.form_submit_button("Add."):
        start = datetime.combine(start_date, start_time).isoformat()
        end = datetime.combine(end_date, end_time).isoformat()

        new_timetable = {
            "job_name": job['job_name'],
            "title": title,
            "start_time": start,
            "end_time": end,
            "is_booked": is_booked
        }
        response = client.post_timetable(job['job_name'], new_timetable)

        st.session_state.show_add_timetable = False
        st.success(response)

def edit_timetable(job, timetable):
    pass

def delete_timetable(job, timetable):
    pass
