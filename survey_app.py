import streamlit as st

# Title of the app
st.title('Simple Survey App')

# Collect user information
name = st.text_input('What is your name?')
age = st.number_input('What is your age?', min_value=0, max_value=120)
feedback = st.text_area('What feedback do you have for us?')

# Submit button
if st.button('Submit'):
    # Show confirmation
    st.success(f'Thank you, {name}! Your feedback has been recorded.')
    # Save data to a file (append mode)
    with open('responses.csv', 'a') as f:
        f.write(f'{name},{age},{feedback}\n')