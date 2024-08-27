"""
Module that contains the command line app.
"""
import os
import io
import argparse
import shutil
from google.cloud import storage
from google.cloud import speech
import ffmpeg
from tempfile import TemporaryDirectory

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
input_audios = "input_audios"
text_prompts = "text_prompts"


def makedirs():
    os.makedirs(input_audios, exist_ok=True)
    os.makedirs(text_prompts, exist_ok=True)


def download():
    print("download")

    # Clear
    shutil.rmtree(input_audios, ignore_errors=True, onerror=None)
    makedirs()

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    # bucket = client.bucket(bucket_name)

    # storage_client = storage.Client(project=gcp_project)
    # bucket = storage_client.bucket(bucket_name)

    # blobs = bucket.list_blobs(prefix=input_audios+"/")
    # for blob in blobs:
    #     print(blob.name)
    #     if not blob.name.endswith("/"):
    #         blob.download_to_filename(blob.name)


def transcribe():
    print("transcribe")
    makedirs()

    # Speech client
    client = speech.SpeechClient()

    # Get the list of audio file
    audio_files = os.listdir(input_audios)

    for audio_path in audio_files:
        uuid = audio_path.replace(".mp3", "")
        audio_path = os.path.join(input_audios, audio_path)
        text_file = os.path.join(text_prompts, uuid + ".txt")

        if os.path.exists(text_file):
            continue

        print("Transcribing:", audio_path)
        with TemporaryDirectory() as audio_dir:
            flac_path = os.path.join(audio_dir, "audio.flac")
            stream = ffmpeg.input(audio_path)
            stream = ffmpeg.output(stream, flac_path)
            ffmpeg.run(stream)

            with io.open(flac_path, "rb") as audio_file:
                content = audio_file.read()

            # Transcribe
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(language_code="en-US")
            operation = client.long_running_recognize(config=config, audio=audio)
            response = operation.result(timeout=90)
            print("response:", response)
            text = "None"
            if len(response.results) > 0:
                text = response.results[0].alternatives[0].transcript
                print(text)

            # Save the transcription
            with open(text_file, "w") as f:
                f.write(text)


def upload():
    print("upload")
    makedirs()

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of text file
    text_files = os.listdir(text_prompts)

    for text_file in text_files:
        file_path = os.path.join(text_prompts, text_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)


def main(args=None):
    print("Args:", args)

    if args.download:
        download()
    if args.transcribe:
        transcribe()
    if args.upload:
        upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Transcribe audio file to text")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download audio files from GCS bucket",
    )

    parser.add_argument(
        "-t", "--transcribe", action="store_true", help="Transcribe audio files to text"
    )

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload transcribed text to GCS bucket",
    )

    args = parser.parse_args()

    main(args)
