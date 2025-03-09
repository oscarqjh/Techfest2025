from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class MisinformationOutput(BaseModel):
  """Output schema for Misinformation"""
  misinfomation_score: float
  explaination: str

@CrewBase
class ResearchRurl():
	"""ResearchRurl crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/research_agents.yaml'
	tasks_config = 'config/research_tasks.yaml'

	@agent
	def misinformation_expert(self) -> Agent:
		return Agent(
			config=self.agents_config['misinformation_expert'],
			verbose=True,
		)
	
	
	@task
	def misinformation_task(self) -> Task:
		return Task(
			config=self.tasks_config['misinformation_task'],
			output_pydantic=MisinformationOutput,
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
		)
