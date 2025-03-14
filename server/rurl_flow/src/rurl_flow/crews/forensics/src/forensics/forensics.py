from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from .tools.detect_forgery_tool import DetectForgeryTool
from .tools.image_websearch_tool import ImageWebsearchTool 

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class ImageForensics():
	"""ImageForensics crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	# Create tools
	detect_forgery_tool = DetectForgeryTool()
	image_websearch_tool = ImageWebsearchTool() 

	@agent
	def image_forgery_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['image_forgery_expert'],
			tools=[self.detect_forgery_tool],
			verbose=True
		)
  
	@agent
	def image_websearch_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['image_websearch_expert'],
			tools=[self.image_websearch_tool],  # Assign web search tool
			verbose=True
		)
	
	@agent
	def forensics_compiler(self) -> Agent:
		return Agent(
			config=self.agents_config['forensics_compiler'],
			verbose=True
		)
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def image_forgery_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_forgery_task']
		)
	@task
	def image_websearch_task(self) -> Task:
		return Task(
			config=self.tasks_config['image_websearch_task']
		)

	@task
	def compile_forensics_task(self) -> Task:
		return Task(
			config=self.tasks_config['compile_forensics_task']
		)
		
	@crew
	def crew(self) -> Crew:
		"""Creates the ImageForensics crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

  
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
