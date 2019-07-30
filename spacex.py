import logging
import requests
from tools import download_image

logger = logging.getLogger(__name__)



def fetch_spacex_latest_launch(launch='latest', path='images/spacex', filename='spacex_', qty=1):
    url = f'https://api.spacexdata.com/v3/launches/{launch}'
    response = requests.get(url)
    response.raise_for_status()
    urls = response.json()['links']['flickr_images']

    qty = min(qty, len(urls))
    for index, url in enumerate(urls[:qty]):
        download_image(url, path, filename + str(index))
