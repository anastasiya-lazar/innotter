import logging
import boto3
from botocore.exceptions import ClientError
import os


class S3Service:
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_S3_REGION_NAME")
    )
    bucket_name = os.environ.get("AWS_STORAGE_BUCKET_NAME")

    def upload_file(self, file_name, object_name=None):
        if object_name is None:
            object_name = os.path.basename(file_name)
        try:
            self.s3_client.upload_fileobj(file_name, self.bucket_name, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return True

    def create_presigned_url(self, object_name):
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': object_name
                },
                ExpiresIn=3600
            )
        except ClientError as e:
            logging.error(e)
            return None
        return url

    def delete_object(self, object_name):
        response = self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=object_name
        )
        return response
