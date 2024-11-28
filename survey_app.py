import streamlit as st

# Title of the app
st.title('Survey on Statistical and data science consulting services at LiRI')

# Description
st.write("We are conducting a survey to improve our services. Please help us by providing your feedback.")

# Collect user information
level_options = ["Bachelor", "Master", "PhD", "Postdoc", "other"]
level = st.radio("Please select your current level of study or position:", level_options)

researchfield = st.text_input("What is your field of study?")
if len(researchfield) < 3:
    st.warning("Please enter a valid field of research.")

# Submit button
if st.button("Submit"):
    # Show confirmation
    st.success(f'Thank you for you feedback!')
    # Save data to a file (append mode)
    with open("responses.csv", "a") as f:
        f.write(f'{level},{researchfield}\n')