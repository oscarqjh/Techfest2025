from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from .....tools.web_parsing_tool import WebParsingTool
from .....tools.web_analyser_tool import WebAnalyserTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Analysts():
	"""Analysts crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	# Create tools
	web_parsing_tool = WebParsingTool()
	web_analyser_tool = WebAnalyserTool()

	@agent
	def web_parser(self) -> Agent:
		return Agent(
			config=self.agents_config['web_parser'],
			tools=[self.web_parsing_tool],
			verbose=True
		)

	@agent
	def web_analyser(self) -> Agent:
		return Agent(
			config=self.agents_config['web_analyser'],
			tools=[self.web_analyser_tool],
			verbose=True
		)

	@agent
	def text_analyser(self) -> Agent:
		return Agent(
			config=self.agents_config['text_analyser'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def web_parsing_task(self) -> Task:
		return Task(
			config=self.tasks_config['web_parsing_task'],
		)

	@task
	def web_analyser_task(self) -> Task:
		return Task(
			config=self.tasks_config['web_analyser_task'],
		)
	

	# Add in config if done
	# @task
	# def text_analyser_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['text_analyser_task'],
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the Analysts crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
