import logging
from tools import create_folder, make_request, download_image

logger = logging.getLogger(__name__)



def fetch_spacex_latest_launch(path='downloads/spacex', filename_template='spacex'):
    logger.info('Starting to fetching spacex last launch photos')
    url = 'https://api.spacexdata.com/v3/launches/latest'
    create_folder('')
    response = make_request(url)
    if not response:
        logger.info("Didn't get 2xx response. Function stoped")
        pass
    try:
        urls = response.json()['links']['flickr_images']
    except Exception as e:
        logger.error(f"Urls didn't collected. {e}")
    logger.info('Images urls received')

    for index, url in enumerate(urls):
        filename = '{}_{}'.format(filename_template, index)
        download_image(url, filename, path)
