# Neccessary libraries ________________________________________________________________
import streamlit as st  # For creating a website
import requests # For sending requests to API server of the stability.ai
import base64   # for decode the generated image
from PIL import Image   # for open the image
from io import BytesIO  # for working with binary data of the image

# Choose API endpoint and insert the API key of the Stability AI __________________________________
# API_ENDPOINT: the location to the service of the Stability.AI API server
# API_KEY: for getting the authority for using the server of the API server
API_ENDPOINT = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
API_KEY="your API key"


# The Website ________________________________________________________________

# Website's title
st.title("Text to Image Generator")

# Getting input prompt
text_prompts = st.text_area("Enter text prompts (one per line):", height=200)

# Function to generate and download image
def generate_and_save_images():

    """
        This function will send request to the API server using the post request(prompt and information about the image that we want) and then receive the response(information about the generated images) from the API server.
        And we can download the generated images
    """

    # Split the prompts by newlines
    prompts = text_prompts.split("\n")


    # AI Model's' parameters:
    # steps: number of times that the model should take, the larger the higher quality
    # width and height: the dimension of the generated image
    # seed: the number that control the randomness of the generated image (if you input one prompt again then you will get the same image)
    # samples: number of images to be generated
    # cfg_scale: a number that tell the model, how much accuracy that you the output image to be closed to your prompt

    # The body is the request that will be sent to the API server and ask the server to do as the request
    body = {
        "steps": 50,
        "width": 1024,
        "height": 1024,
        "seed": 0,
        "cfg_scale": 7,
        "samples": 1,
        # remove any white spaces
        "text_prompts": [{"text": prompt, "weight": 1} for prompt in prompts if prompt.strip()],
    }

    # Define headers for the API request package
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    # Process of sending the request to the API servern and decode the response that has our generated image into normal image that we want to see
    try:
        # Send the request to the Stability AI and store in the response when the server sends back the requested data
        response = requests.post(API_ENDPOINT, headers=headers, json=body)

        # Check the status code if it is 200 then everything is fine
        if response.status_code == 200:
            # Get the response that sent back from the API server as JSON format
            response_json = response.json()

            # Decoding the generated image from the response
            # The response_json["artifacts"] contains the image data 
            for index, image_data in enumerate(response_json["artifacts"]):
                # The image data is encoded in base64
                # We have to decode the data back to binary data for the next function to be able to open the image
                image_bytes = base64.b64decode(image_data["base64"])
                # Open the image
                image = Image.open(BytesIO(image_bytes))
                # Show the generated image on the website
                st.image(image, caption=f"Generated Image {index + 1}", use_column_width=True)

                # Download the image
                filename = f"generated_image_{index + 1}.png"

                # Create download button
                st.download_button(
                    label=f"Download Image {index + 1}",
                    data=image_bytes,
                    key=f"download_button_{index}",
                    file_name=filename,
                )
        else:
            # ERROR message
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        # ERROR message
        st.error(f"Error: {str(e)}")

# Generate images when the "generate image" button on the website is clicked
if st.button("Generate Images"):
    generate_and_save_images()

