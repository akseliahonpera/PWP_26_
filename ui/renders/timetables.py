'''
Timetables related UI content
'''
import streamlit as st
from datetime import datetime
from api_client import APIClient #pylint: disable=import-error

if "client" not in  st.session_state:
    st.session_state.client = APIClient()

client = st.session_state.client

def timetables(job):
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

                if "show_edit_timetable" not in st.session_state:
                    st.session_state.show_edit_timetable = False
                if col1.button("Edit", key=f"tt-edit-{i}"):
                    st.session_state.show_edit_timetable = True
                if st.session_state.show_edit_timetable:
                    edit_timetable(job, timetable)

                if col2.button("Delete", key=f"tt-delete-{i}"):
                    response = client.delete_timetable(job["job_name"], timetable['title'])
                    st.info(response)

    if "show_add_timetable" not in st.session_state:
        st.session_state.show_add_timetable = False
    if st.button("Add timetable"):
        st.session_state.show_add_timetable = True
    if st.session_state.show_add_timetable:
        add_timetable(job)

def add_timetable(job):
    '''
    Add a timetable
    '''
    form = st.form("add_timetable_form")

    title = form.text_input("Title", "")

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
    '''
    Edit timetable to set it booked or unbooked
    '''
    form = st.form(f"edit_timetable_form_{job['job_name']}_{timetable['title']}")
    form.write(f"Editing the timetable: {timetable['title']}")

    #start_date = form.date_input("Start date")
    #start_time = form.time_input("Start time")
    #end_date = form.date_input("End date")
    #end_time = form.time_input("End time")

    is_booked = form.checkbox("Booked", timetable['is_booked'])

    if form.form_submit_button("Edit."):
        #start = datetime.combine(start_date, start_time).isoformat()
        #end = datetime.combine(end_date, end_time).isoformat()

        new_timetable = {
            "job_name": job['job_name'],
            "title": timetable['title'],
            "start_time": timetable['start_time'],
            "end_time": timetable['end_time'],
            "is_booked": is_booked
        }
        response = client.update_timetable(job['job_name'], new_timetable)

        st.session_state.show_edit_timetable = False
        st.success(response)

def delete_timetable(job, timetable):
    '''
    Delete timetable
    '''
    st.warning(f"Deleting: {timetable['title']}")

    column1, column2 = st.columns(2)

    if column1.button("Delete"):
        response = client.delete_timetable(job["job_name"], timetable['title'])
        st.info(response)
        st.rerun()

    if column2.button("Cancel"):
        st.rerun()

    st.session_state.show_delete_timetable = False
