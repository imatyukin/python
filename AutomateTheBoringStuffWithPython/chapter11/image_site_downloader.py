#!/usr/bin/env python3
import requests
import bs4
import shutil
import os


def main():
    res = requests.get('http://imgur.com/')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')

    if not os.path.exists("images"):
        os.mkdir("images")

    for idx, image in enumerate(soup.select('img[alt]')):
        image_link = "http:" + image.get('src')
        image_file = requests.get(image_link, stream=True)
        with open('images/img_' + str(idx) + '.jpg', 'wb') as f:
            shutil.copyfileobj(image_file.raw, f)
        del image_file


if __name__ == "__main__":
    main()
