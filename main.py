# Description: This file contains the main code for the Streamlit app.
# import the necessary libraries
import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv
from database import Database

# Load environment variables
load_dotenv()

# Initialize the GROQ client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)

# Load the list of categories from a file
with open(file="categories.txt", mode="r") as file:
    category_list = file.read().splitlines()
    category_list = ", ".join(category_list)


def categorize_case(case_description):
    """Categorize the case into one of the predefined categories."""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Strictly Categorize the case into one of the following categories: {category_list}. Only respond with category.",
            },
            {
                "role": "user",
                "content": f"Case descripiton: {case_description}",
            },
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


def summarize_case(case_description):
    """Summarize the case into a few sentences."""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Act as a case summariser and summarize the case precisely. Provide a brief summary of the case in a few sentences. Only respond with the summary.",
            },
            {
                "role": "user",
                "content": f"Case descripiton: {case_description}",
            },
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


def analyze_case(case_description):
    """Analyze the case and extract key entities and sentiments."""
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": f"Act as a case analyser and analyse the case precisely. Extract key entities and sentiments and Only respond with it.",
            },
            {
                "role": "user",
                "content": f"Case descripiton: {case_description}",
            },
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# Create a new instance of the Database class
db = Database()
db.create_table()

# Streamlit app
st.title("Case Management System")

# Input form for new case description
st.header("Input New Case Description")
with st.form(key='case_form'):
    case_description = st.text_area("Case Description")
    submit_button = st.form_submit_button(label='Submit')

    if submit_button and case_description:
        # Categorize, summarize, and analyze the case
        category = categorize_case(case_description)
        summary = summarize_case(case_description)
        analysis = analyze_case(case_description)

        # Store case details
        case = {
            "description": case_description,
            "category": category,
            "summary": summary,
            "analysis": analysis
        }
        db.add_case(case_description, category, summary, analysis)
        # cases.append(case)

        st.success("Case added successfully!")

# Display all cases
cases = db.get_all_cases()

st.header("All Cases")
for index, case in enumerate(cases):
    id, description, category, summary, analysis = case

    st.subheader(f"Case {index + 1}")
    st.write(f"**Description:** {description}")
    st.write(f"**Category:** {category}")
    st.write(f"**Summary:** {summary}")
    st.write(f"**Analysis:** {analysis}")


    # Add a button to delete the case
    if st.button(f"Delete Case {index + 1}"):
        db.delete_case(id)
        st.success(f"Case {index + 1} deleted successfully!")
        st.rerun()