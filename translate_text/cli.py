"""
Module that contains the command line app.
"""
import os
import argparse
import shutil
from google.cloud import storage
from googletrans import Translator

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_paragraphs = "text_paragraphs"
text_translated = "text_translated"

translator = Translator()


def makedirs():
    os.makedirs(text_paragraphs, exist_ok=True)
    os.makedirs(text_translated, exist_ok=True)


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


def translate():
    print("translate")
    makedirs()

    # Get the list of text file
    text_files = os.listdir(text_paragraphs)

    for text_file in text_files:
        uuid = text_file.replace(".txt", "")
        file_path = os.path.join(text_paragraphs, text_file)
        translated_file = os.path.join(text_translated, uuid + ".txt")

        if os.path.exists(translated_file):
            continue

        with open(file_path) as f:
            input_text = f.read()

        results = translator.translate(input_text, src="en", dest="fr")

        print(results.text)

        # Save the translation
        with open(translated_file, "w") as f:
            f.write(results.text)


def upload():
    print("upload")
    makedirs()

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of text file
    text_files = os.listdir(text_translated)

    for text_file in text_files:
        file_path = os.path.join(text_translated, text_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)


def main(args=None):
    print("Args:", args)

    if args.download:
        download()
    if args.translate:
        translate()
    if args.upload:
        upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Translate English to French")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download text paragraphs from GCS bucket",
    )

    parser.add_argument("-t", "--translate", action="store_true", help="Translate text")

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload translated text to GCS bucket",
    )

    args = parser.parse_args()

    main(args)
