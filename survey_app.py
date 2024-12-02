import streamlit as st
import sqlite3

# Title of the app
st.title('Survey on Statistical and data science consulting services at LiRI')

# Description
st.write('We are conducting a survey to improve our services. Please help us by providing your feedback.')

# Collect user information
level_options = ['Bachelor', 'Master', 'PhD', 'Postdoc', 'Principal investigator or professor', 'other']
level = st.radio('Please select your current level of study or position:', level_options)
if level == 'other':
    level = st.text_input('Please specify your level of study or position:')
    if len(level) < 3:
        st.warning('Please enter a valid level of study or position.')

# Add yes no question
st.write('Are you associated with the University of Zurich?')
associated = st.radio('Please select:', ['Yes', 'No'])

researchfield = st.text_input('What is your field of study?')
if len(researchfield) < 3:
    st.warning('Please enter a valid field of research.')

# New page


# Submit button
if st.button('Submit'):
    # Show confirmation
    st.success(f'Thank you for you feedback!')
    # Save data to a file (append mode)

    # Save data to a database
    conn = sqlite3.connect('survey.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS survey (level TEXT, associated TEXT, researchfield TEXT)")
    c.execute("INSERT INTO survey (level, associated, researchfield) VALUES (?, ?, ?)", (level, associated, researchfield))
    conn.commit()
    conn.close()
