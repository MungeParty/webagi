from .base_agent import BaseAgent

class ExecutionAgent(BaseAgent):
	def __init__(self, config, openai_api, index):
		super().__init__(config, openai_api, index)

	def execute_task(self, objective: str, task: str):
		context = self.get_context(query=objective, n=5)
		prompt = self.get_instruction().format(
			objective=objective,
			task=task,
			context=context)
		return self.call(prompt)
