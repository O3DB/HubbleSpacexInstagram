import logging
import os
from tools import create_folder, make_request, download_image


logger = logging.getLogger(__name__)


def get_hubble_image_url(image_id):
    url = f'http://hubblesite.org/api/v3/image/{image_id}'
    response = make_request(url)
    return 'https:' + response.json()['image_files'][-1]['file_url']


def fetch_hubble_collection(collection_name, template_filename='hubble', path='downloads/hubble'):
    collection_url = 'http://hubblesite.org/api/v3/images'
    image_url = 'http://hubblesite.org/api/v3/image/{}'
    payload = {'page': 'all', 'collection_name': collection_name}
    path = os.path.join(path, collection_name)

    response = make_request(collection_url, payload=payload)
    images_info = response.json()

    for image in images_info:
        image_id = image['id']
        image_url = get_hubble_image_url(image_id)
        filename = template_filename + '_' + str(id)
        download_image(image_url, filename, path)


def fetch_hubble_image(image_id, template_filename='hubble', path='downloads/hubble'):
    image_url = get_hubble_image_url(image_id)
    filename = template_filename + str(image_id)
    create_folder(path)
    download_image(image_url, filename, path)

