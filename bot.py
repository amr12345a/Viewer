import requests
import datetime
import sounddevice
import librosa
import time
from telethon.sync import TelegramClient

# List of keywords to search for in project descriptions
keywords = ["scraping", "crypto", "trading", "api", "scrape", "automation", "bot", "meta trader", "meta", "forex",
            "data", "web scraping", "web", "python", "data scraping", "data", "data mining", "mining",
            "data extraction", "extraction", "data collection", "collection", "data analysis", "analysis",
            "data processing", "processing", "data entry", "entry"]

# List to store already saved project URLs
saved_projects = []

# Telegram client configuration
client = TelegramClient("", 0, "")
# Freelancer.com Token
token = ""
client.start()

while True:
    for keyword in keywords:
        try:
            # Make a request to the Freelancer API to get active projects matching the keyword
            response = requests.get("https://www.freelancer.com/api/projects/0.1/projects/active/?compact=&limit=3&project_types%5B%5D=fixed&query=" + keyword,
                                    headers={"freelancer-oauth-v1": token}).json()
            projects = response["result"]["projects"]

            for project in projects:
                project_url = project["seo_url"]

                # Check if the project was recently updated and not already saved
                if abs(datetime.datetime.timestamp(datetime.datetime.now()) - project["time_updated"]) < 1000 and project_url not in saved_projects:
                    # Load and play audio file
                    audio, sr = librosa.load('m.wav')
                    sounddevice.play(audio, sr)

                    # Save the project URL and send it to a Telegram chat
                    saved_projects.append(project_url)
                    client.send_message(1835031012, "https://www.freelancer.com/projects/" + project_url)

            time.sleep(30)  # Wait for 30 seconds before making the next request
        except Exception as e:
            print(e)
            time.sleep(120)  # Wait for 2 minutes before retrying

    time.sleep(60)  # Wait for 1 minute before starting the next iteration
