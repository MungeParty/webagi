from typing import Dict
from collections import deque
from .utils.openai_utils import OpenAIAPI
from .utils.pinecone_utils import PineconeUtils
from .utils.agent_config import AgentConfig
from .agents.execution_agent import ExecutionAgent
from .agents.task_creation_agent import TaskCreationAgent
from .agents.prioritization_agent import PrioritizationAgent
from .settings import (
	PINECONE_API_KEY,
	PINECONE_ENVIRONMENT,
	OPENAI_API_KEY
)

class Agency:
	def __init__(self, config_file: str, objective: str, table_name: str, task_list: deque = None):
		# Initialize the task list
		self.task_id_counter = 1
		self.objective = objective
		self.task_list = task_list or deque()
		if len(self.task_list) == 0:
			self.add_task({"task_name": "Develop a task list"})

		# Initialize OpenAI
		self.openai_api = OpenAIAPI(OPENAI_API_KEY)

		# Initialize Pinecone
		self.pinecone_utils = PineconeUtils(PINECONE_API_KEY, PINECONE_ENVIRONMENT)
		self.pinecone_utils.initialize()

		# Create and connect to the Pinecone index
		self.pinecone_utils.create_index(table_name)
		self.index = self.pinecone_utils.connect_index(table_name)

		# Load the agent configurations
		self.config = AgentConfig({})
		self.config.load_agent_configurations([config_file])

		# Initialize the agents
		self.execution_agent = ExecutionAgent(
			self.config['execution_agent'],
			self.openai_api,
			self.index)

		self.task_creation_agent = TaskCreationAgent(
			self.config['task_creation_agent'],
			self.openai_api,
			self.index)

		self.prioritization_agent = PrioritizationAgent(
			self.config['prioritization_agent'],
			self.openai_api,
			self.index)

	def add_task(self, task: Dict):
		self.task_id_counter += 1
		task.update({"task_id": self.task_id_counter})
		self.task_list.append(task)

	def run(self):
		# Completes one iteration of the agency loop
		if self.task_list:
			# Print the task list
			print("\033[95m\033[1m"+"\n*****TASK LIST*****\n"+"\033[0m\033[0m")
			for t in self.task_list:
				print(str(t['task_id'])+": "+t['task_name'])

			# Step 1: Pull the first task
			task = self.task_list.popleft()
			print("\033[92m\033[1m"+"\n*****NEXT TASK*****\n"+"\033[0m\033[0m")
			print(str(task['task_id'])+": "+task['task_name'])

			# Send to execution function to complete the task based on the context
			result = self.execution_agent.execute_task(
				self.objective,
				task["task_name"])

			this_task_id = int(task["task_id"])
			print("\033[93m\033[1m"+"\n*****TASK RESULT*****\n"+"\033[0m\033[0m")
			print(result)

			# Step 2: Enrich result and store in Pinecone
			enriched_result = {'data': result} # This is where you should enrich the result if needed
			result_id = f"result_{task['task_id']}"
			vector = enriched_result['data'] # extract the actual result from the dictionary
			self.index.upsert([(
				result_id,
				self.openai_api.get_ada_embedding(vector),
				{"task":task['task_name'],"result":result})])

		# Step 3: Create new tasks
		new_tasks = self.task_creation_agent.create_tasks(
			self.objective, 
			enriched_result,
			task["task_name"],
			[t["task_name"] for t in self.task_list])

		# Step 4: Add new tasks to the task list
		for new_task in new_tasks:
			self.task_id_counter += 1
			new_task.update({"task_id": self.task_id_counter})
			self.add_task(new_task)

		# Step 5: Prioritize the task list
		self.task_list = self.prioritization_agent.prioritize_tasks(
			self.objective,
			this_task_id,
			[t["task_name"] for t in self.task_list])
