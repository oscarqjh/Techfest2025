from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Rurl():
	"""Rurl crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def web_parser(self) -> Agent:
		return Agent(
			config=self.agents_config['web_parser'],
			verbose=True
		)

	@agent
	def image_forgery_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['image_forgery_expert'],
			verbose=True
		)

	@agent
	def news_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['news_analyst'],
			verbose=True
		)

	@agent
	def web_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['web_researcher'],
			verbose=True
		)

	@agent
	def misinformation_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['misinformation_expert'],
			verbose=True,
			# llm = LLM(
			# 	model="openai/gpt-4o-mini",
			# 	temperature=0.2,
			# 	# response_format=MisinformationToolOutput # Uncomment after importing all tool output classes
        	# )
		)
	
	@agent
	def blacklister(self) -> Agent:
		return Agent(
			config=self.agents_config['blacklister'],
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
	def image_forgery_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_forgery_task'],
		)
	
	@task
	def news_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['news_analysis_task'],
		)
	
	@task
	def web_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['web_research_task'],
		)
	
	@task
	def misinformation_task(self) -> Task:
		return Task(
			config=self.tasks_config['misinformation_task'],
		)

	@task
	def blacklist_task(self) -> Task:
		return Task(
			config=self.tasks_config['blacklist_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Rurl crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
