from typing import Dict, List
from .base_agent import BaseAgent

class TaskCreationAgent(BaseAgent):
	def __init__(self, config, openai_api, index):
		super().__init__(config, openai_api, index)

	def create_tasks(self, objective: str, task: str, result: Dict, task_list: List[str], user_feedback: str = ""):
		prompt = self.get_instruction().format(
    	objective=objective,
			task=task,
			result=result,
			task_list=task_list,
			user_feedback=user_feedback)
		response = self.call(prompt)
		new_tasks = response.split('\n')
		return [{"task_name": task_name} for task_name in new_tasks]
