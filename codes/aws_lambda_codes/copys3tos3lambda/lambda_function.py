import json
import boto3
from datetime import datetime, timedelta

SOURCE_BUCKET = 'a-quiet-place-2'
DESTINATION_BUCKET = 'athenacheck'
SRC_KEY = 'A.Quiet.Place.Part.II.2020.1080p.WEBRip.x265-RARBG/A.Quiet.Place.Part.II.2020.1080p.WEBRip.x265-RARBG.mp4'


s3_client = boto3.client('s3')
s3 = boto3.resource('s3')
def lambda_handler(event, context):
    copy_source = {
        'Bucket': SOURCE_BUCKET,
        'Key': SRC_KEY
    }
    s3.meta.client.copy(copy_source, DESTINATION_BUCKET, 'quite.mp4')
    # Copy object
    # s3_client.copy_object(
    #     Bucket=DESTINATION_BUCKET,
    #     #Key='quiteplacemovie.mp4',
    #     Key='a.srt',
    #     CopySource={'Bucket':SOURCE_BUCKET, 'Key':SRC_KEY})    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
