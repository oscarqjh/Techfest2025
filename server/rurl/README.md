## Agents:

- **Web_parser**
- **Image_forgery_expert**
- **News_analyst**
- **Web_researcher**
- **Misinformation_expert**
- **Blacklist**

## Tasks:

- **Web_parsing_task**
- **Image_forgery_task**
- **News_analysis_task**
- **Web_research_task**
- **Misinformation_task**
- **Blacklist_task**

# **AI Agent System - Quick Guide**

## **Components**

1. **Agent** - The entity performing tasks.
2. **Task** - A mission assigned to an agent.
3. **Tool** - Functions used by agents to complete tasks.

## **Structure**

- **Agents** execute **Tasks**.
- **Tasks** can use **Tools** to complete their objectives.
- **Tasks** can link to other tasks through structured inputs/outputs.
- **Tools** contain functions relevant to specific tasks (e.g., `analyze_web_tool`).

## **Configuration**

- **YML Files**: Initialize default settings for agents, tasks, and tools.
  - Can be edited to add/remove configurations as needed.

## **Crew (Team Execution)**

- Combines all **Agents** into a team.
- Executes tasks **sequentially** by default.
- The final output is from the **last executed task**.

# **Installation**

Ensure you have Python >=3.10 <3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install uv:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:

```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/rurl/config/agents.yaml` to define your agents
- Modify `src/rurl/config/tasks.yaml` to define your tasks
- Modify `src/rurl/crew.py` to add your own logic, tools and specific args
- Modify `src/rurl/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the rurl Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The rurl Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.
