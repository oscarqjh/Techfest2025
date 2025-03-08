#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, and_

from .crews.analysts.src.analysts.analysts import Analysts
from .crews.image_forensics.src.image_forensics.image_forensics import ImageForensics
from .crews.researchers.src.researchers.researchers import Researchers
from .crews.validators.src.validators.validators import Validators

from .crews.analysts.src.analysts.tools.WebParsingTask import WebParsingTask
from .crews.analysts.src.analysts.tools.WebAnalyserTask import WebAnalyserTask


class RURLState(BaseModel):
    weblink: str = ""
    domain: str = ""
    title: str = ""
    content: str = ""
    image_links: list[str] = []
    date: str = ""

class RURLFlow(Flow[RURLState]):

    @start()
    def parse_web(self):
        print("Parsing contents of the web article: ", self.state.weblink)

        web_parser = WebParsingTask()
        result = web_parser._run(self.state.weblink)
        print("Result = ",  result)
        self.state.title = result.title
        self.state.content = result.content
        self.state.image_links = result.image_links
        self.state.date = result.date

    @listen(parse_web)
    async def web_analyse(self):
        print("Analysing the web article")
        web_analyser = WebAnalyserTask()
        result = await web_analyser._run(self.state.content)
        self.state.web_analyse_results = result

    # Analysts crew
    @listen(parse_web)
    def analyse_image_and_text(self):
        print("Analysing the image and text")
        result = (
            Analysts()
            .crew()
            .kickoff(inputs={"url": self.state.w})
        )
        self.state.analysed_image_text_results = result
    
    # Image Forensics crew
    @listen(parse_web)
    async def detect_forgery(self):
        print("Analysing image for forgery or deepfakes")
        result = await (
            ImageForensics()
            .crew()
            .kickoff_async(inputs={"image_links": self.state.image_urls})
        )
        self.state.forgery_results = result

    # Validator crew
    @listen(parse_web)
    async def internal_validation(self):
        print("Validating source credibility")
        result = await (
            Validators()
            .crew()
            .kickoff_async(inputs={"domain": self.state.domain})
        )
        self.state.internal_validation_results = result # is_blacklisted, is_credible

    # Researchers crew
    @listen(web_analyse)
    async def web_research(self):
        print("Generating fact checks")
        result = await (
            Researchers()
            .crew()
            .kickoff(inputs={"content": self.state.content})
        )
        self.state.web_research_results = result

    @listen(and_(analyse_image_and_text, detect_forgery, internal_validation, web_research))
    def generate_insights(self):
        print("Generating insights on the credibility of the article")
        


def kickoff():
    rurl_flow = RURLFlow()
    rurl_flow.kickoff(inputs={"weblink":"https://www.example.com"})


def plot():
    rurl_flow = RURLFlow()
    rurl_flow.plot()

if __name__ == "__main__":
    kickoff()
