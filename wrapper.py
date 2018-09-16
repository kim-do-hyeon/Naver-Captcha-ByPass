import StringIO
import re
import urllib2

from pytesser import *


def convert_string(t):
    t = t.upper()
    t = re.findall('[A-Z]+', t)
    t = ''.join(t)
    return t


def convert_image_to_string(image, psm=3, oem=3):
    """
    :param image:
    :param psm: Page segmentation modes (Default: 3 - Fully automatic page segmentation, but no OSD.)
    :param oem: OCR Engine modes (Default: 3 - based on what is available.)
    """
    return image_to_string(image, psm, oem)


def extract_image_by_color(image, color):
    """
    :param image: RGB Mode Image
    :param color: RGB
    :return:
    """
    im = image.copy()
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            im.putpixel((y, x), (0, 0, 0) if (im.getpixel((y, x)) == color) else (255, 255, 255))
    return im


def extract_file_by_url(url):
    opener = urllib2.build_opener()
    data = opener.open(url).read()
    return StringIO.StringIO(data)


class Pixel:
    def __init__(self, color, pos):
        self.color = color
        self.pos = pos


def bypass_captcha_from_file(filename, monochrome=False):
    im = Image.open(filename)
    if monochrome:
        im = im.convert('RGB')
        im = extract_image_by_color(im, im.getpixel((0, 0)))
    text = convert_image_to_string(im, 3, 1)
    return convert_string(text)


def bypass_captcha_from_file2(filename):
    im = Image.open(filename)
    im = im.convert('RGB')
    pixel = []
    text = ''
    for x in range(im.size[1]):
        for y in range(im.size[0]):
            color = im.getpixel((y, x))
            b = True
            for i in range(0, len(pixel)):
                if pixel[i].color == color:
                    b = False
                    break
            if b:
                pixel.append(Pixel(color, y))
    pixel.sort(key=lambda v: v.pos)
    for i in range(1, len(pixel)):
        out = extract_image_by_color(im, pixel[i].color)
        text += convert_image_to_string(out, 10, 1)[0]
    return convert_string(text)


def bypass_captcha_from_url(url):
    f = extract_file_by_url(url)
    return bypass_captcha_from_file(f)


def bypass_captcha_from_url2(url):
    f = extract_file_by_url(url)
    return bypass_captcha_from_file2(f)
