#!/usr/bin/env python
from random import randint
import sys

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, and_

from .crews.analysts.src.analysts.analysts import Analysts
from .crews.image_forensics.src.image_forensics.image_forensics import ImageForensics
from .crews.researchers.src.researchers.researchers import Researchers
from .crews.validators.src.validators.validators import Validators

from .tools.web_parsing_tool import WebParsingTool
from .tools.web_analyser_tool import WebAnalyserTool
from .tools.web_researcher_tool import web_search_node


class RURLState(BaseModel):
    weblink: str = ""
    domain: str = ""
    title: str = ""
    content: str = ""
    image_urls: list[str] = []
    date: str = ""
    web_analyse_results: dict = {}
    analysed_image_text_results: dict = {}
    forgery_results: dict = {}
    internal_validation_results: dict = {}
    web_research_results: dict = {}

class RURLFlow(Flow[RURLState]):

    @start()
    def parse_web(self):
        print("Parsing contents of the web article: ", self.state.weblink)

        web_parser = WebParsingTool()
        result = web_parser._run(self.state.weblink)
        print("Result = ",  result)
        self.state.title = result.get("title","")
        self.state.content = result.get("content","")
        self.state.image_urls = result.get("image_links",[])
        self.state.date = result.get("date","")

    @listen(parse_web)
    async def web_analyse(self):
        print("Analysing the web article")
        web_analyser = WebAnalyserTool()
        analyser_input = {
            "data": {
                "title": self.state.title,
                "weblink": self.state.weblink,
                "image_urls": self.state.image_urls,
                "content": self.state.content,
                "date": self.state.date
            }
        }

        result = await web_analyser._run(analyser_input)
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

        # get article body from data
        article_body = self.state.web_analyse_results['article_body']

        # run web search
        result = await web_search_node(article_body)

        # append result
        self.state.web_research_results = result

    @listen(and_(analyse_image_and_text, detect_forgery, internal_validation, web_research))
    def generate_insights(self):
        print("Generating insights on the credibility of the article")
        

def kickoff():
    rurl_flow = RURLFlow()
    rurl_flow.kickoff(inputs={"weblink":"https://www.straitstimes.com/opinion/forum/forum-singapores-foreign-policy-based-on-realism"})


def plot():
    rurl_flow = RURLFlow()
    rurl_flow.plot()

if __name__ == "__main__":
    kickoff()
