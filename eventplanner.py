import streamlit as st
import sqlite3
from datetime import datetime, timedelta

def create_table():
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            event_date DATE NOT NULL,
            event_time TIME NOT NULL,
            event_details TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_data(event_type, event_date, event_time, event_details):
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO event1 (event_type, event_date, event_time, event_details) VALUES (?, ?, ?, ?)', (event_type, event_date, event_time, event_details))
    conn.commit()
    conn.close()

def read_data():
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event1')
    events = cursor.fetchall()
    conn.close()
    return events

def delete_data(event_id):
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM event1 WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

def validate_time(event_time):
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event1 WHERE event_time = ?', (event_time,))
    conflicting_events = cursor.fetchall()
    conn.close()
    return conflicting_events


def send_notifications():
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    current_time_str = current_time.strftime('%H:%M:%S')  # Convert time to string
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event1 WHERE event_date = ? AND event_time = ?', (current_date, current_time_str))
    upcoming_events = cursor.fetchall()
    conn.close()
    for event in upcoming_events:
        st.write(f"Notification: The {event[1]} event - {event[4]} is scheduled for today at {event[3]}.")

import streamlit as st
import sqlite3
from datetime import datetime, timedelta

def create_table():
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS event1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT NOT NULL,
            event_date DATE NOT NULL,
            event_time TIME NOT NULL,
            event_details TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_data(event_type, event_date, event_time, event_details):
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO event1 (event_type, event_date, event_time, event_details) VALUES (?, ?, ?, ?)', (event_type, event_date, event_time, event_details))
    conn.commit()
    conn.close()

def read_data():
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event1')
    events = cursor.fetchall()
    conn.close()
    return events

def delete_data(event_id):
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM event1 WHERE id = ?', (event_id,))
    conn.commit()
    conn.close()

def validate_time(event_time):
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event1 WHERE event_time = ?', (event_time,))
    conflicting_events = cursor.fetchall()
    conn.close()
    return conflicting_events

def send_notifications():
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    current_time_str = current_time.strftime('%H:%M:%S')
    conn = sqlite3.connect('event.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM event1 WHERE event_date = ? AND event_time = ?', (current_date, current_time_str))
    upcoming_events = cursor.fetchall()
    conn.close()
    for event in upcoming_events:
        st.write(f"Notification: The {event[1]} event - {event[4]} is scheduled for today at {event[3]}.")

def main():
    create_table()
    st.title("Hotel Event Planner")

    # Sidebar
    st.sidebar.title("Options")
    selected_option = st.sidebar.selectbox("Select Option", ["Add Event", "View Events"])

    if selected_option == "Add Event":
        st.sidebar.subheader("Add Event")
        event_type = st.sidebar.selectbox("Event Type", ["Birthday", "Marriage", "Business Meeting/Conference"])
        event_date = st.sidebar.date_input("Event Date")
        event_time = st.sidebar.time_input("Event Time")
        event_details = st.sidebar.text_input("Event Details", "")

        if st.sidebar.button("Add"):
            # Validate time
            event_time_str = event_time.strftime('%H:%M:%S')
            conflicting_events = validate_time(event_time_str)
            if conflicting_events:
                st.sidebar.error("Another event is already scheduled at this time.")
            else:
                create_data(event_type, event_date, event_time_str, event_details)
                st.sidebar.success("Event added successfully!")

    elif selected_option == "View Events":
        st.subheader("Scheduled Events")
        events = read_data()
        for event in events:
            st.write(f"**{event[1]}** - Date: {event[2]}, Time: {event[3]}, Details: {event[4]}")
            if st.button("Delete"):
                delete_data(event[0])
                st.success("Event deleted successfully!")

    send_notifications()

if __name__ == "__main__":
    main()

