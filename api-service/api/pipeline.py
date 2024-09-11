import os
import asyncio
from glob import glob
from google.cloud import storage

gcp_project = "ac215-project"
bucket_name = "mega-pipeline-bucket"
input_audios = "/persistent/input_audios"
text_prompts = "/persistent/text_prompts"
text_paragraphs = "/persistent/text_paragraphs"
text_audios = "/persistent/text_audios"
text_translated = "/persistent/text_translated"
output_audios = "/persistent/output_audios"
output_audios_pp = "/persistent/output_audios_pp"

storage_client = storage.Client(project=gcp_project)
bucket = storage_client.bucket(bucket_name)


def makedirs():
    os.makedirs(input_audios, exist_ok=True)
    os.makedirs(text_prompts, exist_ok=True)
    os.makedirs(text_paragraphs, exist_ok=True)
    os.makedirs(text_audios, exist_ok=True)
    os.makedirs(text_translated, exist_ok=True)
    os.makedirs(output_audios, exist_ok=True)
    os.makedirs(output_audios_pp, exist_ok=True)


def delete_files(folder):
    files = glob(folder + "/*/*")
    for f in files:
        os.remove(f)


accepted_files = [
    "input-01",
    "input-02",
    "input-03",
    "input-04",
    "input-05",
    "input-06",
    "input-07",
    "input-08",
    "input-09",
    "input-10",
]


def download_files(match_glob):
    blobs = bucket.list_blobs(match_glob=match_glob)
    for blob in blobs:
        print(blob.name)
    # blobs = bucket.list_blobs(prefix=folder + "/")
    # for blob in blobs:
    #     if blob.name.endswith("/"):
    #         continue
    #     pathname, extension = os.path.splitext(blob.name)
    #     filename = pathname.split("/")[-1]
    #     if filename in accepted_files:
    #         extension = os.path.splitext(blob.name)[1]
    #         if extension == ".mp3" or extension == ".txt":
    #             local_file_path = "/persistent/" + blob.name
    #             if not os.path.exists(local_file_path):
    #                 print("Downloading:", blob.name)
    #                 blob.download_to_filename(local_file_path)
    #     else:
    #         # Delete files not accepted
    #         print("Delete:", blob.name)
    #         #blob.delete()


def sync_files(match_glob):
    print("Sync:", match_glob)
    blobs = bucket.list_blobs(match_glob=match_glob)
    for blob in blobs:
        print(blob.name)
        local_file_path = "/persistent/" + blob.name
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        print("Downloading:", blob.name)
        blob.download_to_filename(local_file_path)
    # # local files
    # local_files = os.listdir("/persistent/" + folder)

    # blobs = bucket.list_blobs(prefix=folder + "/")
    # for blob in blobs:
    #     if blob.name.endswith("/"):
    #         continue
    #     pathname, extension = os.path.splitext(blob.name)
    #     filename = pathname.split("/")[-1]
    #     if filename in accepted_files:
    #         extension = os.path.splitext(blob.name)[1]
    #         if extension == ".mp3" or extension == ".m4a" or extension == ".txt":
    #             local_file_path = "/persistent/" + blob.name
    #             if not os.path.exists(local_file_path):
    #                 print("Downloading:", blob.name)
    #                 blob.download_to_filename(local_file_path)

    #             if local_file_path in local_files:
    #                 local_files.remove(local_file_path)
    #     else:
    #         # Delete files not accepted
    #         print("Delete:", blob.name)
    #         #blob.delete()

    # print("local_files:", local_files)
    # for local_file in local_files:
    #     if os.path.exists(local_file):
    #         os.remove(local_file)


def sync_file_ondemand():
    # Ensure we have the folders
    makedirs()

    # Delete all local files if the exist
    delete_files(input_audios)
    delete_files(text_prompts)
    delete_files(text_paragraphs)
    delete_files(text_audios)
    delete_files(text_translated)
    delete_files(output_audios)
    delete_files(output_audios_pp)

    sync_files("input_audios")
    sync_files("text_prompts")
    sync_files("text_paragraphs")
    sync_files("text_audios")
    sync_files("text_translated")
    sync_files("output_audios")
    sync_files("output_audios_pp")


class PipelineManager:
    def __init__(self):
        self.timestamp = 0

    async def sync(self):
        # Ensure we have the folders
        makedirs()

        # Delete all local files if the exist
        delete_files(input_audios)
        delete_files(text_prompts)
        delete_files(text_paragraphs)
        delete_files(text_audios)
        delete_files(text_translated)
        delete_files(output_audios)
        delete_files(output_audios_pp)

        while True:
            print("Syncing Pipeline files...")
            sync_files("input_audios/input-*.mp3")
            sync_files("text_prompts/*/input-*.txt")
            sync_files("text_paragraphs/*/input-*.txt")
            sync_files("text_audios/*/input-*.mp3")
            # sync_files("text_translated")
            # sync_files("output_audios")
            # sync_files("output_audios_pp")

            # Wait
            await asyncio.sleep(15)
