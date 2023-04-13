from typing import Dict
from pinecone import Index
from ..utils.openai_utils import OpenAIAPI

class BaseAgent:
    def __init__(self, config: Dict, openai_api: OpenAIAPI, index: Index):
        self.openai_api = openai_api
        self.index = index
        self.config = config
    
    def call(self, prompt: str):
        self.openai_api.call(
            prompt,
            model=self.config['model'],
            temperature=self.config['temperature'],
            max_tokens=self.config['max_tokens'])

    def get_instruction(self):
        return str(self.config['instruction'])
    
    def get_embedding(self, query: str):
        return self.openai_api.get_ada_embedding(query)
    
    def get_context(self, query: str, n: int):
        query_embedding = self.get_embedding(query)
        results = self.index.query(query_embedding, top_k=n, include_metadata=True)
        sorted_results = sorted(results.matches, key=lambda x: x.score, reverse=True)
        return [(str(item.metadata['task'])) for item in sorted_results]
