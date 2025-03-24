"""
streamlit_app.py

This Streamlit app collects survey responses for a Power analysis workshop hosted by CLARIN-CH and conducted by LiRI.

Features:
- Loads intro text and survey configuration from external files.
- Collects participant preferences, challenges, and research backgrounds.
- Stores responses in a Google Sheets document.

Survey Sections:
1. Workshop Goals
2. Statistical Analyses
3. Tool Preferences
4. Challenges
5. Session Format
6. Research Background
7. Takeaways
8. Additional Comments

Google Sheets Integration:
- Reads and appends survey responses to the "Responses" worksheet.

Usage:
Run with Streamlit, ensuring required files and Google Sheets connection are configured.

"""
import streamlit as st
import pandas as pd
import json
from streamlit_gsheets import GSheetsConnection

# Load intro text from file
with open("intro.txt", "r", encoding="utf-8") as file:
    intro_text = file.read()

# Load survey configuration from JSON
with open("content.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Display title and intro
st.title("Survey: Power analysis workshop")
st.markdown(intro_text)

# Establish a Google Sheets connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Fetch existing survey data
existing_data = conn.read(worksheet="Responses", ttl=5)
existing_data = existing_data.dropna(how="all")

# Survey form
with st.form(key="survey_form"):

    # Workshop content
    st.subheader("Workshop content")
    st.caption(config["workshop_goals"]["label"])

    workshop_goals = []
    for item in config["workshop_goals"]["options"]:
        if st.checkbox(item):
            workshop_goals.append(item)

    other_goal = st.text_input("Other (please specify)", key="other_goal")
    if other_goal:
        workshop_goals.append(other_goal)

    st.markdown(" ")

    # Statistical analyses
    st.subheader("Statistical analyses")
    st.caption(config["analysis_types"]["label"])

    analysis_types = []
    for item in config["analysis_types"]["options"]:
        if st.checkbox(item):
            analysis_types.append(item)

    other_analysis = st.text_input("Other (please specify)", key="other_analysis")
    if other_analysis:
        analysis_types.append(other_analysis)

    st.markdown(" ")

    # Tool preference
    st.subheader("Tool preference")
    st.caption(config["tools_preference"]["label"])

    tools_preference = []
    for item in config["tools_preference"]["options"]:
        if st.checkbox(item):
            tools_preference.append(item)

    st.markdown(" ")

    # Challenges
    st.subheader("Challenges")
    st.caption("Any challenges you've faced with power analysis?")

    struggles = st.text_area("What challenges have you faced?", key="struggles", label_visibility="collapsed")

    st.markdown(" ")

    # Session format
    st.subheader("Session format preference")
    st.caption("Choose the option that best matches your preference for this short workshop.")

    tech_detail = st.radio(
        "What kind of session would be most useful for you?",
        [
            "A practical, hands-on session with concrete examples and minimal technical theory",
            "A more in-depth technical discussion, focusing on concepts and methods rather than interactive work",
            "A mix of both, if possible",
            "No strong preference"
        ],
        key="tech_detail"
    )

    st.markdown(" ")

    # Research background
    st.subheader("Research background")
    st.caption(config["research_background"]["label"])

    research_background = st.selectbox(
        "Select your primary research area",
        config["research_background"]["options"],
        index=None,
        placeholder="Choose one"
    )

    other_background = st.text_input("If 'Other', please specify", key="other_background")

    if research_background == "Other":
        research_background = other_background

    st.markdown(" ")

    # Takeaways
    st.subheader("Takeaways")
    st.caption("What would you like to take away from this workshop?")

    takeaways = st.text_area("Your key takeaways", key="takeaways", label_visibility="collapsed")

    st.markdown(" ")

    # Additional comments
    st.subheader("Additional comments")
    st.caption("Anything else you'd like to include or suggest?")

    extra_topics = st.text_area("Anything else?", key="extra_topics", label_visibility="collapsed")

    st.markdown(" ")

    # Submit form
    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not workshop_goals:
            st.warning("Please select at least one topic.")
            st.stop()

        new_response = pd.DataFrame([{
            "workshop_goals": ", ".join(workshop_goals),
            "analysis_types": ", ".join(analysis_types),
            "tools_preference": ", ".join(tools_preference),
            "struggles": struggles,
            "session_format": tech_detail,
            "research_background": research_background,
            "takeaways": takeaways,
            "extra_topics": extra_topics
        }])

        updated_df = pd.concat([existing_data, new_response], ignore_index=True)
        conn.update(worksheet="Responses", data=updated_df)

        st.success("Your response has been recorded! Thank you.")
