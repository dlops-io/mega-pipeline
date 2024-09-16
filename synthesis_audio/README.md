# Synthesis Audio

🇫🇷 &rightarrow; 🔊

In this container you will implement the following:
* Read the translated text from the GCS bucket `mega-pipeline-bucket` and folder `text_translated`
* Use Cloud Text-to-Speech API to generate an audio file in French or any other language 
* Save the audio mp3 file in bucket `mega-pipeline-bucket` and folder `output_audios` (use the same file name and change the extension to .mp3)


# Create a local secrets folder and add the GCP Credentials File:
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
* Go to a terminal inside `synthesis_audio`
* Run docker container by using:
```
sh docker-shell.sh
```

## Run CLI

**Synthesis Audio**
```
python cli.py --download
python cli.py --synthesis
```