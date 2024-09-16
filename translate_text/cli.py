"""
Module that contains the command line app.
"""
import os
import argparse
import shutil
import glob
from google.cloud import storage
from googletrans import Translator

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_paragraphs = "text_paragraphs"
text_translated = "text_translated"
group_name = "" # This needs to be your Group name e.g: group-01, group-02, group-03, group-04, group-05, ...
assert group_name!="", "Update group name"
assert group_name!="pavlos-advanced", "Update group name"

translator = Translator()


def makedirs():
    os.makedirs(os.path.join(text_paragraphs,group_name), exist_ok=True)
    os.makedirs(os.path.join(text_translated,group_name), exist_ok=True)


def download():
    print("download")

    # Clear
    shutil.rmtree(text_paragraphs, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(match_glob=f"{text_paragraphs}/{group_name}/input-*.txt")
    for blob in blobs:
        blob.download_to_filename(blob.name)


def translate():
    print("translate")
    makedirs()

    # Get the list of text file
    text_files = glob.glob(os.path.join(text_paragraphs, group_name, "input-*.txt"))
    for text_file in text_files:
        uuid = os.path.basename(text_file).replace(".txt", "")
        translated_file = os.path.join(text_translated, group_name, uuid + ".txt")

        if os.path.exists(translated_file):
            continue

        with open(text_file) as f:
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
    text_files = glob.glob(os.path.join(text_translated, group_name, "input-*.txt"))

    for text_file in text_files:
        filename = os.path.basename(text_file)
        destination_blob_name = os.path.join(text_translated, group_name, filename)
        blob = bucket.blob(destination_blob_name)
        print("Uploading:",destination_blob_name, text_file)
        blob.upload_from_filename(text_file)


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
