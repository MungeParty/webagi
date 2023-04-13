import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")

# Set Pinecone environment
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
