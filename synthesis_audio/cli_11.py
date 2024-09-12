"""
Module that contains the command line app.
"""
import os
import argparse
import shutil
import glob
import requests
from google.cloud import storage

# Generate the inputs arguments parser

parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_translated = "text_translated"
output_audios = "output_audios_pp"
group_name = "pavlos" # This needs to be your Group name e.g: group-01, group-02, group-03, group-04, group-05, ...

# Define constants

CHUNK_SIZE = 1024

# Pavlos Voice id


VOICE_ID = "TG3keNw5JZvsEiTtWt7t"
#Define the path to the secrets file
secrets_file_path = 'secrets/11lab_api_key.txt'

# Read the file and set the environment variable
with open(secrets_file_path) as f:
    for line in f:
        if 'XI_API_KEY' in line:
            key, value = line.strip().split('=')
            os.environ[key] = value

XI_API_KEY = os.environ['XI_API_KEY']  

def makedirs():
    os.makedirs(os.path.join(text_translated,group_name), exist_ok=True)
    os.makedirs(os.path.join(output_audios,group_name), exist_ok=True)


def download():
    print("download")

    # Clear
    shutil.rmtree(text_translated, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(match_glob=f"{text_translated}/{group_name}/input-*.txt")
    for blob in blobs:
        blob.download_to_filename(blob.name)


def synthesis():
    print("synthesis")
    makedirs()

    # Get the list of text file
    text_files = glob.glob(os.path.join(text_translated, group_name, "input-*.txt"))
    for text_file in text_files:
        uuid = os.path.basename(text_file).replace(".txt", "")
        audio_file = os.path.join(output_audios, group_name, uuid + ".mp3")
    
        if os.path.exists(audio_file):
            continue
        
        with open(text_file) as f:
            TEXT_TO_SPEAK = f.read()
    
        OUTPUT_PATH = audio_file
    
        # Construct the URL for the Text-to-Speech API request
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    
        # Set up headers for the API request, including the API key for authentication
        headers = {
            "Accept": "application/json",
            "xi-api-key": XI_API_KEY
        }
    
        # Set up the data payload for the API request, including the text and voice settings
        data = {
            "text": TEXT_TO_SPEAK,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8,
                "style": 0.0,
                "use_speaker_boost": True
            }
        }
    
        # Make the POST request to the TTS API with headers and data, enabling streaming response
        response = requests.post(tts_url, headers=headers, json=data, stream=True)
    
        # Check if the request was successful
        if response.ok:
            # Open the output file in write-binary mode
            with open(OUTPUT_PATH, "wb") as f:
                # Read the response in chunks and write to the file
                for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                    f.write(chunk)
            # Inform the user of success
            print("Audio stream saved successfully.")
        else:
            # Print the error message if the request was not successful
            print(response.text)

     

def upload():
    print("upload")
    makedirs()

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of text file
    audio_files = glob.glob(os.path.join(output_audios, group_name, "input-*.mp3"))

    for audio_file in audio_files:
        filename = os.path.basename(audio_file)
        destination_blob_name = os.path.join(output_audios, group_name, filename)
        blob = bucket.blob(destination_blob_name)
        print("Uploading:",destination_blob_name, audio_file)
        blob.upload_from_filename(audio_file)


def main(args=None):
    print("Args:", args)

    if args.download:
        download()
    if args.synthesis:
        synthesis()
    if args.upload:
        upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Synthesis Pavlos audio from text")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download paragraph of text from GCS bucket",
    )
    
    parser.add_argument(
        "-s", "--synthesis", action="store_true", help="Synthesis audio"
    )
    
    parser.add_argument(
        "-u", "--upload", action="store_true", help="Upload audio file to GCS bucket"
    )
    
    args = parser.parse_args()
    
    main(args)
