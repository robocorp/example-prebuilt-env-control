import logging
import os
import random
import string
import requests
import subprocess

import boto3
from RPA.Robocorp.Vault import Vault
from RPA.Robocorp.WorkItems import WorkItems

HOLOLIB_ZIP = "hololib.zip"

def get_env_file(url: str) -> str:
    logging.info(f"received the URL from workitem: {url}")
    filename = os.path.basename(url)
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    logging.info(f"downloaded the file {filename}")
    return filename

def rcc_prebuild(filename: str, output_filename: str):
    rcc_path = os.environ.get("RCC_EXE", "rcc")
    command = [rcc_path, "ht", "prebuild", "--export", output_filename, filename]
    if filename == "conda.yaml":
        command.insert(3, "--force")
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    logging.debug(f"RCC stdout: {result.stdout}")
    logging.debug(f"RCC stderr: {result.stderr}")
    os.remove(filename)

def upload_to_s3(filename: str, bucket_name: str):
    _secret = Vault().get_secret("s3secret")

    s3_key = _secret["key"]
    s3_secret = _secret["secret"]
    s3 = boto3.client(
        "s3",
        aws_access_key_id=s3_key,
        aws_secret_access_key=s3_secret,
        region_name='eu-west-1'
    )

    rand = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    dest_name = f"{rand}-{filename}"

    with open(filename, "rb") as f:
        s3.upload_fileobj(f, bucket_name, dest_name)

    logging.info(f"File '{dest_name}' uploaded to S3 bucket '{bucket_name}'")
    wi.create_output_work_item({"holotree_location": dest_name, "bucket": bucket_name}, save=True)
    os.remove(HOLOLIB_ZIP)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    wi = WorkItems()
    wi.get_input_work_item()
    variables = wi.get_work_item_variables()
    url = variables["url"]
    bucket_name = variables.get("bucket")

    filename = get_env_file(url)
    rcc_prebuild(filename, HOLOLIB_ZIP)
    upload_to_s3(HOLOLIB_ZIP, bucket_name)