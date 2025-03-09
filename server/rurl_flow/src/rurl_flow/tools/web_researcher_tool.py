import asyncio
import json
import os
from pydantic import BaseModel

from crewai import LLM
from tavily import TavilyClient

async def web_search_node(data):
      
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
