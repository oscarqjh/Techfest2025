#!/usr/bin/env python
from random import randint
import sys
import time
import asyncio

from pydantic import BaseModel

from crewai.flow import Flow, listen, start, and_

from .crews.analysts.src.analysts.analysts import Analysts
from .crews.forensics.src.forensics.forensics import ImageForensics
from .crews.researchers.src.researchers.researchers import Researchers
from .crews.validators.src.validators.validators import Validators
from .crews.insights.src.insights.insights import Insights

from .tools.web_parsing_tool import WebParsingTool
from .tools.web_analyser_tool import WebAnalyserTool
from .tools.web_researcher_tool import web_search_node
import json


class RURLState(BaseModel):
    domain: str = ""
    title: str = ""
    content: str = ""
    image_urls: list[str] = []
    date: str = ""
    parsed_web_results: dict = {}
    web_analyse_results: dict = {}
    analysed_image_text_results: dict = {}
    forgery_results: dict = {}
    internal_validation_results: dict = {}
    web_research_results: dict = {}
    insights: dict = {}

class RURLFlow(Flow[RURLState]):

    def __init__(self, url, **kwargs):
      super().__init__(**kwargs)
      self.url = url

    @start()
    async def parse_web(self):
        print("Parsing contents of the web article: ", self.url)

        web_parser = WebParsingTool()
        result = web_parser._run(self.url)
        # Update states
        self.state.title = result.get("title","")
        self.state.content = result.get("content","")
        self.state.image_urls = result.get("image_urls",[])
        self.state.date = result.get("date","")
        self.state.parsed_web_results = {"parsed_web_results":result} # Save results into state
        print("PARSE WEB: ",result)
        return result

    @listen(parse_web)
    async def web_analyse(self, data: dict):
        print("Analysing the web article")
        web_analyser = WebAnalyserTool()

        # Input data from parse_web
        analyser_input = {
            "data": {
                "title": self.state.title,
                "weblink": self.url,
                "image_urls": self.state.image_urls,
                "content": self.state.content,
                "date": self.state.date
            }
        }
        # input_data = {}
        # input_data["data"] = data

        result = web_analyser._run(analyser_input)
        self.state.web_analyse_results = {"web_analyse_results":result} # Save results into state
        print("ANALYSE: ",result)
        return result

    # # Analysts crew
    # @listen(parse_web)
    # def analyse_image_and_text(self):
    #     print("Analysing the image and text")
    #     result = (
    #         Analysts()
    #         .crew()
    #         .kickoff(inputs={"url": self.url})
    #     )
    #     self.state.analysed_image_text_results = {"analysed_image_text_results":result.model_dump()} # Save results into state
    #     print("ANALYSTS: ",result)
    
    # Image Forensics crew
    @listen(parse_web)
    async def detect_forgery(self):
        print("Analysing image for forgery or deepfakes")
        result = await (
            ImageForensics()
            .crew()
            .kickoff_async(inputs={"image_urls": self.state.image_urls})
        )
        self.state.forgery_results = {"forgery_results":result.model_dump()} # Save results into state
        print("FORGERY: ",result)

    # Validator crew
    @listen(parse_web)
    async def internal_validation(self):
        print("Validating source credibility")
        result = await (
            Validators()
            .crew()
            .kickoff_async(inputs={"domain": self.state.domain})
        )
        self.state.internal_validation_results = {"internal_validation_results":result.model_dump()} # Save results into state - ['blacklisted', 'likely_credible', 'unreliable']
        print("VALIDATE: ",result)

    # Researchers crew
    @listen(web_analyse)
    async def web_research(self, data: dict):
        print("Generating fact checks")

        # run web search
        result = await web_search_node(data)

        # append result
        self.state.web_research_results = {"web_research_results":result} # Save results into state
        print("RESEARCH: ",result)

    @listen(and_(detect_forgery, internal_validation, web_research))
    def generate_insights(self):
        print("Generating insights on the credibility of the article")
        result = (
            Insights()
            .crew()
            .kickoff(inputs={
                "credibility": self.state.internal_validation_results,
                "cross_references": self.state.web_research_results
            })
        )
        self.state.insights = result.model_dump() # Save results into state
    
    @listen(generate_insights)
    def return_results(self):
        print("Returning results")
        resulting_dict = {
            "url": self.url,
            "title": self.state.title,
            "date": self.state.date,
            "parsed_web_results": self.state.parsed_web_results,
            "web_analyse_results": self.state.web_analyse_results,
            "analysed_image_text_results": self.state.analysed_image_text_results,
            "forgery_results": self.state.forgery_results,
            "internal_validation_results": self.state.internal_validation_results,
            "web_research_results": self.state.web_research_results,
            "insights": self.state.insights
        }

        with open("results.json", "w") as f:
            json.dump(resulting_dict, f, indent=4)
        return resulting_dict


def kickoff(url):
    t0 = time.time()
    rurl_flow = RURLFlow(url=url)
    res = asyncio.run(rurl_flow.kickoff_async())

    print("Time taken = ", time.time()-t0)

def plot():
    rurl_flow = RURLFlow()
    rurl_flow.plot()

if __name__ == "__main__":
    kickoff()
