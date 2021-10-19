# Mega Pipeline App

🎙️ &rightarrow; 📝 &rightarrow; 🗒️ &rightarrow; 🇫🇷 &rightarrow; 🔊

In this tutorial app is to build a Mega  Pipeline App which does the following:

* Allows a user to Record audio using a mic

* The audio file is then transcribed using Google Cloud Speech to Text API

* The text is used as a prompt to a pre-trained GPT2 model to Generate Text (100 words)

* The generated text is synthesized to audio using Google Cloud Text-to-Speech API

* The generated text is also translated to French using googletrans

* The translated text is then synthesized to audio using Google Cloud Text-to-Speech API

### Sample Code to Read/Write to GCS Bucket

* Download from bucket
```
from google.cloud import storage

# Initiate Storage client
storage_client = storage.Client(project=gcp_project)

# Get reference to bucket
bucket = storage_client.bucket(bucket_name)

# Find all content in a bucket
blobs = bucket.list_blobs(prefix="input_audios/")
for blob in blobs:
    print(blob.name)
    if not blob.name.endswith("/"):
        blob.download_to_filename(blob.name)

```

* Upload to bucket
```
from google.cloud import storage

# Initiate Storage client
storage_client = storage.Client(project=gcp_project)

# Get reference to bucket
bucket = storage_client.bucket(bucket_name)

# Destination path in GCS 
destination_blob_name = "input_audios/test.mp3"
blob = bucket.blob(destination_blob_name)

blob.upload_from_filename("Path to test.mp3 on local computer")

```

### Some notes for running on Windows
* Docker Win10 installation - needs WSL2 or Hyper-V enabled: https://docs.docker.com/desktop/windows/install/
* Use `Git` BASH to run (which is like a smaller `Cygwin`)
* Needed to add pwd in quotes in order to escape the spaces that common in windows directory structures
* Need to prefix docker run with `winpty` otherwise I get a "the input device is not a TTY." error
* `winpty docker run --rm -ti --mount type=bind,source="$(pwd)",target=/app generate_text`
