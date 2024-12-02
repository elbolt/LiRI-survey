import streamlit as st
import sqlite3

# Title of the app
st.title('Survey on Statistical and Data Science Consulting Services at LiRI')

# Description
st.write('We are conducting a survey to improve our services. Please help us by providing your feedback.')

# Collect user information
level_options = ['Bachelor', 'Master', 'PhD', 'Postdoc', 'Principal investigator or professor', 'Other']
level = st.radio('Please select your current level of study or position:', level_options)
if level == 'Other':
    level = st.text_input('Please specify your level of study or position:')
    if len(level) < 3:
        st.warning('Please enter a valid level of study or position.')

# Add yes/no question
st.write('Are you associated with the University of Zurich?')
associated = st.radio('Please select:', ['Yes', 'No'])

researchfield = st.text_input('What is your field of study?')
if len(researchfield) < 3:
    st.warning('Please enter a valid field of research.')

# Submit button
if st.button('Submit'):
    if len(level) < 3 or len(researchfield) < 3:
        st.error("Please fill in all fields correctly.")
    else:
        # Save data to the database
        try:
            # Use Streamlit secrets to get the database path
            db_path = st.secrets["db"]["path"]

            # Connect to SQLite database
            conn = sqlite3.connect(db_path)
            c = conn.cursor()

            # Create table if it doesn't exist
            c.execute("""
                CREATE TABLE IF NOT EXISTS survey (
                    level TEXT,
                    associated TEXT,
                    researchfield TEXT
                )
            """)

            # Insert data into the table
            c.execute("INSERT INTO survey (level, associated, researchfield) VALUES (?, ?, ?)", 
                      (level, associated, researchfield))
            conn.commit()
            conn.close()

            # Show confirmation
            st.success('Thank you for your feedback!')

        except Exception as e:
            st.error(f"An error occurred: {e}")