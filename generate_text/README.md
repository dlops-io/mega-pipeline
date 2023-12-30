# Generate Text

📝 &rightarrow; 🗒️ 

In this container you will implement the following:
* Read the text prompt from the GCS bucket `mega-pipeline-bucket` and folder `text_prompts`
* Use GPT2 or OpenAI API to generate text (About 100 words)
* Save the paragraph of text as a text file in bucket `mega-pipeline-bucket` and folder `text_paragraphs` (use the same file name)

### Prerequisites for Development
* Have Docker Desktop installed
* Check that your Docker is running with the following command
`docker run hello-world`
### Install VSCode  
Follow the [instructions](https://code.visualstudio.com/download) for your operating system.  
If you already have a preferred text editor, skip this step.  

### Project Setup

* Create a folder `generate_text`

### GCP Credentials File
* Download the `mega-pipeline.json` and save it inside a folder called `secrets` inside `generate_text`
<a href="https://static.us.edusercontent.com/files/fo4cDM3adnwMlJVUXZXtzcH2" download>mega-pipeline.json</a>

### Create Pipfile & Pipfile.lock files
* Add `Pipfile` with a the following contents:
```
[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[dev-packages]

[packages]

[requires]
python_version = "3.8"
```

* Add `Pipfile.lock` with a the following contents:
```
{
    "_meta": {
        "hash": {
            "sha256": "7f7606f08e0544d8d012ef4d097dabdd6df6843a28793eb6551245d4b2db4242"
        },
        "pipfile-spec": 6,
        "requires": {
            "python_version": "3.8"
        },
        "sources": [
            {
                "name": "pypi",
                "url": "https://pypi.org/simple",
                "verify_ssl": true
            }
        ]
    },
    "default": {},
    "develop": {}
}
```

### Create Dockerfile
* Create a `Dockerfile` and base it from `python:3.8-slim-buster` the official Debian-hosted Python 3.8 image
* Set the following environment variables:
```
ENV PYENV_SHELL=/bin/bash
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json
```

* Ensure we have an up to date baseline, install dependencies by running
```
apt-get update
apt-get upgrade -y
apt-get install -y --no-install-recommends build-essential
```

* Install pipenv
```
pip install --no-cache-dir --upgrade pip
pip install pipenv
```
* Create a `app` folder by running `mkdir -p /app`

* Set the working directory as `/app`
* Add `Pipfile`, `Pipfile.lock` to the `/app` folder
* Run `pipenv sync`

* Add the rest of your files to the `/app` folder
* Add Entry point to `/bin/bash`
* Add a command to get into the `pipenv shell`

* Example dockerfile can be found [here](https://github.com/dlops-io/mega-pipeline#sample-dockerfile)

### Docker Build & Run
* Build your docker image and give your image the name `generate_text`

* You should be able to run your docker image by using:
```
docker run --rm -ti -v "$(pwd)":/app generate_text
```
* The `-v "(pwd)":/app` option is to mount your current working directory into the `/app` directory inside the container as a volume. This helps us during development of the app so when you change a source code file using VSCode from your host machine the files are automatically changed inside the container.

### Python packages required
* `pipenv install` the following:
  - `google-cloud-storage`
  - `tensorflow`
  - `transformers`

* If you exit your container at this point, in order to get the latest environment from the pipenv file. Make sure to re-build your docker image again

### CLI to interact with your code
* Add a python file `cli.py`
* The CLI should have the following command line argument options
```
python cli.py --help
usage: cli.py [-h] [-d] [-g] [-u]

Generate text from prompt

optional arguments:
  -h, --help      show this help message and exit
  -d, --download  Download text prompts from GCS bucket
  -g, --generate  Generate a text paragraph
  -u, --upload    Upload paragraph text to GCS bucket
```

* Use this as a starter template for your `cli.py`
```
"""
Module that contains the command line app.
"""
import argparse

def download():
    print("download")

def generate():
    print("generate")

def upload():
    print("upload")

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
    parser = argparse.ArgumentParser(
        description='Generate text from prompt')

    parser.add_argument("-d", "--download", action='store_true',
                        help="Download text prompts from GCS bucket")

    parser.add_argument("-g", "--generate", action='store_true',
                        help="Generate a text paragraph")

    parser.add_argument("-u", "--upload", action='store_true',
                        help="Upload paragraph text to GCS bucket")

    args = parser.parse_args()

    main(args)
```

* Requirements for `cli.py`
Use the following values:
```
gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_prompts = "text_prompts"
text_paragraphs = "text_paragraphs"
```

* `text_prompts` - Bucket where we store the text prompts that was synthesized by audio to text
* `text_paragraphs` - Bucket where we store the generated text from GPT2 or OpenAI API

* -d, --download    Download text prompts from GCS bucket
Write a function to download all text prompts from the bucket `text_prompts` and store them locally in a folder `text_prompts`

* -g, --generate  Generate a text paragraph
Write a function to generate text using the prompt and save the generated text in a local folder `text_paragraphs`
Feel free to the `transformers` package to generate text like we did in th Language Model tutorial

* -u, --upload      Upload paragraph text to GCS bucket
Write a function to upload the files in `text_paragraphs` to the bucket `text_paragraphs` in GCS

* Sample code to read/write to a GCS Bucket can be found [here](https://github.com/dlops-io/mega-pipeline#sample-code-to-readwrite-to-gcs-bucket)

### Testing your code locally
* Inside your docker shell make sure you run the following commands:
* `python cli.py -d` - Should download all the required data from GCS bucket
* `python cli.py -g` - Should generate text using GPT2 or OpenAI API and save it locally
* `python cli.py -u` - Should upload the generated text to the remote GCS bucket
* Verify that your uploaded data shows up in the [Mega Pipeline App](https://ai5-mega-pipeline.dlops.io/)

### OPTIONAL: Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag generate_text <USER NAME>/generate_text`
* Push to Docker Hub: `docker push <USER NAME>/generate_text`
