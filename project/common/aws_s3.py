import boto3


def copy_to_bucket(bucket_from_name, bucket_to_name, file_name, rename=False):
    s3 = boto3.resource('s3')
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3.meta.client.copy(copy_source, bucket_to_name, 'otherkey')
