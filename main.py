import os
import logging
import argparse
import sys

from log import setup_logging
from tools import create_folder, download_image
from spacex import fetch_spacex_latest_launch
from hubble import fetch_hubble_collection, fetch_hubble_image
from instagram import upload_photos_to_instagram


def parse_args():
    parser = argparse.ArgumentParser(
        description="Script supports: downloading hubble collections photos\
        or SpaceX last launch photos and upploading photos from /images\
        to Instagram")
    parser.add_argument('-hbl', '--hubble', help='enter collection name to download')
    parser.add_argument('-s', '--spacex', help='qty of latest spacex launch photos to download', type=int)
    parser.add_argument('-inst', '--instagram', help='pass timeout value between uploads', type=int)
    return parser.parse_args()


def main():
    logger = logging.getLogger('main')
    setup_logging()
    logger.info('Program started')

    args = parse_args()
    if len(sys.argv) <=1:
        logger.info('No arguments passed. Program can not be started')
        print('Please input at least one argument and run script again')
        return
    logger.info(f'Program started with args: {args}')
    hubble_collection = args.hubble
    spacex_qty = args.spacex
    instagram_timeout = args.instagram

    if hubble_collection:
        if not fetch_hubble_collection(hubble_collection):
            print('Collection not found')
    if spacex_qty:
        fetch_spacex_latest_launch(qty=spacex_qty)
    if instagram_timeout:
        upload_photos_to_instagram(timeout=instagram_timeout)


if __name__ == '__main__':
    main()
    