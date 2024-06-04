import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO
from CombineAPIs import *
import os, io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import pandas as pd
from openai import AsyncOpenAI
import base64
import requests
import webcolors
import geocoder

os.environ['GOOGLE_APPLICATION_CRDENTIALS'] = "SAT.json"
api_key = os.environ.get('OPENAI_API_KEY')  ##my api key is stored in an environmental variable

def encode_image(image_path):
  try:
        # Fetch the image data from the URL
        response = requests.get(image_path)
        if response.status_code == 200:
            # Encode the image data in base64 format
            content_base64 = base64.b64encode(response.content).decode('utf-8')
            return content_base64
        else:
            print("Failed to fetch image from URL")
            return None
  except Exception as e:
        print(f"An error occurred: {e}")
        return None

#####################################################################################################################################
#####################################################################################################################################
def detect_properties(image):
    response = client.image_properties(image=image)

    dominant_colors = response.image_properties_annotation.dominant_colors.colors

    # Convert RGB values to tuple
    rgb_values = [(color.color.red, color.color.green, color.color.blue) for color in dominant_colors]
    try:
        color_name = webcolors.rgb_to_name(rgb_values, spec='css3')
        print(color_name)
        return color_name
    except:
        print("Hard time deciphering color")
    
######################################################################################################################################
######################################### LANDMARKS ##################################################################################
def get_location_name(latitude, longitude):
    location = geocoder.osm([latitude, longitude], method='reverse', language='en')
    address = location.address if location else None
    return address

def detect_landmarks(image) -> str:
    #do a try catch for every method being used 
    response = client.landmark_detection(image=image)
    landmarks = response.landmark_annotations

    places = []
    for landmark in landmarks:
        places.append(landmark.description)
        for location in landmark.locations:
            lat_lng = location.lat_lng
            lat = lat_lng.latitude
            long = lat_lng.longitude
            break

    if len(places) == 0:
        return "No location"
    else:
        location_name = get_location_name(lat, long)  #order of street address, neighborhood, city, district, region, country, postal code
        location_name = places[0] + ', '+  location_name
        print(location_name)  #order of name, street address, neighborhood, city, district, region, country, postal code
        if response.error.message:
            raise Exception(
                "{}\nFor more info on error messages, check: "
                "https://cloud.google.com/apis/design/errors".format(response.error.message)
                 )
        return location_name
##############################################################################################################################################
##############################################################################################################################################
################################################READING TEXTS OFF AN IMAGE ###################################################################

def detect_text(image) -> str:
    response = client.text_detection(image=image)
    #text_description = response.text_annotations[0].description
    #print(text_description)

    texts = response.text_annotations

    if texts:
        text_description = response.text_annotations[0].description
        return text_description
    else:
        return "No text detected in the image"
    

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
################################################################################################################################################
################################################################################################################################################
################################################################################################################################################    
def detect_logo(image):
    response = client.logo_detection(image=image)
    logos = response.logo_annotations


    if len(logos) == 0:
        print("No applicable logo was found")
        return "No logo was found in the image"
    else:
        logos = (logos[0].description)
        return logos

#################################################################################################################################################
#################################################################################################################################################
#################################################################################################################################################
def multiple_object(image):
    objects = client.object_localization(image=image).localized_object_annotations
    object_list = []
    print(f"Number of objects found: {len(objects)}")
    for object_ in objects:
        object_list.append(object_.name)

    print(object_list)
##################################################################################################################################################
##################################################################################################################################################
##################################################################################################################################################
def generate_description(image, url):
    base64_image = encode_image(url)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }
    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"Make a story based on the image features?"},
                {"type": "text", "text": f"Landmark information from the image in the order: ( name of place, street address #, street address, neighborhood, city, district, region, country, postal code): + {detect_landmarks(image)}"},
                {"type": "text", "text": f"The image contains these objects and descriptions: +  {multiple_object(image)}"},
                {"type": "text", "text": f"Text features in the image: +  {detect_text(image)}"},
                {"type": "text", "text": f"Logos in the image: +  {detect_logo(image)}"},
                {"type": "text", "text": f"Colors in the image: + {detect_properties(image)}"} if detect_properties(image) != "Hard time deciphering color" else {"type": "text", "text": "Hard time deciphering color"},
                ],
        }
    ],
    "max_tokens": 400
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    print(response.json()['choices'][0]['message']['content'])
    print("Story has been made")
    return response.json()['choices'][0]['message']['content']
#############################################################################################################################################################
#############################################################################################################################################################
def ask_questions(story, question):
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
    }
    payload = {
    
    "model": "gpt-4-vision-preview",
    "messages": [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": f"This is the story: {story}"},
                {"type": "text", "text": f"Answer the question: {question}"},
            ],
        }
    ],
    "max_tokens": 300
    }
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    return (response.json()['choices'][0]['message']['content'])

def submit_url():
    url = url_entry.get()
    response = requests.get(url)
    if response.status_code == 200:
            img_data = response.content
            img = Image.open(BytesIO(img_data))
            img.thumbnail((200, 200))  # Resize the image to fit in the GUI
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection

    else:
            print("Failed to fetch image from URL")


    content_base64 = base64.b64encode(response.content).decode('utf-8')
    current_image = vision_v1.Image(content=content_base64)
    # Display the story text below the image
    global story 
    story = generate_description(current_image, url)
    story_label.config(text=story)



def prompt_questions():
    question = question_entry.get()
    answer = ask_questions(question, story)
    question_display.config(text=answer)

# Create a window

client = vision_v1.ImageAnnotatorClient()
story = ""
window = tk.Tk()
window.title("Image Viewer")
window.geometry("1000x400")

# Create a label for instruction
instruction_label = tk.Label(window, text="Enter image URL:")
instruction_label.pack(pady=10)

# Create an entry widget for user input
url_entry = tk.Entry(window, width=50)
url_entry.pack(pady=10)

# Create a button to submit the URL
submit_button = tk.Button(window, text="Submit", command=submit_url)
submit_button.pack(pady=10)

# Create a label to display the image
image_label = tk.Label(window)
image_label.pack(pady=10)
# Create a label to display the story text
story_label = tk.Label(window, text="", wraplength=800, font=('Arial', 13))
story_label.pack(pady=10)

##############################################################################################
##############################################################################################
# Create a label for instruction
instruction_label2 = tk.Label(window, text="Ask a question about the story")
instruction_label2.pack(pady=10)

question_entry = tk.Entry(window, width=70)
question_entry.pack(pady=10)

# Create a button to submit the question
question_button = tk.Button(window, text="Enter Question", command=prompt_questions)
question_button.pack(pady=10)

question_display = tk.Label(window, text="", wraplength=500, font=('Arial', 13))
question_display.pack(pady=10)

window.mainloop()
