#!/opt/conda/bin/python3

import json
import subprocess
from hashlib import md5

import os

import boto3

from get_dataset import fetch

def generate_id(id_prefix, context_filename):
        timestamp = subprocess.check_output(['date', '-u', '+%Y%m%dT%H%M%S.%NZ']).decode().strip()

        with open(context_filename) as context_file:
            hash_suffix = md5(context_file.read().encode()).hexdigest()[0:5]

        job_id = f'{id_prefix}-{timestamp}-{hash_suffix}'
        print(f'Generated job ID: {job_id}')
        return job_id

pge_root = os.environ["pge_root"]
context_filepath = os.path.join(pge_root, '_context.json')

download_root = '.'
job_id = generate_id('S1-ARIARNN-PREPARED-DATA', context_filepath)
output_root = f'./{job_id}'
os.makedirs(output_root)


# TODO: Replace this with localization preprocessor
with open(context_filepath) as context_file:
    context = json.load(context_file)

# input_dataset = next(filter(lambda param: param['name'] == 'input_dataset', context['job_specification']['params']))
# url = next(filter(lambda url: url.startswith('s3://'), input_dataset['value']['urls']))
url = 's3://s3-us-west-2.amazonaws.com/aria-dev-lts-fwd-torresal/datasets/stack/v1.0/2015/03/15/coregistered_slcs-20150315231319-20161222231426'

_, bucket_name, data_product_root_path = url.split('amazonaws.com')[1].split('/', 2)

files = [
    '*/merged/geom_master/lat.rdr.full*',
    '*/merged/geom_master/lon.rdr.full*',
    '*/merged/SLC/*'
]

s3 = boto3.resource('s3')
bucket = s3.Bucket(bucket_name)
fetch(bucket, data_product_root_path, files, download_root)

os.chdir(os.path.join(os.getcwd(), data_product_root_path, 'merged'))

out = subprocess.check_output([f'{pge_root}/process_frames.sh'])
print(out)

with open(os.path.join(output_root, f'{job_id}.dataset.json'), 'w+') as definition_file:
    json.dump({
        "version": "v1.0",
        # "location": input_dataset['value']['location']
    }, definition_file)

with open(os.path.join(output_root, f'{job_id}.met.json'), 'w+') as metadata_file:
    json.dump({}, metadata_file)