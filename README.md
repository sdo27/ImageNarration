# Description #
The Image Narration application is a Python-based GUI tool that allows users to input an image URL and generate a detailed story based on the image's features. It utilizes Google Vision API for image analysis and OpenAI GPT-4 for story generation and question answering.

# Features #
Load an image from a URL and display it in the GUI.
Analyze the image to detect landmarks, objects, text, logos, and dominant colors.
Generate a story based on the detected features using OpenAI GPT-4.
Ask questions about the generated story and receive answers using OpenAI GPT-4.
# Prerequisites #
- Python 3.10
- Tkinter for GUI
- PIL (Pillow) for image handling
- Requests for HTTP requests
- Google Cloud Vision API client library
- OpenAI API client library
- Webcolors for color name conversion
- Geocoder for reverse geocoding
# Installation #
Install the required Python packages:
pip install tkinter pillow requests google-cloud-vision pandas openai webcolors geocoder

# APIs #
Set up Google Cloud Vision API:
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/SAT.json"

Create a Google Cloud project and enable the Vision API.
Download the service account key file and set the environment variable:
export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/SAT.json"

Set up OpenAI API:
Obtain an OpenAI API key and set the environment variable:
export OPENAI_API_KEY="your_openai_api_key"

# Execution #
Run the application:
python image_viewer.py

Enter the image URL in the provided entry field and click "Submit".

The image will be displayed, and a story based on the image features will be generated and displayed below the image.

To ask a question about the generated story, enter your question in the provided entry field and click "Enter Question".

The answer to your question will be displayed below the question entry field.

# Code Structure # 
- encode_image(image_path): Encodes the image from the provided URL to base64 format.
- detect_properties(image): Detects dominant colors in the image.
- get_location_name(latitude, longitude): Gets location name from latitude and longitude using reverse geocoding.
- detect_landmarks(image): Detects landmarks in the image.
- detect_text(image): Detects text in the image.
- detect_logo(image): Detects logos in the image.
- multiple_object(image): Detects multiple objects in the image.
- generate_description(image, url): Generates a story based on the image features.
- ask_questions(story, question): Answers questions about the generated story.
- submit_url(): Fetches the image from the URL and generates the story.
- prompt_questions(): Prompts questions about the story and displays the answer.


# Notes #
Ensure the correct paths for the service account key file and API keys are set.
The GUI window size and layout can be adjusted as needed.

# License #
This project is licensed under the MIT License.
