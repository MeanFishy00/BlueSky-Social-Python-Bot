"""
Automated API Interaction and Task Scheduler

This script uses the Atproto client to post text and images fetched from external APIs
to a platform. It includes a task scheduler to automate these tasks.

Features:
- Text posting with content fetched from a specified API.
- Image posting with images fetched and saved temporarily.
- Secure credential handling using environment variables.
- Logging for debugging and tracking activity.
- Task scheduling for periodic execution.

Dependencies:
- atproto
- requests
- schedule
- logging

Setup:
1. Configure API credentials in environment variables: API_USERNAME, API_PASSWORD.
2. Replace placeholder URLs (<YOUR_API_URL>, <IMAGE_API_URL>) with actual endpoints.
3. Install required Python packages: `pip install atproto requests schedule`.
"""

from atproto import Client  # Import the Client class to interact with the API
import requests  # Import the requests library to handle HTTP requests
import os  # Import os to access environment variables for secure credential handling
import json  # Import json to parse JSON responses
import schedule  # Import schedule to schedule tasks at regular intervals
import time  # Import time to handle delays in the scheduler loop
import logging  # Import logging for better debugging and tracking of events
import tempfile  # Import tempfile for handling temporary files

# Configure the logging system
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler(),  # Also log to the console
    ],
)

# Fetch configuration from environment variables
TEXT_API_URL = os.getenv("TEXT_API_URL", "https://example.com/api/text")
IMAGE_API_URL = os.getenv("IMAGE_API_URL", "https://example.com/api/image")
API_USERNAME = os.getenv("API_USERNAME")
API_PASSWORD = os.getenv("API_PASSWORD")

if not (API_USERNAME and API_PASSWORD):
    logging.error("API_USERNAME and API_PASSWORD must be set as environment variables.")
    exit(1)

# Initialize the API client
client = Client()
client.login(API_USERNAME, API_PASSWORD)

def textPost():
    """
    Fetch data from an API and post the response as text using the client.
    """
    try:
        # Fetch data from the API
        response = fetch_data(TEXT_API_URL)
        
        # If the response is valid, post it as text
        if response:
            post = client.post(text=response.get("text", "Default Text"))  # Use a default text if 'text' is not present in the response
            logging.info(f"Text Posted: {post.uri}")  # Log the success and URI of the post
    except Exception as e:
        logging.error(f"Failed to post text: {e}")

def fetch_data(url: str):
    """
    Fetch JSON data from the specified API endpoint.

    Parameters:
    - url (str): The URL of the API endpoint to fetch data from.

    Returns:
    - dict: Parsed JSON data from the API response, or None if the request fails.
    """
    try:
        # Make an HTTP GET request to the specified URL with a timeout of 10 seconds
        res = requests.get(url, timeout=10)
        
        # Raise an exception if the response code indicates an error (4xx or 5xx)
        res.raise_for_status()
        
        # Parse and return the JSON content of the response
        return res.json()
    except requests.RequestException as e:
        logging.error(f"HTTP Request failed for URL {url}: {e}")
        return None

def imagePost():
    """
    Fetch an image from an API, save it temporarily, and post it with metadata.
    """
    try:
        # Fetch the image content from the API
        res = requests.get(IMAGE_API_URL, stream=True)
        res.raise_for_status()

        # Use a temporary file to save the image
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            temp_file.write(res.content)
            temp_file_path = temp_file.name

        # Open the saved image file in binary mode and post it using the client
        with open(temp_file_path, "rb") as img:
            post = client.send_image(
                text="Daily Cat Picture!",  # Descriptive text for the post
                image=img,  # Image content
                image_alt="A cute cat picture",  # Alternative text for accessibility
            )

        logging.info(f"Image Posted: {post.uri}")
    except Exception as e:
        logging.error(f"Failed to post image: {e}")

def run_scheduler():
    """
    Configure and run the task scheduler.

    This function schedules tasks to run at regular intervals and enters an infinite loop
    to keep the scheduler running.
    """
    # Schedule the textPost function to run every minute
    schedule.every(1).minutes.do(textPost)
    
    # Schedule the imagePost function to run every 2 hours
    schedule.every(2).hours.do(imagePost)
    
    logging.info("Scheduler is running. Press Ctrl+C to stop.")

    # Infinite loop to keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(1)

# Entry point of the script
if __name__ == "__main__":
    run_scheduler()
