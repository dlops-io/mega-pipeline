"""
Module that contains the command line app.
"""
import os
import io
import argparse
import shutil
from google.cloud import storage
from transformers import GPT2Tokenizer, TFGPT2LMHeadModel, GPT2Config

# Generate the inputs arguments parser
parser = argparse.ArgumentParser(description="Command description.")

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_prompts = "text_prompts"
text_paragraphs = "text_paragraphs"


def makedirs():
    os.makedirs(text_paragraphs, exist_ok=True)
    os.makedirs(text_prompts, exist_ok=True)


def download():
    print("download")

    # Clear
    shutil.rmtree(text_prompts, ignore_errors=True, onerror=None)
    makedirs()

    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=text_prompts + "/")
    for blob in blobs:
        print(blob.name)
        if blob.name.endswith(".txt"):
            blob.download_to_filename(blob.name)


def generate():
    print("generate")
    makedirs()

    # Tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    # Model - Load pretrained GPT Language Model
    model = TFGPT2LMHeadModel.from_pretrained(
        "gpt2", pad_token_id=tokenizer.eos_token_id
    )

    # Get the list of text file
    text_files = os.listdir(text_prompts)

    for text_file in text_files:
        uuid = text_file.replace(".txt", "")
        file_path = os.path.join(text_prompts, text_file)
        paragraph_file = os.path.join(text_paragraphs, uuid + ".txt")

        if os.path.exists(paragraph_file):
            continue

        with open(file_path) as f:
            input_text = f.read()

        # Tokenize Input
        input_ids = tokenizer.encode(input_text, return_tensors="tf")
        print("input_ids", input_ids)

        # Generate output
        # outputs = model.generate(
        #     input_ids,
        #     do_sample=True,
        #     max_length=100,
        #     top_k=50
        # )
        # paragraph = tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Generate output
        outputs = model.generate(
            input_ids, max_length=50, num_beams=3, early_stopping=False
        )
        paragraph = tokenizer.decode(outputs[0], skip_special_tokens=True)

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
    text_files = os.listdir(text_paragraphs)

    for text_file in text_files:
        file_path = os.path.join(text_paragraphs, text_file)

        destination_blob_name = file_path
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(file_path)


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
