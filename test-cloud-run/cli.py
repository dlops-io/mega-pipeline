"""
Module that contains the command line app.
"""
import os
import io
import argparse
import shutil
import glob
import google.auth
from google.cloud import storage
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
input_audios = "input_audios"

#############################################################################
#                            Initialize the model                           #
vertexai.init(project=gcp_project, location="us-central1")
model = GenerativeModel(model_name="gemini-1.5-flash-001",)
generation_config = GenerationConfig(
    temperature=0.01
)
#############################################################################


def test_no_auth():
    print("Test No Auth inside container")

    try:
        print("Testing.. current service account")
        credentials, project_id = google.auth.default()

        if hasattr(credentials, "service_account_email"):
            print(credentials.service_account_email)
        else:
            print("WARNING: no service account credential. User account credential?")

    except Exception as e:
        print(f"Error occurred while generating content: {e}")

def test_auth():
    print("Test with Auth inside container")

    try:
        print("Testing.. current service account")
        credentials, project_id = google.auth.default()

        if hasattr(credentials, "service_account_email"):
            print(credentials.service_account_email)
        else:
            print("WARNING: no service account credential. User account credential?")

    except Exception as e:
        print(f"Error occurred while generating content: {e}")
    
    try:
        print("Testing.. AUTH")

        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        blobs = bucket.list_blobs(prefix=input_audios+"/")
        for blob in blobs:
            print(blob.name)

    except Exception as e:
        print(f"Error occurred while generating content: {e}")

def main(args=None):
    print("Args:", args)

    print("GOOGLE_APPLICATION_CREDENTIALS", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

    if args.test_no_auth:
        test_no_auth()
    
    if args.test_auth:
        test_auth()


if __name__ == "__main__":
    # Generate the inputs arguments parser
    # if you type into the terminal 'python cli.py --help', it will provide the description
    parser = argparse.ArgumentParser(description="Generate text from prompt")

    parser.add_argument(
        "--test_no_auth",
        action="store_true",
        help="Test run container",
    )
    parser.add_argument(
        "--test_auth",
        action="store_true",
        help="Test run container",
    )

    args = parser.parse_args()

    main(args)
