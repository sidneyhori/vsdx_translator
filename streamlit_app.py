import streamlit as st
from google.oauth2 import service_account
from google.cloud import translate_v2 as translate
import tempfile
import base64
from vsdx import VisioFile

# Language options for translation
language_options = {
    "Spanish": "es",
    "Portuguese": "pt",
    "French": "fr",
    "German": "de",
    "Chinese (Simplified)": "zh-CN",
    "Korean": "ko",
    # Add more languages as needed
}

# Function to create a download link
def create_download_link(data, filename):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

# Function to perform text translation
def translate_text(client, text, target_language='es'):
    result = client.translate(text, target_language=target_language)
    return result['translatedText']

# Function to authenticate with GCP and get the translate client
def authenticate_and_get_client(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", suffix='.json') as fp:
        fp.write(uploaded_file.getvalue().decode("utf-8"))
        credentials_path = fp.name
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = translate.Client(credentials=credentials)
    return client

def main():
    st.title("VSDX Translator - Multi files")
    st.subheader("This version allows you to translate VSDX files into multiple languages.")
    
    # Language selection
    target_language = st.selectbox("Choose the language to translate to:", list(language_options.keys()))
    target_language_code = language_options[target_language]

    uploaded_file = st.file_uploader("Upload Google Cloud Service Account JSON", type=["json"])

    if uploaded_file is not None:
        client = authenticate_and_get_client(uploaded_file)
        st.success("Authentication successful. Please select the files you wish to translate.")
        
        uploaded_files = st.file_uploader("Select .VSDX files", accept_multiple_files=True)
        
        if uploaded_files:
            process_files(client, uploaded_files, target_language_code, target_language)

            st.success("Please refresh the page to restart the app and translate more files.")

# Function to process uploaded VSDX files
def process_files(client, uploaded_files, target_language_code, target_language):
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            filename = tmp_file.name

        total_word_count = 0
        with VisioFile(filename) as visio:
            for page in visio.pages:
                for shape in page.all_shapes:
                    if shape.text:
                        total_word_count += len(shape.text.split())

        st.info(f'Translating {uploaded_file.name} to {target_language}: {total_word_count} words to be translated. Please wait...')

        my_bar = st.progress(0)

        word_count = 0
        with VisioFile(filename) as visio:
            for page in visio.pages:
                for shape in page.all_shapes:
                    if shape.text:
                        shape.text = translate_text(client, shape.text, target_language_code)
                        word_count += len(shape.text.split())
                        percent_complete = int(word_count / total_word_count * 100)
                        percent_complete = min(percent_complete, 99)
                        my_bar.progress(percent_complete)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as translated_file:
                visio.save_vsdx(translated_file.name)
                translated_filename = translated_file.name
        
        st.success(f'File {uploaded_file.name} translated to {target_language}! Click the link below to download it.')

        with open(translated_filename, "rb") as file:
            translated_data = file.read()        
        st.markdown(create_download_link(translated_data, translate_text(client, uploaded_file.name, target_language_code)), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
