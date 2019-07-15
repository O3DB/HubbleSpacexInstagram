import os
import requests
import logging


logger = logging.getLogger(__name__)

def create_folder(folder_path):
    logger.debug(f'Executed create_folder func to create {folder_path}')
    try:
        os.makedirs(folder_path)
        logger.info(f'Folder {folder_path} created')
    except Exception as e:
        logger.error(f'Folder not created. {e}')
        pass


def make_request(url):
    logger.debug(f'Executed get_image({url})')
    try:
        response = requests.get(url,timeout=3)
        logger.info(f'Response status code {response.status_code}')
        if response.status_code // 100 == 2:
            return response
    except Exception as e:
        logger.error(e)


def check_mime_type(response, target_type):






# def get_image

def save_binary_content(content, file_path):
    logger.debug(f'Saving content to the {file_path}')
    with open(file_path, 'wb') as file:
        try:
            file.write(content)
            logger.info('Content succesfully saved')
        except Extension as e:
            logger.error(f'Error has occured while saving content. {e}')


def define_extension_from_url(url):
    logger.debug('Defining extension of {url}')
    extensions = ['jpg', 'jpeg', 'png', 'bmp', 'tif']
    if any(img_extension in url for img_extension in extensions):
        extension = url.split('.')[-1]
        logger.info(f'Extension defined: {extension}')
        return extension
    logger.warning(f'Extension not in {extensions}')


def download_image(url, filename=None, path=None):
    logger.debug(f'download_image execudet with argument: {url}')
    extension = define_extension_from_url(url)
    if not extension:
        pass
    response = make_request(url)
    if not response:
        pass
    if 'image' not in response.headers['content-type']:
        logger.warning(f'Mime type not image: {response.headers['content-type']}')
    if filename:
        
        file_path = filename + '.' + extension
    else:
        filename = url.split('/')[-1]
    if path:
        file_path = os.path.join(path, file_path)
    save_binary_content()


