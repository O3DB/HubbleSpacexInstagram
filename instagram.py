import os
import random
import time
import tempfile

from instabot import Bot
from instabot.api.api_photo import compatible_aspect_ratio, get_image_size
import PIL.Image
import numpy as np

from config import USERNAME, PASSWORD
from tools import scan_for_files_in_folder


def correct_ratio(photo):
    return compatible_aspect_ratio(get_image_size(photo))


def fix_photo(photo):
    with open(photo, 'rb') as f:
        img = PIL.Image.open(f)
        img = strip_exif(img)
        if not correct_ratio(photo):
            img = get_highest_entropy(img)
        photo = os.path.join(tempfile.gettempdir(), 'instacron.jpg')
        img.save(photo)
    return photo


def entropy(data):
    """Calculate the entropy of an image"""
    hist = np.array(PIL.Image.fromarray(data).histogram())
    hist = hist / hist.sum()
    hist = hist[hist != 0]
    return -np.sum(hist * np.log2(hist))


def crop(x, y, data, w, h):
    x = int(x)
    y = int(y)
    return data[y:y + h, x:x + w]


def get_highest_entropy(img, min_ratio=4 / 5, max_ratio=90 / 47):
    from scipy.optimize import minimize_scalar
    w, h = img.size
    data = np.array(img)
    ratio = w / h
    if ratio > max_ratio:
        # Too wide
        w_max = int(max_ratio * h)

        def _crop(x): return crop(x, y=0, data=data, w=w_max, h=h)
        xy_max = w - w_max
    else:
        # Too narrow
        h_max = int(w / min_ratio)

        def _crop(y): return crop(x=0, y=y, data=data, w=w, h=h_max)
        xy_max = h - h_max
    x = minimize_scalar(lambda xy: -entropy(_crop(xy)),
                        bounds=(0, xy_max),
                        method='bounded').x
    return PIL.Image.fromarray(_crop(x))


def strip_exif(img):
    """Strip EXIF data from the photo to avoid a 500 error."""
    data = list(img.getdata())
    image_without_exif = PIL.Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    return image_without_exif


def upload_photos_to_instagram(foldername, captions=['Good', 'Nice photo'], timeout=30):
    bot = Bot()
    bot.login(username=USERNAME, password=PASSWORD)
    photos = scan_for_files_in_folder(foldername)
    for photo in photos:
        photo_path = os.path.join(foldername, photo)
        pic = fix_photo(photo_path)
        caption = random.choice(captions)
        bot.upload_photo(pic, caption=caption)
        time.sleep(timeout)


