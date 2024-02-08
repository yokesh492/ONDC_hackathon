from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from io import BytesIO
# from dotenv import load_dotenv
from google.cloud import storage
import os
import google.generativeai as genai
import json
import re

# load_dotenv()
genai.configure(api_key="AIzaSyDo3bbDydm0fN9V2es__wTP_QAD7nwDXO0")
#os.environ['GOOGLE_APPLICATION_CREDENTIALS']
client = storage.Client()
bucket_name = 'ondc_hackathonimage'


model = genai.GenerativeModel('gemini-pro-vision')
model2 = genai.GenerativeModel('gemini-pro')
prompt = """
    you are an expert ecommerce seller who is about to digitalize the catalogue , 
    from the given image extract the data such as 
    {
    name: name of the product,
    description: write the description for less than 30 words of the product dont leave empty,
    price: price of the product if its mention in image else give leave empty,
    category: top 3 category from this   
    - Diary Products 
  - Meat 
  - Fish and seafoods 
  - Fruits and Nuts 
  - Veggies 
  - Bread & Creals 
  - Oil & Fats 
  - Sauce & Spice 
  - Convenience Food (Ready to eat foods) 
  - Baby Food 
  - Pet Food 
  - Beverages 
  - Detergents 
  - Toiletries ,
    varients : {
    size : size of the product if size in mention in image else empty.
    }
    }
    give output in this json format.
    Do not use markdown.
"""


async def get_gemini_response(image_data):

    response = model.generate_content([ image_data[0], prompt])
    #response = json.dump(response.text)
    # print(eval(response.text.replace('json','')))
    print(response.text)
    text = response.text.replace('json','')
    print(text)
    text = eval(text.replace('`',''))
    # print(text)
    return text

def process_image(uploaded_file: UploadFile):
    if uploaded_file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Unsupported image format")
    uploaded_file.file.seek(0)
    image_content = uploaded_file.file.read()
    #print("################################################################",image_content)
    if not image_content:
        raise HTTPException(status_code=400, detail="Empty image content")

    #image = Image.open(BytesIO(uploaded_file.file.read()))
    return  image_content


async def get_gemini_text(input_text):
    prompt = f"""
    you are an expert ecommerce seller who is about to digitalize the catalogue , 
    from the given product summary 
    {input_text}  extract the data such as name , description based on retrive product name , category , price if mention in summary if null then empty string ,varients such as color ,size if it mention.
    if product summary does not contain enough information to extract the requested data fields. just give output , give empty string.
    give output in this json format.
     """
    response = model2.generate_content(prompt)
    print(response.text)
    text = response.text.replace('json','')
    print(text)
    text = eval(text.replace('`',''))
    return text

async def upload_image_to_gcs(uploaded_file: UploadFile):
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(uploaded_file.filename)
    blob.upload_from_file(uploaded_file.file)
    image_url = f'https://storage.googleapis.com/{bucket_name}/{blob.name}'
    image_url = blob.public_url
    return  image_url
