#!/usr/bin/env python3

import argparse
import logging
import re
import sys
from pathlib import Path

import bs4
import requests

logger = logging.getLogger()
parser = argparse.ArgumentParser()


def _setup_logging(verbosity: int):
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)
    if verbosity >= 1:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(logging.INFO)


def _setup_arguments():
    parser.add_argument('destination', type=str)
    parser.add_argument('url', type=str)
    parser.add_argument('-v', '--verbose', action='count', default=0)


def find_videos(soup: bs4.BeautifulSoup) -> list[str]:
    video = soup.find_all('source', attrs={'src': re.compile(r'.*\.etsystatic.com/video.*')})
    video = [vid.get('src') for vid in video]
    return video


def find_images(soup: bs4.BeautifulSoup) -> list[str]:
    image_holder = soup.find('div', attrs={'class': 'image-carousel-container'})
    images = image_holder.find_all('img', attrs={'data-src': re.compile(r'https://i\.etsystatic.*')})
    images.append(soup.find('img', attrs={'src': re.compile(r'https://i\.etsystatic.*')}))
    images = [image.get('data-src') for image in images]
    return images


def main(args: argparse.Namespace):
    _setup_logging(args.verbose)

    args.destination = Path(args.destination).resolve().expanduser()
    args.destination.mkdir(exist_ok=True)

    page = requests.get(args.url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')

    images = find_images(soup)
    logger.info(f'Found {len(images)} images')

    videos = find_videos(soup)
    logger.info(f'Found {len(videos)} videos')

    resources = list(filter(None, images + videos))
    download_resources(args.destination, resources)


def download_resources(root_destination: Path, resources: list[str]):
    for res in resources:
        data = requests.get(res)
        url_regex = re.compile(r'.*/(.*?)$')
        name = re.match(url_regex, data.url).group(1)
        destination = Path(root_destination, name)
        with open(destination, 'wb') as file:
            file.write(data.content)
        logger.debug(f'Written {destination.name} to disk')


if __name__ == '__main__':
    _setup_arguments()
    args = parser.parse_args()
    main(args)
