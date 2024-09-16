"""
Module that contains the command line app.
"""
import os
import io
import argparse
import shutil
import glob
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_prompts = "text_prompts"  # THIS IS THE TRANSCRIBED TEXT 
text_paragraphs = "text_paragraphs" # THIS IS THE LLM GENERATED TEXT
group_name = "" # This needs to be your Group name e.g: group-01, group-02, group-03, group-04, group-05, ...
assert group_name!="", "Update group name"
assert group_name!="pavlos-advanced", "Update group name"
#############################################################################
#                            Initialize the model                           #
vertexai.init(project=gcp_project, location="us-central1")
model = GenerativeModel(model_name="gemini-1.5-flash-001",)
generation_config = GenerationConfig(
    temperature=0.01
)
#############################################################################

def makedirs():
    os.makedirs(os.path.join(text_paragraphs,group_name), exist_ok=True)
    os.makedirs(os.path.join(text_prompts,group_name), exist_ok=True)


def download():
    print("download")

    # Clear
    shutil.rmtree(text_prompts, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=gcp_project)
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(match_glob=f"{text_prompts}/{group_name}/input-*.txt")
    for blob in blobs:
        blob.download_to_filename(blob.name)


def generate():
    print("generate")
    makedirs()

    # Get the list of text file
    text_files = glob.glob(os.path.join(text_prompts, group_name, "input-*.txt"))
    for text_file in text_files:
        uuid = os.path.basename(text_file).replace(".txt", "")
        paragraph_file = os.path.join(text_paragraphs, group_name, uuid + ".txt")

        if os.path.exists(paragraph_file):
            continue

        with open(text_file) as f:
            input_text = f.read()


        # Generate output
        input_prompt = f"""
            Create a transcript for the podcast about cheese with 1000 or more words.
            Use the below text as a starting point for the cheese podcast.
            Output the transcript as paragraphs and not with who is talking or any "Sound" or any other extra information.
            Do not highlight or make words bold.
            The host's name is Pavlos Protopapas.
            {input_text}
        """
        print(input_prompt,"\n\n\n")
        response = model.generate_content(input_prompt,generation_config=generation_config)
        paragraph = response.text


        print("Generated text:")
        print(paragraph)

        # Save the transcription
        with open(paragraph_file, "w") as f:
            f.write(paragraph)


def upload():
    print("upload")
    makedirs()

    # Upload to bucket
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Get the list of text file
    text_files = glob.glob(os.path.join(text_paragraphs, group_name, "input-*.txt"))

    for text_file in text_files:
        filename = os.path.basename(text_file)
        destination_blob_name = os.path.join(text_paragraphs, group_name, filename)
        blob = bucket.blob(destination_blob_name)
        print("Uploading:",destination_blob_name, text_file)
        blob.upload_from_filename(text_file)


def main(args=None):
    print("Args:", args)

    if args.download:
        download()
    if args.generate:
        generate()
    if args.upload:
        upload()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Generate text from prompt")

    parser.add_argument(
        "-d",
        "--download",
        action="store_true",
        help="Download text prompts from GCS bucket",
    )

    parser.add_argument(
        "-g", "--generate", action="store_true", help="Generate a text paragraph"
    )

    parser.add_argument(
        "-u",
        "--upload",
        action="store_true",
        help="Upload paragraph text to GCS bucket",
    )

    args = parser.parse_args()

    main(args)
