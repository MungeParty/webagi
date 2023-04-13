import openai

class OpenAIAPI:
	def __init__(self, api_key, default_model:str='gpt-3.5-turbo', default_temperature=0.5, default_max_tokens=100):
		self.api_key = api_key
		self.default_model = default_model
		self.default_temperature = default_temperature
		self.default_max_tokens = default_max_tokens
		openai.api_key = api_key

	def call(self, prompt, model=None, temperature=None, max_tokens=None):
		model = model or self.default_model
		temperature = temperature or self.default_temperature
		max_tokens = max_tokens or self.default_max_tokens

		try:
			if not model.startswith('gpt-'):
				# Use completion API
				response = openai.Completion.create(
					engine=model,
					prompt=prompt,
					temperature=temperature,
					max_tokens=max_tokens,
					top_p=1,
					frequency_penalty=0,
					presence_penalty=0,
					subject	= "AI",
				)
				return response.choices[0].text.strip()
			else:
				# Use chat completion API
				messages=[{"role": "user", "content": prompt}]
				response = openai.ChatCompletion.create(
					model=model,
					messages=messages,
					temperature=temperature,
					max_tokens=max_tokens,
					n=1,
					stop=None,
				)
				return response.choices[0].message.content.strip()
		except Exception as e:
			print(f"Error during OpenAI API call: {e}")
			return None

	def get_ada_embedding(self, text):
		text = text.replace("\n", " ")
		try:
			return openai.Embedding.create(input=[text], model="text-embedding-ada-002")["data"][0]["embedding"]
		except Exception as e:
			print(f"Error during ADA embedding: {e}")
			return None
