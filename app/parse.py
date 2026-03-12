import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass


URL = "https://mate.academy/en/"


@dataclass
class Course:
    name: str
    short_description: str
    duration: str


def get_page(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    return response.text


def parse_courses(html: str) -> list[Course]:
    soup = BeautifulSoup(html, "html.parser")
    courses: list[Course] = []

    career_blocks = soup.select("section h3")

    for block in career_blocks:
        name = block.get_text(strip=True)

        parent = block.parent
        text = parent.get_text(" ", strip=True)

        duration = ""
        short_description = ""

        words = text.split()

        for i, word in enumerate(words):
            if "+" in word and "month" in words[i + 1]:
                duration = f"{word} {words[i + 1]}"
                break

        if duration:
            short_description = text.split(duration)[-1].strip()

        if name and short_description:
            courses.append(
                Course(
                    name=name,
                    short_description=short_description,
                    duration=duration,
                )
            )

    return courses


def get_all_courses() -> list[Course]:
    html = get_page(URL)
    return parse_courses(html)