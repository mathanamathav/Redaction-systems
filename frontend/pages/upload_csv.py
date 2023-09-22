import streamlit as st
import pandas as pd
import io
import requests

st.set_page_config(page_title="CSV Redaction", page_icon="🔒" , layout="wide")

# Define the API endpoint
API_ENDPOINT = "http://127.0.0.1:8000/batch_text"
CHUNCK_SIZE = 100

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
    df = pd.read_csv(uploaded_file , header=None , names = ["Text"])
    df.reset_index(inplace=True,drop=True)

    st.write("Original CSV data:")
    st.dataframe(df , use_container_width=True)

    input = df["Text"].to_list()

    modified_text, mappings, modified_text_read, mappings_read  = [] , [] , [] , [] 

    for i in range(0 , len(input) , CHUNCK_SIZE):

        data = input[i:i+CHUNCK_SIZE]
        response = requests.post(
                API_ENDPOINT, json={"text_input": data})
        
        if response.status_code == 200:
            response = response.json()
            print( response )
            modified_text.extend(response.get("data"))
            mappings.extend(response.get("mappings"))
            modified_text_read.extend(response.get("read_data"))
            mappings_read.extend(response.get("read_mappings"))
    
    df["Modified Text"] = modified_text
    df["Mapping"] = mappings
    df["Modified Text Readability"] = modified_text_read
    df["Mapping Readability"] = mappings_read

    st.write("Modified CSV data:")
    st.dataframe(df , use_container_width=True)

    # Download the modified CSV file
    csv_file = df.to_csv(index=False).encode()
    st.download_button(
        label="Download Modified CSV",
        data=csv_file,
        file_name="modified_csv.csv",
        key="download_button",
    )