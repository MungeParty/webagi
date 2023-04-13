import json
from typing import Any, Dict, List, Union

class AgentConfig:
	def __init__(self, config_dict: Dict[str, Union[str, Dict[str, Any]]]) -> None:
		self.config_dict = config_dict

	def load_agent_configurations(self, config_files: List[str]) -> None:
		"""
		Load agent configurations from one or more files and update the internal configuration dictionary.
		:param config_files: List of file paths or URLs to load configurations from.
		"""
		for file in config_files:
			with open(file) as f:
				data = json.load(f)
				for agent, config in data.items():
					self.config_dict[agent] = config

	def get_agent_settings(self, agent_name: str) -> Dict[str, Any]:
		"""
		Retrieve the configuration settings for a given agent.
		:param agent_name: Name of the agent to retrieve settings for.
		:return: A dictionary of configuration settings for the given agent.
		"""
		return self.config_dict.get(agent_name, {})

	def __getitem__(self, key: str) -> Dict[str, Any]:
		return self.config_dict.get(key, {})
