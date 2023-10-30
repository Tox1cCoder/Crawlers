import os
import sys
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from logger import log
from crawler.base_crawler import BaseCrawler
from utils.bs4_utils import get_text_from_tag


class VNExpressCrawler(BaseCrawler):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.logger = log.get_logger(name=__name__)
        self.article_type_dict = {
            0: "thoi-su",
            1: "du-lich",
            2: "the-gioi",
            3: "kinh-doanh",
            4: "khoa-hoc",
            5: "giai-tri",
            6: "the-thao",
            7: "phap-luat",
            8: "giao-duc",
            9: "suc-khoe",
            10: "doi-song"
        }

    def extract_content(self, url: str) -> tuple:
        """
        Extract title, description, paragraphs, and image URLs from the URL.
        @param url (str): URL to crawl
        @return title (str)
        @return description (generator)
        @return paragraphs (generator)
        @return image_urls (list)
        """
        content = requests.get(url).content
        soup = BeautifulSoup(content, "html.parser")

        title = soup.find("h1", class_="title-detail")
        if title is None:
            return None, None, None, []

        title = title.text

        description = (get_text_from_tag(p) for p in soup.find("p", class_="description").contents)
        paragraphs = (get_text_from_tag(p) for p in soup.find_all("p", class_="Normal"))

        # Extract image URLs
        image_urls = []
        image_tags = soup.find_all("img", itemprop="contentUrl")
        for img_tag in image_tags:
            image_url = img_tag.get("data-src")
            if image_url:
                image_urls.append(urljoin(url, image_url))

        return title, description, paragraphs, image_urls

    def write_content(self, url: str, output_fpath: str) -> bool:
        """
        From URL, extract title, description, paragraphs, and download/save images.
        @param url (str): URL to crawl
        @param output_fpath (str): File path to save crawled result
        @return (bool): True if crawl successfully and otherwise
        """
        title, description, paragraphs, image_urls = self.extract_content(url)

        if title is None:
            return False

        with open(output_fpath, "w", encoding="utf-8") as file:
            file.write(title + "\n")
            for p in description:
                file.write(p + "\n")
            for p in paragraphs:
                file.write(p + "\n")

        # Create a directory to save images
        image_dir = os.path.join(os.path.dirname(output_fpath), "images")
        os.makedirs(image_dir, exist_ok=True)

        # Download and save images
        for i, image_url in enumerate(image_urls):
            image_filename = f"image_{i}.jpg"  # You can use a better naming scheme if needed
            image_path = os.path.join(image_dir, image_filename)

            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_path, "wb") as image_file:
                    image_file.write(response.content)

        return True

    def get_urls_of_type_thread(self, article_type, page_number):
        """" Get urls of articles in a specific type in a page"""
        page_url = f"https://vnexpress.net/{article_type}-p{page_number}"
        content = requests.get(page_url).content
        soup = BeautifulSoup(content, "html.parser")
        titles = soup.find_all(class_="title-news")

        if (len(titles) == 0):
            self.logger.info(
                f"Couldn't find any news in {page_url} \nMaybe you sent too many requests, try using less workers")

        articles_urls = list()

        for title in titles:
            link = title.find_all("a")[0]
            articles_urls.append(link.get("href"))

        return articles_urls
