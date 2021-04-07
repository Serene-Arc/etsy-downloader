#!/usr/bin/env python3
# coding=utf-8

import bs4
import pytest
import requests

import etsydownloader.__main__ as main


@pytest.mark.parametrize(('test_url', 'expected_len'), (
    ('https://www.etsy.com/au/listing/928498580/925-sterling-silver-butterfly-necklace', 9),
    ('https://www.etsy.com/au/listing/256472602/koala-necklace-in-silver-gold-collarbone', 4),
    ('https://www.etsy.com/au/listing/911249518/gemstone-chew-chewlery-adhd-anxiety', 10),
    ('https://www.etsy.com/au/listing/824302891/chill-pill-mix-match-stainless-steel', 10),
    ('https://www.etsy.com/au/listing/948839970/flip-desk-toy-rotating-pocket-toy-fidget', 8),
))
def test_find_images(test_url: str, expected_len: int):
    page = requests.get(test_url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    results = main.find_images(soup)
    assert len(results) == expected_len


@pytest.mark.parametrize(('test_url', 'expected_len'), (
    ('https://www.etsy.com/au/listing/824302891/chill-pill-mix-match-stainless-steel', 1),
    ('https://www.etsy.com/au/listing/948839970/flip-desk-toy-rotating-pocket-toy-fidget', 1),
))
def test_find_videos(test_url: str, expected_len: int):
    page = requests.get(test_url)
    soup = bs4.BeautifulSoup(page.text, 'html.parser')
    results = main.find_videos(soup)
    assert len(results) == expected_len
