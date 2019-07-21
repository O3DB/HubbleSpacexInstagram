import os, errno
from os import walk
import requests
import logging
from config import verify_ssl


logger = logging.getLogger(__name__)


def create_folder(folder_path):
    logger.debug(f'Executed create_folder func to create {folder_path}')
    try:
        os.makedirs(folder_path)
        logger.debug(f'Folder {folder_path} created')
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
        logger.debug('Folder allready exists')


def make_request(url, payload=None, timeout=3):
    logger.debug(f'Executed get_image({url})')
    try:
        response = requests.get(url, params=payload, timeout=timeout, verify=verify_ssl)
        logger.debug(f'Response status code {response.status_code}')
        if response.status_code // 100 == 2:
            return response
    except Exception as e:
        logger.error(e)


def save_binary_content(content, file_path):
    logger.debug(f'Saving content to the {file_path}')
    with open(file_path, 'wb') as file:
        file.write(content)


def define_image_extension_from_url(url):
    logger.debug('Defining extension of {url}')
    extensions = ['jpg', 'jpeg', 'png', 'bmp', 'tif']
    if any(img_extension in url for img_extension in extensions):
        extension = url.split('.')[-1]
        logger.info(f'Extension defined: {extension}')
        return extension
    logger.warning(f'Extension not in {extensions}')


def check_mime_type(response, type='image'):
    '''function takes response object,
    compare MIME type with passed type (image by default)
    and returns document's extension
    '''
    content_type = response.headers['content-type']
    logger.debug(f'Content type is {content_type}')
    if type not in content_type:
        return
    return content_type.split('/')[-1]


def scan_for_files_in_folder(foldername, recursion=False):
    files = []
    for (dirpath, dirnames, filenames) in walk(foldername):
        files.extend(filenames)
        if not recursion:
            break
    return files


def download_image(url, filename='image', path='.'):
    logger.info(f'Start image downloading from {url}')
    response = make_request(url)
    if not response:
        logger.info("Didn't get 2xx response. Function stoped")
        return
    extension = check_mime_type(response)
    if not extension:
        logger.info('Extension not defined. Function stoped')
        return
    logger.info(f'Get image content with {extension} extension')
    filename = filename + '.' + extension
    file_path = os.path.join(path, filename)

    save_binary_content(response.content, file_path)
    logger.info(f'Successfully downloaded {file_path}')