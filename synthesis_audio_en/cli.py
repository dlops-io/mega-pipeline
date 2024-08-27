"""
Module that contains the command line app.
"""
import os
import argparse
import shutil
from google.cloud import storage
from google.cloud import texttospeech

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_paragraphs = "text_paragraphs"
text_audios = "text_audios"

# Instantiates a client
client = texttospeech.TextToSpeechClient()


def makedirs():
    os.makedirs(text_paragraphs, exist_ok=True)
    os.makedirs(text_audios, exist_ok=True)


def download():
    print("download")

    # Clear
    shutil.rmtree(text_paragraphs, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=text_paragraphs + "/")
    for blob in blobs:
        print(blob.name)
        if blob.name.endswith(".txt"):
            blob.download_to_filename(blob.name)


def synthesis():
    print("synthesis")
    makedirs()

    language_code = "en-US"

    # Get the list of text file
    text_files = os.listdir(text_paragraphs)

    for text_file in text_files:
        uuid = text_file.replace(".txt", "")
        file_path = os.path.join(text_paragraphs, text_file)
        audio_file = os.path.join(text_audios, uuid + ".mp3")

        if os.path.exists(audio_file):
            continue

        with open(file_path) as f:
            input_text = f.read()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=input_text)

        # Build the voice request, select the language code ("en-US") and the ssml
        # voice gender ("neutral")
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected
        # voice parameters and audio file type
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the audio file
        with open(audio_file, "wb") as out:
            # Write the response to the output file.
            out.write(response.audio_content)


def upload():
    print("upload")
    makedirs()

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of files
    audio_files = os.listdir(text_audios)

    for audio_file in audio_files:
        file_path = os.path.join(text_audios, audio_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)


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
    parser = argparse.ArgumentParser(description="Synthesis audio from text")

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
