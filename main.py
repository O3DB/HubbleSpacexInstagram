import os
import logging

#composite tools
def download_image(url, file_path):
    response = safety_request(url)
    if isinstance(response, str):
        return response
    if 'image' in response.headers['content-type']:
        return response.status_code
    else:
        return f'No image found on the url: {url}'
    save_binary_content(response.content, file_path)




#SpaceX
def download_spaceX_image(image_url, folder_path):
    img_extension = define_extension_from_url(image_url)
    if not img_extension:
        pass
    file_path = os.path.join(folder_path, filename + '_' + str(index) + '.' + img_extension)
    download_image(image_url, file_path)


# def fetch_spacex_last_launch_images(folder_path='downloads/spacex'):
#     url = 'https://api.spacexdata.com/v3/launches/latest'
#     filename = 'spaceX_last_launch'

#     create_folder(folder_path)

#     response = safety_request(url)
#     if isinstance(response, str):
#         return response
#     image_urls = response.json()['links']['flickr_images']

#     for index

#     rs = (grequests.get(url) for url in image_urls)
#     for index, response in enumerate(grequests.map(rs)):
#         print(response.content)
#         print(index)
#         file_path = os.path.join(folder_path, filename + '_' + str(index) + '.' + 'jpg')
#         print(file_path)
#         save_binary_content(response.content, file_path)




logger = logging.getLogger('main')
if __name__ == '__main__':
    from log import setup_logging
    from tools import create_folder, download_image

    setup_logging()
    

    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warning('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

    download_image('https://upload.wikimedia.org/wikipedia/commons/3/3f/HST-SM4.jpeg')