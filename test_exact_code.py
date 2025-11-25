"""
A script to practice how the csv file is read from s3 file, transformed into dictionary , add metadata (similiar to  raw vg ingestor)
"""


import boto3
from aws_lambda_powertools.utilities.streaming import S3Object
from aws_lambda_powertools.utilities.streaming.transformations import CsvTransform
from aws_lambda_powertools.logging import Logger
from helper import Metadata, meta_row_number

# upload a csv file into s3 bucket

logger = Logger()


def file_upload():
    file_csv = './test.csv'
    s3 = boto3.client('s3')
    s3.upload_file(file_csv, 'test-s3-bucket-13', 'test.csv')
    return print("file has been uploaded")


# file_upload()
#  read the csv file from the s3 bucket
def read_file():
    bucket = 'test-s3-bucket-13'
    key = 'test.csv'
    s3_obj = S3Object(bucket=bucket, key=key)
    lines = s3_obj.readlines()
    decoded_lines = [line.decode("utf-8").rstrip("\n") for line in lines]
    return print(f"these are decoded line {decoded_lines}")


# read_file()
#  read the file and transform the data into dictionary in batches

FIELDS = [
    "Name",
    "mail",
    "Phone",
    "Address",
    "sale_price"
]

def batch_transform():
    bucket = 'test-s3-bucket-13'
    key = 'test.csv'
    logger.info(
        f"Retrieving S3 file {key} from bucket {bucket}."
    )
    fieldnames = FIELDS
    s3_obj = S3Object(bucket=bucket, key=key)
    dict_reader = s3_obj.transform(CsvTransform(
        fieldnames=fieldnames,
        encoding="utf-8",
        delimiter=",")
        )
     # Skip the first row (header row)
    next(dict_reader)
#   This will read a row which is changed to a dict and add a addition column
# meta_source_file_row_number and counts the rows using meta_row_number function

    dict_reader_with_numbers = meta_row_number(dict_reader, row_num_start=1)
    for row in dict_reader_with_numbers:
        print(row)
    return dict_reader_with_numbers
# print(type(dict_reader_with_numbers))


# batch_transform()

# create row number for each record
# create some metadata and cloud event headers

def create_metadata():
    metadata = Metadata(
        source_file="input.csv",
        source_file_row=42
    )
    metadata_test = metadata.to_string
    return print(type(metadata_test))


# create_metadata()

def cloud_event():
  pass