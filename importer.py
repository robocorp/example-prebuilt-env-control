import logging
import subprocess

import boto3
from RPA.Robocorp.WorkItems import WorkItems
from RPA.Robocorp.Vault import Vault

HOLOLIB_ZIP = "hololib.zip"

wi = WorkItems()
wi.get_input_work_item()
variables = wi.get_work_item_variables()


def download_from_s3(path: str):
    _secret = Vault().get_secret("s3secret")

    s3_key = _secret["key"]
    s3_secret = _secret["secret"]
    s3 = boto3.client(
        "s3",
        aws_access_key_id=s3_key,
        aws_secret_access_key=s3_secret,
        region_name='eu-west-1'
    )

    s3_bucket = variables["bucket"]
    s3.download_file(s3_bucket, path, HOLOLIB_ZIP)

def rcc_import() -> str:
    result = subprocess.run(["/usr/bin/rcc", "ht", "import", HOLOLIB_ZIP], capture_output=True, text=True, shell=True)
    logging.debug(f"RCC stdout: {result.stdout}")
    logging.debug(f"RCC stderr: {result.stderr}")
    logging.info("imported the holotree")

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    url = variables["holotree_location"]

    download_from_s3(url)
    rcc_import()