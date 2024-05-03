from dotenv import load_dotenv

load_dotenv()  ## load all the environment variables

import streamlit as st
import os ##important for retrieving the environment vars

from PIL import Image
import google.generativeai as genai


genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

##Function to load Gemini pro vision

model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_resposne(input,image,prompt):
    response = model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        ## read the file into bytes
        bytes_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": uploaded_file.type, # get the mime type of uploaded file
                "data":bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")   
##Initialize our streamlit setup

st.set_page_config(page_title="Multi Languag Invoice Extractor")
st.header("Gemini Application")
input = st.text_input("Input prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice...",type=['jpg','jpeg','png'])

image=''
if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image",use_column_width=True)

submit = st.button("Tell me about the invoice")    

input_prompt = """
You are an expert in understanding the invoices. We will upload an image as invoice and you will have to answer any questions based on the uploaded invoice image
"""


# ifsubmit is clicked:
if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_resposne(input_prompt,image_data,input)
    st.subheader("The respionse is: ")
    st.write(response)
    