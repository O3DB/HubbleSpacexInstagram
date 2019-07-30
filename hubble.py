import logging
import os
import requests

from tools import download_image
from errors import merry


logger = logging.getLogger(__name__)


def get_hubble_collection_ids(collection_name):
    url = 'http://hubblesite.org/api/v3/images'
    payload = {'page': 'all', 'collection_name': collection_name}
    response = requests.get(url, params=payload)
    response.raise_for_status()
    images_info = response.json()
    return [image['id'] for image in images_info]


def download_hubble_image(image_id, path='images', filename=None):
    url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = requests.get(url)
    response.raise_for_status()
    image_url = 'https:' + response.json()['image_files'][-1]['file_url']
    if not filename:
        filename = 'hubble_{}'.format(image_id)
    download_image(image_url, path, filename, verify=False)

@merry._try
def fetch_hubble_collection(collection_name, path='images', qty=None):
    image_ids = get_hubble_collection_ids(collection_name)
    if not image_ids:
        logger.warning(f'No photos found in collection "{collection_name}""')
    if not qty:
        qty = len(image_ids)
    qty = min(qty, len(image_ids))

    for image_id in image_ids[:qty]:
        download_hubble_image(image_id)