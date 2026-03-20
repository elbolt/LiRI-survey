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
import os
import json
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials


class _EnvGSheetsConn:
    """Gspread-backed connection built from environment variables (Posit Connect)."""

    def __init__(self):
        creds_info = json.loads(os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"])
        scopes = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        creds = Credentials.from_service_account_info(creds_info, scopes=scopes)
        client = gspread.authorize(creds)
        self._sheet = client.open_by_url(os.environ["GSHEETS_SPREADSHEET"])

    def read(self, worksheet: str, ttl=None) -> pd.DataFrame:
        ws = self._sheet.worksheet(worksheet)
        return pd.DataFrame(ws.get_all_records())

    def update(self, worksheet: str, data: pd.DataFrame):
        ws = self._sheet.worksheet(worksheet)
        ws.clear()
        ws.update([data.columns.tolist()] + data.fillna("").values.tolist())


def get_gsheets_conn():
    if "GOOGLE_SERVICE_ACCOUNT_JSON" in os.environ:
        return _EnvGSheetsConn()
    from streamlit_gsheets import GSheetsConnection
    return st.connection("gsheets", type=GSheetsConnection)

# Load intro text from file
with open("intro.txt", "r", encoding="utf-8") as file:
    intro_text = file.read()

# Load survey configuration from JSON
with open("content.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Display title and intro
st.title("CLARIN-CH & LiRI Online Workshop on Statistical Power Analysis")
st.markdown(intro_text)

# Inject CSS to hide Cmd/Ctrl+Enter hint on all text inputs
st.markdown(
    """
    <style>
    div[data-testid="stTextArea"] div[data-testid="InputInstructions"],
    div[data-testid="stTextInput"] div[data-testid="InputInstructions"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Establish a Google Sheets connection
conn = get_gsheets_conn()

# Fetch existing survey data
existing_data = conn.read(worksheet="Responses", ttl=5)
existing_data = existing_data.dropna(how="all")

# Survey form
with st.form(key="survey_form"):

    # Workshop content
    st.subheader("Workshop content")
    st.caption(config["workshop_content"]["label"])

    workshop_content = []
    for item in config["workshop_content"]["options"]:
        if st.checkbox(item):
            workshop_content.append(item)

    other_goal = st.text_input("Other — please specify", key="other_goal")
    st.markdown(" ")

    if other_goal:
        workshop_content.append(other_goal)

    # Statistical analyses
    st.subheader("Statistical analyses")
    st.caption(config["analysis_types"]["label"])

    analysis_types = []
    for item in config["analysis_types"]["options"]:
        if st.checkbox(item):
            analysis_types.append(item)

    other_analysis = st.text_input("Other — please specify", key="other_analysis")
    st.markdown(" ")

    if other_analysis:
        analysis_types.append(other_analysis)

    # Tool preference
    st.subheader("Tool preference")
    st.caption(config["tools"]["label"])

    tools = []
    for item in config["tools"]["options"]:
        if st.checkbox(item):
            tools.append(item)

    st.markdown(" ")

    # Challenges
    st.subheader("Challenges")
    st.caption("Are there any challenges you've faced with power analysis?")

    struggles = st.text_area("What challenges have you faced?", key="struggles", label_visibility="collapsed")

    st.markdown(" ")

    # Session format
    st.subheader("Session format preference")
    st.caption("Choose the option that best matches your preference for this short workshop.")

    session_format = st.radio(
        "What kind of session would be most useful for you?",
        [
            "A practical, hands-on session with concrete examples and minimal technical theory",
            "A more in-depth technical discussion, focusing on concepts and methods rather than interactive work",
            "A mix of both, if possible",
            "No strong preference"
        ],
        key="session_format"
    )

    st.markdown(" ")

    # Research background
    st.subheader("Research background")
    st.caption(config["background"]["label"])

    background = st.multiselect(
        "Select your research area(s)",
        config["background"]["options"]
    )

    other_background = st.text_input("Other — please specify", key="other_background")

    # Add manually specified 'Other' entry if selected
    if "Other" in background and other_background:
        background = [rb for rb in background if rb != "Other"]
        background.append(other_background)
        st.markdown(" ")

    # Takeaways
    st.subheader("Takeaways")
    st.caption("What would you like to take away from this workshop?")

    takeaways = st.text_area("Your key takeaways", key="takeaways", label_visibility="collapsed")

    st.markdown(" ")

    # Additional comments
    st.subheader("Additional comments")
    st.caption("Anything else you'd like to include or suggest?")

    comments = st.text_area("Anything else?", key="comments", label_visibility="collapsed")

    st.markdown(" ")

    # Submit form
    submit_button = st.form_submit_button(label="Submit")

    if submit_button:
        if not workshop_content:
            st.warning("Please select at least one topic.")
            st.stop()

        new_response = pd.DataFrame([{
            "content": ", ".join(workshop_content),
            "analyses": ", ".join(analysis_types),
            "tools": ", ".join(tools),
            "struggles": struggles,
            "format": session_format,
            "background": background,
            "takeaways": takeaways,
            "comments": comments
        }])

        updated_df = pd.concat([existing_data, new_response], ignore_index=True)
        conn.update(worksheet="Responses", data=updated_df)

        st.success("Your response has been recorded! Thank you.")
