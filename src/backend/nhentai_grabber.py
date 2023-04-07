import asyncio
import os
import time

import requests
from bs4 import BeautifulSoup
from NHentai import NHentaiAsync

# TODO: Problems may occur when manga name is too long

print("Preparing for parsing")
class Grabber:
    def __init__(
        self,
        folder: str,
        try_counts: int = -1,
        wait_time: int = 3,
        tags_delimiter: str = "; ",
        tags_file: str = "tags.txt"
    ):
        self.folder = folder
        self.try_counts = try_counts
        self.wait_time = wait_time
        self.tags_delimiter = tags_delimiter
        self.tags_file = tags_file

    async def get_page(self, link: str, try_counts: int = 3, wait_time: int = 5) -> requests.Response | None:
        try_counter = try_counts
        while try_counter != 0:
            try_counter -= 1
            try:
                return requests.get(link)
            except requests.RequestException:
                if try_counter == 0:
                    return None

                if try_counts > 0:
                    print(f"Error, trying again after {wait_time} seconds, left {try_counter} attempt(s)")
                elif try_counts < 0:
                    print(f"Error, trying again after {wait_time} seconds")

                time.sleep(wait_time)

    def replace_denied_marks(self, string: str) -> str:
        denied_marks = {
            "/": "%2F",
            "\\": "%5C",
            "*": "%2A",
            ":": "%3A",
            "?": "%3F",
            "\"": "%22",
            "<": "%3C",
            ">": "%3E",
            "|": "%7C"
        }

        for mark, code in denied_marks.items():
            string = string.replace(mark, code)

        return string

    def get_soup(link: str) -> BeautifulSoup:
        return BeautifulSoup(.content, "html.parser")

    def get_tags(self, soup: BeautifulSoup) -> dict:
        tags = {"ID":"", "Name":"", "Parodies":"", "Characters":"", "Tags":"",
                "Artists":"", "Groups":"", "Languages":"", "Categories":"", "Pages":""}

        tags["Name"] += soup.select("h1.title")[0].text
        tags["ID"] += soup.select("#gallery_id")[0].text[1:] # From 1 because the first char is # (#123456)
        for tag_container in soup.select("div.tag-container")[:-1]: # To -1 because the last tag is Uploaded
            for name in tag_container.select("span.name"):
                tags[tag_container.contents[0].strip()[:-1]] += name.text.strip() + self.tags_delimiter # To -1 because the last char is : (Pages:)

        return tags

    def download_page(link: str, manga_folder: str):
        with open(f"{manga_folder}\\{link.split('/')[-1]}", "wb") as file:
            file.write(requests.get(link).content)

    def manga_page_parser(self, link: str, first_page: int = 1, last_page: int = None):
        soup = self.get_soup(link)
        tags = self.get_tags(soup)
        if last_page is None:
            last_page = int(tags["Pages"].strip("; ")) + 1
        manga_folder = f"{self.folder}\\{self.replace_denied_marks(tags['Name'])}"
        if not os.path.exists(manga_folder):
            os.makedirs(manga_folder)

        # Downloads pages from first_page to last_page
        for img in soup.select("img.lazyload")[first_page:last_page+1]: # From 1 because of cover, to Pages+1 because of Thumbs
            data_src = img.attrs['data-src'].split('/')
            page, extension = os.path.splitext(data_src[-1])
            img_link = f"https://i.nhentai.net/galleries/{data_src[-2]}/{page[:-1]}{extension}"

            self.download_page(img_link, manga_folder)

            # Adds manga ID to the end of each picture code
            with open(f"{manga_folder}\\{page[:-1]}{extension}", "a", encoding = "utf-8") as file:
                file.write(f"\nID:{tags['ID']}")

            print(f"{img_link} SAVED TO {manga_folder}")

        # Writes tags to a file
        with open(f"{manga_folder}\\{self.tags_file}", "w", encoding = "utf-8") as file:
            for tag, value in tags.items():
                file.write(f"{tag}: {value.strip()}\n")

    def run(self, link: str):
        self.manga_page_parser(link)

if __name__ == "__main__":
    grabber = Grabber("F:\\H")
    with open("E:\\Secret Info\\Файлы\\Циферки.txt", encoding = "utf-8") as manga_file:
        for manga in manga_file:
            grabber.run(manga.strip())
