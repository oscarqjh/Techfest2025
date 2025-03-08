#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from .crews.poem_crew.poem_crew import PoemCrew

from .crews.analysts.src.analysts.analysts import Analysts
from .crews.image_forensics.src.image_forensics.image_forensics import ImageForensics
from .crews.researchers.src.researchers.researchers import Researchers
from .crews.validators.src.validators.validators import Validators


class RURLState(BaseModel):
    weblink: str
    title: str
    content: str
    image_links: list[str]
    date: str


class RURLFlow(Flow[RURLState]):

    @start()
    def parse_web_article(self, weblink: str):
        print("Parsing contents of the web article: ", self.state.weblink)
        result = (
            Analysts()
            .web_parsing_task()
            .kickoff(inputs={"url": self.state.weblink})
        )
        self.title = result.title
        self.content = result.content
        self.image_links = result.image_links
        self.date = result.date

    @listen(parse_web_article)
    def analyse_article(self):
        print("Analysing the article")
        result = (
            Researchers()
            .article_analysis_task()
            .kickoff(inputs={"body": self.state.content})
        )
    
    def analyse_image_and_text(self):
        print("Analysing the image and text")
        result = (
            ImageForensics()
            .image_text_analysis_task()
            .kickoff(inputs={"url": self.state.w})
        )

    def detect_forgery(self):
        print("Analysing image for forgery or deepfakes")
        result = (
            ImageForensics()
            .crew()
            .kickoff(inputs={"image_links": self.state.image_urls})
        )

    def generate_poem(self):
        print("Generating poem")
        result = (
            PoemCrew()
            .crew()
            .kickoff(inputs={"sentence_count": self.state.sentence_count})
        )

        print("Poem generated", result.raw)
        self.state.poem = result.raw

    @listen(generate_poem)
    def save_poem(self):
        print("Saving poem")
        with open("poem.txt", "w") as f:
            f.write(self.state.poem)


def kickoff():
    poem_flow = PoemFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = PoemFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
