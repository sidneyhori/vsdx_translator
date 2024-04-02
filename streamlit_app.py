import tempfile
import streamlit as st
from google.cloud import translate_v2 as translate
from vsdx import VisioFile
import os
import base64

# Environment setup
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = secrets.GOOGLE_APPLICATION_CREDENTIALS

# Translation function
def translate_text(text, target_language='es'):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

# Download link function
def create_download_link(data, filename):
    b64 = base64.b64encode(data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
    return href

# Main app
def main():
    st.title("VSDX Translator - Multi files")
    st.subheader("This version currently translates VSDX files from English to Spanish (LATAM).")
    st.write("Please select the files you wish to translate.")

    # Ensure 'uploader_key' is initialized properly
    uploader_key = st.session_state.get('uploader_key', 0)

    # File uploader with a dynamic key based on 'uploader_key'
    uploaded_files = st.file_uploader("Select .VSDX files", accept_multiple_files=True, key=f"file_uploader_{uploader_key}")

    if uploaded_files:
        process_files(uploaded_files)
        st.info('Please click on Refresh Session buttom above and select new files for more translations.', icon="ℹ️")

# Process uploaded files
def process_files(uploaded_files):
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

        st.info(f'Translating {uploaded_file.name}: {total_word_count} words to be translated. Please wait...', icon="ℹ️")
        
        my_bar = st.progress(0)

        word_count = 0
        with VisioFile(filename) as visio:
            for page in visio.pages:
                for shape in page.all_shapes:
                    if shape.text:
                        shape.text = translate_text(shape.text, 'es')
                        word_count += len(shape.text.split())
                        percent_complete = int(word_count / total_word_count * 100)
                        percent_complete = min(percent_complete, 99)
                        my_bar.progress(percent_complete)

            with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as translated_file:
                visio.save_vsdx(translated_file.name)
                translated_filename = translated_file.name
        
        st.success(f'File {uploaded_file.name} translated! Click the link below to download it.', icon="✅")

        with open(translated_filename, "rb") as file:
            translated_data = file.read()
        st.markdown(create_download_link(translated_data, translate_text(uploaded_file.name, 'es')), unsafe_allow_html=True)

# Button to refresh the session
if st.button('Refresh Session'):
    # Increment or initialize 'uploader_key' in session state to reset the file uploader
    st.session_state['uploader_key'] = st.session_state.get('uploader_key', 0) + 1

main()

# import tempfile
# import streamlit as st
# from google.cloud import translate_v2 as translate
# from vsdx import VisioFile
# import os
# import base64

# """
# # VSDX Translator - Multi files
# This version currently translates VSDX files from English to Spanish (LATAM).
# Please select the files you wish to translate.
# """

# # Environment setup
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'smooth-zenith-397515-81d825818ab7.json'

# # Translation function
# def translate_text(text, target_language='es'):
#     translate_client = translate.Client()
#     result = translate_client.translate(text, target_language=target_language)
#     return result['translatedText']

# # Download link function
# def create_download_link(data, filename):
#     b64 = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
#     return href

# # File uploader modified to accept multiple files
# uploaded_files = st.file_uploader("Select .VSDX files", accept_multiple_files=True)

# if uploaded_files:
#     for uploaded_file in uploaded_files:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             filename = tmp_file.name

#         # Initialize word count for progress calculation
#         total_word_count = 0
#         with VisioFile(filename) as visio:
#             for page in visio.pages:
#                 for shape in page.all_shapes:
#                     if shape.text:
#                         total_word_count += len(shape.text.split())

#         # Display information about translation progress
#         st.info(f'Translating {uploaded_file.name}: {total_word_count} words to be translated. Please wait...', icon="ℹ️")
        
#         my_bar = st.progress(0)

#         word_count = 0
#         with VisioFile(filename) as visio:
#             for page in visio.pages:
#                 for shape in page.all_shapes:
#                     if shape.text:
#                         shape.text = translate_text(shape.text, 'es')
#                         word_count += len(shape.text.split())
#                         percent_complete = int(word_count / total_word_count * 100)
#                         percent_complete = min(percent_complete, 99) # Ensure it does not go over 99%
#                         my_bar.progress(percent_complete)

#             # Save the modified Visio file
#             with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as translated_file:
#                 visio.save_vsdx(translated_file.name)
#                 translated_filename = translated_file.name
        
#         st.success(f'File {uploaded_file.name} translated! Click the link below to download it.', icon="✅")

#         # Provide download link for the translated file
#         with open(translated_filename, "rb") as file:
#             translated_data = file.read()
#         st.markdown(create_download_link(translated_data, translate_text(uploaded_file.name, 'es')), unsafe_allow_html=True)

#     st.info('Select new files above if you want more translations.', icon="ℹ️")

# import tempfile
# import streamlit as st
# from google.cloud import translate_v2 as translate
# from vsdx import VisioFile
# import streamlit.components.v1 as components
# import os
# import base64

# # Make sure to replace 'your-service-account-file.json' with the actual filename of the uploaded key
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'smooth-zenith-397515-81d825818ab7.json'

# """
# # VSDX Translator
# This version currently translates VSDX files from English to Spanish (LATAM).
# Please select the file you wish to translate.
# """

# # Function to translate text using Google Cloud Translation API
# def translate_text(text, target_language='es'):
#     translate_client = translate.Client()
#     result = translate_client.translate(text, target_language=target_language)
#     return result['translatedText']

# # Function to create a download link
# def create_download_link(data, filename):
#     b64 = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
#     return href

# # Upload the VSDX file
# uploaded = st.file_uploader("Upload a .VSDX")

# if uploaded:
#     # Save the uploaded file to a temporary file
#     with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as tmp_file:
#         tmp_file.write(uploaded.getvalue())
#         filename = tmp_file.name

#     # Determine number of words to be translated
#     total_word_count = 0
#     with VisioFile(filename) as visio:
#         for page in visio.pages:
#             for shape in page.all_shapes:
#                 if shape.text:
#                     total_word_count += len(shape.text.split())

#     # Process the Visio file
#     st.info('There are ' + str(total_word_count) + ' words to be translated, please wait...', icon="ℹ️")
    
#     my_bar = st.progress(0, text=None)

#     word_count = 0

#     with VisioFile(filename) as visio:
#         for page in visio.pages:
#             for shape in page.all_shapes:
#                 if shape.text:
#                     #st.write(shape.text)
#                     # Translate the shape's text from English to Spanish
#                     shape.text = translate_text(shape.text, 'es')
#                     #st.write(shape.text)
#                     word_count += len(shape.text.split())
#                     percent_complete = int(word_count / total_word_count * 100)
#                     if percent_complete > 100:
#                         percent_complete = 99
#                     my_bar.progress(percent_complete, text=None)

#         # Save the modified Visio file to a new temporary file
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as translated_file:
#             visio.save_vsdx(translated_file.name)
#             translated_filename = translated_file.name
    
#     st.success('File Translated! Click the link below to download it.', icon="✅")

#     # Read the contents of the translated file
#     with open(translated_filename, "rb") as file:
#         translated_data = file.read()

#     # Automatically download the translated file
#     st.markdown(create_download_link(translated_data, 'Translated_' + uploaded.name), unsafe_allow_html=True)

#     st.info('Select a new file above if you want a new translation.', icon="ℹ️")

# import tempfile
# import streamlit as st
# from google.cloud import translate_v2 as translate
# from vsdx import VisioFile
# import os
# import base64

# # Environment setup
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'smooth-zenith-397515-81d825818ab7.json'

# # Translation function
# def translate_text(text, target_language='es'):
#     translate_client = translate.Client()
#     result = translate_client.translate(text, target_language=target_language)
#     return result['translatedText']

# # Download link function
# def create_download_link(data, filename):
#     b64 = base64.b64encode(data).decode()
#     href = f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'
#     return href

# # Main app
# def main():
#     st.title("VSDX Translator - Multi files")
#     st.subheader("This version currently translates VSDX files from English to Spanish (LATAM).")
#     st.write("Please select the files you wish to translate.")

#     uploaded_files = st.file_uploader("Select .VSDX files", accept_multiple_files=True, key="file_uploader")

#     if uploaded_files:
#         process_files(uploaded_files)

#         st.info('Select new files above if you want more translations.', icon="ℹ️")

# # Process uploaded files
# def process_files(uploaded_files):
#     for uploaded_file in uploaded_files:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as tmp_file:
#             tmp_file.write(uploaded_file.getvalue())
#             filename = tmp_file.name

#         total_word_count = 0
#         with VisioFile(filename) as visio:
#             for page in visio.pages:
#                 for shape in page.all_shapes:
#                     if shape.text:
#                         total_word_count += len(shape.text.split())

#         st.info(f'Translating {uploaded_file.name}: {total_word_count} words to be translated. Please wait...', icon="ℹ️")
        
#         my_bar = st.progress(0)

#         word_count = 0
#         with VisioFile(filename) as visio:
#             for page in visio.pages:
#                 for shape in page.all_shapes:
#                     if shape.text:
#                         shape.text = translate_text(shape.text, 'es')
#                         word_count += len(shape.text.split())
#                         percent_complete = int(word_count / total_word_count * 100)
#                         percent_complete = min(percent_complete, 99)
#                         my_bar.progress(percent_complete)

#             with tempfile.NamedTemporaryFile(delete=False, suffix='.vsdx') as translated_file:
#                 visio.save_vsdx(translated_file.name)
#                 translated_filename = translated_file.name
        
#         st.success(f'File {uploaded_file.name} translated! Click the link below to download it.', icon="✅")

#         with open(translated_filename, "rb") as file:
#             translated_data = file.read()
#         st.markdown(create_download_link(translated_data, translate_text(uploaded_file.name, 'es')), unsafe_allow_html=True)

# if st.button('Refresh Session'):
#     # Clear the session state related to file uploading and processing
#     if 'file_uploader' in st.session_state:
#         del st.session_state['file_uploader']
#     # Rerun the app to reset the state
#     st.experimental_rerun()

# main()
