# Transcribe Audio

🎙️ &rightarrow; 📝 

In this container, you will implement the following:
* Read audio files from the GCS bucket `mega-pipeline-bucket` and folder `input_audios`
* Use the Google Cloud Speech-to-Text API
* Save the transcribed text as a text file in bucket `mega-pipeline-bucket` and folder `text_prompts` (use the same file name and change extension to .txt)


## Create a local secrets folder and add the GCP Credentials File:
It is important to note that we do not want any secure information in Git. So we will manage these files outside of the git folders. At the same level as the app folders create a folder called secrets

Your folder structure should look like this:

|-mega-pipeline<br>
   &nbsp; &nbsp;   &nbsp; &nbsp;  |-transcribe_audio<br>
    &nbsp; &nbsp;   &nbsp; &nbsp; |-generate_text<br>
    &nbsp; &nbsp;   &nbsp; &nbsp; |-synthesis_audio_en<br>
    &nbsp; &nbsp;   &nbsp; &nbsp; |-translate_text<br>
    &nbsp; &nbsp;  &nbsp; &nbsp;  |-synthesis_audio<br>
|-secrets

Download the json file and place inside the secrets folder:
<a href="https://static.us.edusercontent.com/files/mlca0YEYdvkWPNEowJ0o4hOd" download>mega-pipeline.json</a>

## Run Docker Container
* Go to a terminal inside `transcribe_audio`
* Run docker container by using:
```
sh docker-shell.sh
```

## Run CLI

**Transcribe Audio**
```
python cli.py --download
python cli.py --transcribe
python cli.py --upload
```

