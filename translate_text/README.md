# Translate Text

🗒️ &rightarrow; 🇫🇷

In this container you will implement the following:
* Read the paragraph of text from the GCS bucket `mega-pipeline-bucket` and folder `text_paragraphs`
* Use `googletrans` to translate the text from English to French
* Save the translated text as a text file in bucket `mega-pipeline-bucket` and folder `text_translated` (use the same file name)

### Prerequisites for Development
* Have Docker Desktop installed
* Check that your Docker is running with the following command
`docker run hello-world`
### Install VSCode  
Follow the [instructions](https://code.visualstudio.com/download) for your operating system.  
If you already have a preferred text editor, skip this step.  

### Project Setup

* Create a folder `translate_text`

### GCP Credentials File
* Download the `mega-pipeline.json` from Ed and save it inside a folder called `secrets` inside `translate_text`

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
* Create a `app` folder by running `mkdir -p /app`

* Set the working directory as `/app`
* Add `Pipfile`, `Pipfile.lock` to the `/app` folder
* Run `pipenv sync`

* Add the rest of your files to the `/app` folder
* Add Entry point to `/bin/bash`
* Add a command to get into the `pipenv shell`


### Docker Build & Run
* You should be able to build your docker image by using:
```
docker build -t translate_text -f Dockerfile .
```
* You should be able to run your docker image by using:
```
docker run --rm -ti --mount type=bind,source=$(pwd),target=/app translate_text
```
* The `--mount type=bind,source=$(pwd)` option is to mount your current working directory into the `/app` directory inside the container. This helps us during development of the app so when you change a source code file using VSCode from your host machine the files are automatically changed inside the container.

### Python packages required
* `pipenv install` the following:
  - `google-cloud-storage`
  - `googletrans==4.0.0rc1`

### CLI to interact with your code
* Add a python file `cli.py`
* The CLI should have the following command line argument options
```
python cli.py --help
usage: cli.py [-h] [-d] [-t] [-u]

Translate English to French

optional arguments:
  -h, --help       show this help message and exit
  -d, --download   Download text paragraphs from GCS bucket
  -t, --translate  Translate text
  -u, --upload     Upload translated text to GCS bucket
```

* Requirements for `cli.py`
Use the following values:
```
gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
text_paragraphs = "text_paragraphs"
text_translated = "text_translated"
```

* `text_paragraphs` - Bucket where we store the generated text from GPT2
* `text_translated` - Bucket where we store the translated text

* -d, --download    Download text prompts from GCS bucket
Write a function to download all text paragraphs from the bucket `text_paragraphs` and store them locally in a folder `text_paragraphs`

* -t, --translate  Translate text
Write a function to translate text from english to french and store in a local folder `text_translated`

* Example code to translation:
```
from googletrans import Translator

translator = Translator()

input_text = "Welcome to AC215"

results = translator.translate(input_text, src="en", dest="fr")

print(results.text)
```

* -u, --upload      Upload paragraph text to GCS bucket
Write a function to upload the files in `text_translated` to the bucket `text_translated` in GCS

### Push Container to Docker Hub
* Sign up in Docker Hub and create an [Access Token](https://hub.docker.com/settings/security)
* Login to the Hub: `docker login -u <USER NAME> -p <ACCESS TOKEN>`
* Tag the Docker Image: `docker tag translate_text <USER NAME>/translate_text`
* Push to Docker Hub: `docker push <USER NAME>/translate_text`
