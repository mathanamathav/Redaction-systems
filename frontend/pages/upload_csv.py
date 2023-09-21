import streamlit as st
import pandas as pd
import io
import requests

# Set the page title
st.set_page_config(page_title="CSV Redaction", page_icon="🔒")

# Define the API endpoint
API_ENDPOINT = ""

# Streamlit layout styling
st.markdown(
    """
    <style>
    .stApp {
        max-width: 100%;
        padding: 1rem;
    }
    .stButton>button {
        background-color: #008B8B;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit app title
st.title("Redaction CSV")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)

    # Display the original data
    st.write("Original CSV data:")
    st.write(df)

    # Modify the CSV data (example: add 1 to all values)
    df["simple"] = 1
    modified_df = df

    # Display the modified data
    st.write("Modified CSV data:")
    st.write(modified_df)

    # Download the modified CSV file
    csv_file = modified_df.to_csv(index=False).encode()
    st.download_button(
        label="Download Modified CSV",
        data=csv_file,
        file_name="modified_csv.csv",
        key="download_button",
    )
