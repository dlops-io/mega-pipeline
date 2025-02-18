# Translate Text

🗒️ &rightarrow; 🇫🇷

In this container, you will implement the following:
* Read the text from the GCS bucket `mega-pipeline-bucket` and folder `text_paragraphs`
* Use `googletrans` to translate the text from English to French (or any other language)
* Save the translated text as a text file in bucket `mega-pipeline-bucket` and folder `text_translated` (use the same file name)


## Create a local secrets folder and add the GCP Credentials File:
It is important to note that we do not want any secure information in Git. So we will manage these files outside of the git folders. At the same level as the app folders create a folder called secrets

Your folder structure should look like this:

|-mega-pipeline<br>
    |-transcribe_audio<br>
    |-generate_text<br>
    |-synthesis_audio_en<br>
    |-translate_text<br>
    |-synthesis_audio<br>
|-secrets

Download the json file and place inside the secrets folder:
<a href="https://static.us.edusercontent.com/files/mlca0YEYdvkWPNEowJ0o4hOd" download>mega-pipeline.json</a>

## Run Docker Container
* Go to a terminal inside `translate_text`
* Run docker container by using:
```
sh docker-shell.sh
```

Various options to run docker-shell.sh are:
* `sh docker-shell.sh`          - Default option is to perform a local build and run
* `sh docker-shell.sh  prod`    - Build production docker image and push to registry
* `sh docker-shell.sh  dev`     - Build development docker image locally
* `sh docker-shell.sh  run`     - Run the container (uses registry image if local not found)


## Run CLI
**Translate Text**
```
python cli.py --download
python cli.py --translate
python cli.py --upload
```