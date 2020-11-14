import os
from typing import List
import boto3
from fnmatch import fnmatch

def get_filepaths_from_s3(bucket, prefix=''):
    """Given a path prefix, return a list of all matching filepaths."""
    object_summaries = bucket.objects.filter(Prefix=prefix)
    return map(lambda object: object.key, object_summaries)


def fetch(bucket, data_product_root_path: str, match_patterns: List[str], download_directory: str = '.') -> None:
    """Given an s3 root url and a set of linux-style match-patterns, download all files under that root matching any of the patterns"""
    filepaths = get_filepaths_from_s3(bucket, data_product_root_path)

    for source_filepath in filepaths:
        if any(map(lambda pattern: fnmatch(source_filepath, pattern), match_patterns)):
            destination_filepath = os.path.join(download_directory, source_filepath)

            destination_dir = os.path.split(destination_filepath)[0]
            if not os.path.isdir(destination_dir):
                os.makedirs(destination_dir)

            print(f'Downloading {source_filepath} to {destination_filepath}')
            bucket.download_file(source_filepath, destination_filepath)
