import streamlit as st
import requests

# Set the page title
st.set_page_config(page_title="Redaction", page_icon="🔒", layout="wide")

# Running it in local server
API_ENDPOINT = "http://127.0.0.1:8000/process_text"

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

st.title("Redaction Text Demo")

text_input = st.text_area("Enter your text:")
agree = st.checkbox("Readability")

if st.button("Run"):
    if text_input:
        try:
            response = requests.post(API_ENDPOINT, json={"text_input": text_input})
            if response.status_code == 200:
                result_text = response.json()
                st.text_area("Output", result_text.get("data", ""))
                st.json(result_text.get("mappings", {}))

                if agree:
                    st.text_area("Readable Output", result_text.get("read_data", ""))
                    st.json(result_text.get("read_mappings", {}))
            else:
                st.error("An error occurred. Please try again later.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


st.markdown("## Example Usage")
st.write("1. Enter text in the input field above and click the run.")
st.write("3. The Redacted text will be displayed below the button.")
