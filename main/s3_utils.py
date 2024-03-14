import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import logging


def upload_file_to_s3(file, object_name=None):
    """
    Upload a file to an S3 bucket

    :param file: File to upload
    :param object_name: S3 object name. If not specified, file.name is used
    :return: True if file was uploaded, else False
    """
    if object_name is None:
        object_name = file.name

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    try:
        s3_client.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{object_name}"


def get_s3_presigned_url(object_name, expiration=3600):
    """
    Generate a presigned URL to access an S3 object with temporary access.

    :param object_name: S3 object name.
    :param expiration: Time in seconds for the presigned URL to remain valid. Default is 3600 seconds (1 hour).
    :return: Presigned URL of the S3 object, or None if error.
    """
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )

    try:
        presigned_url = s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.AWS_STORAGE_BUCKET_NAME, "Key": object_name},
            ExpiresIn=expiration,
        )
    except ClientError as e:
        logging.error(e)
        return None

    return presigned_url
