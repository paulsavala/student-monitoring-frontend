import boto3
import json

def empty_str_to_null(s):
    if s.strip() == '':
        return None
    else:
        return s

def read_from_s3(bucket, key, as_dict=False, ignore_missing=False):
    s3 = boto3.client('s3')
    try:
        f = s3.get_object(Bucket=bucket, Key=key)
        result = f['Body'].read().decode()
        if as_dict:
            return json.loads(result)
        return result
    except Exception as e:
        if not ignore_missing:
            print(f'Error accessing {bucket}/{key}')
            raise
        else:
            print(f'{bucket}/{key} does not exist, returning None')
            return None
