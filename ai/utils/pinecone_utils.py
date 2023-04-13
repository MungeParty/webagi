import pinecone

class PineconeUtils:
	def __init__(self, api_key: str, environment: str):
		self.api_key = api_key
		self.environment = environment
		self.index = None

	def initialize(self):
		pinecone.init(api_key=self.api_key, environment=self.environment)

	def create_index(self, index_name: str, dimension: int = 1536, metric: str = "cosine", pod_type: str = "p1"):
		if index_name not in pinecone.list_indexes():
			pinecone.create_index(index_name, dimension=dimension, metric=metric, pod_type=pod_type)

	def connect_index(self, index_name: str):
		self.index = pinecone.Index(index_name)
		return self.index

	def deinitialize(self):
		pinecone.deinit()
