import boto3
import os


class SESService:
    ses_client = boto3.client('ses', region_name=os.getenv("AWS_S3_REGION_NAME"))

    def send_email(self, source, destination, subject, text, html, reply_tos=None):
        send_args = {
            'Source': source,
            'Destination': {
                'ToAddresses': [
                    destination,
                ]
            },
            'Message': {
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': text,
                        'Charset': 'UTF-8'
                    },
                    'Html': {
                        'Data': html,
                        'Charset': 'UTF-8'
                    }
                }
            }
        }
        if reply_tos is not None:
            send_args['ReplyToAddresses'] = reply_tos
        response = self.ses_client.send_email(**send_args)
        message_id = response['MessageId']
        return message_id
