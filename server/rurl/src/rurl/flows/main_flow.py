import asyncio
import time
import json
import os
import sys

from crewai.flow.flow import Flow, listen, start
from crewai import LLM
from tavily import TavilyClient
from pydantic import BaseModel
from dotenv import load_dotenv

from rurl.src.rurl.tools.WebParsingTask import WebParsingTask
from rurl.src.rurl.tools.WebAnalyserTask import WebAnalyserTask
from rurl.src.rurl.research_crew import ResearchRurl

load_dotenv()

class MainFlowState(BaseModel):
    web_parsed_data: dict = {}

class MainFlow(Flow[MainFlowState]):

  def __init__(self, url, **kwargs):
      super().__init__(**kwargs)
      self.url = url

  @start()
  async def web_parser_node(self):
      WebParsingTask.model_rebuild()
      task = WebParsingTask()
      data = task.run(self.url)

      # Save the parsed data to the state
      self.state.web_parsed_data = data  

      print(data)
      return data

  @listen("web_parser_node")
  async def image_forgery_node(self):
      print("forgery detection here")
      
      return "web_parser_node"
  
  @listen("web_parser_node")
  async def web_analyser_node(self, data: dict):
      WebAnalyserTask.model_rebuild()
      task = WebAnalyserTask()
      input_data = {}
      input_data["data"] = data
      data = task.run(input_data)

      print(data)
      
      return data
  
  @listen("web_analyser_node")
  async def web_search_node(self, data):
      
      # get the article body from the data
      article_body = data['article_body']

      # init tavily client
      tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

      async def run_search(section):
          print(f"Running web search for section: {section['id']}")
          return await asyncio.to_thread(tavily_client.search, f"Fact check: {section['content'][:380]}", max_results=3)

      # run web search for each article body item
      tasks = [run_search(section) for section in article_body if section['to_fact_check']]
      search_results = await asyncio.gather(*tasks)

      # append results back to article_body
      result_idx = 0
      for section in article_body:
          if section['to_fact_check']:
              section['search_results'] = search_results[result_idx]['results']
              result_idx += 1  # Increment index only for fact-checked sections
            
      # for each section, using source as context, ask llm to generate a fact-check
      input_array = []

      for section in article_body:
          if section['to_fact_check']:
              formatted_sourcelist = "\n".join(
                  f"""
title: {search_result['title']}
url: {search_result['url']}
content: {search_result['content']}
                  """ for search_result in section['search_results']
              )
              input_array.append(
                  {
                      "given_text": section['content'],
                      "source_list": formatted_sourcelist
                  }
              )


      async def run_analysis(input_data):
          class AnalysisOutput(BaseModel):
              misinformation_score: float
              explanation: str

          llm = LLM(model="gpt-4o", response_format=AnalysisOutput)

          prompt = f"""
You are an expert in analyzing text data and extracting relevant information. 
You have a keen eye for detail and can spot even the most subtle signs of misinformation.

You are given a list of sources and there contents. You are to use these sources to determine if the given text is misinformation or not.
Your output shuuld include "misinformation_score" and "explanation".
misinformation_score should be a float between 0 and 1, where 0 means no misinformation and 1 means full misinformation.
explanation should be a string explaining why the misinformation score is the way it is and should be no longer than 100 words

{input_data['source_list']}

Given text: {input_data['given_text']}
"""
          
          return await asyncio.to_thread(llm.call, prompt)

      # run analysis for each section
      tasks = [run_analysis(input_data) for input_data in input_array]
      result = await asyncio.gather(*tasks)
        
      # attach results to article body
      result_idx = 0
      for section in article_body:
          if section['to_fact_check']:
              section['fact_check'] = json.loads(result[result_idx])
              result_idx += 1  # Increment index only for fact-checked sections

      # write to file
      with open("web_search_nodes.json", "w") as f:
          json.dump(article_body, f, indent=4)
        
      return article_body

  @listen(web_search_node)
  async def source_evaluation_node(self, data):
      
      pass

if __name__ == "__main__":
    t0 = time.time()
    main_flow = MainFlow(url="https://www.straitstimes.com/opinion/forum/forum-singapores-foreign-policy-based-on-realism")
    res = asyncio.run(main_flow.kickoff_async())
    print(f"Time taken: {time.time() - t0}")
