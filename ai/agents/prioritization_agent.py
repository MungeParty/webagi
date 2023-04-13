from collections import deque
from typing import List
from .base_agent import BaseAgent

class PrioritizationAgent(BaseAgent):
	def __init__(self, config, openai_api, index):
		super().__init__(config, openai_api, index)

	def prioritize_tasks(self, objective: str, task_list: List[str], next_task_id: int, user_feedback: str = ""):
		prompt = self.get_instruction().format(
			objective=objective,
			task_list=task_list,
			next_task_id=next_task_id,
			user_feedback=user_feedback)
		response = self.call(prompt)
		new_tasks = response.split('\n')
		task_list = deque()
		for task_string in new_tasks:
			task_parts = task_string.strip().split(".", 1)
			if len(task_parts) == 2:
				task_id = int(task_parts[0].strip()) # Convert the task ID to an integer
				task_name = task_parts[1].strip()
				task_list.append({"task_id": task_id, "task_name": task_name})
		return task_list
