import os
from openai import OpenAI


# Read Azure OpenAI configuration from environment variables
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_key = os.environ["AZURE_OPENAI_API_KEY"]
deployment = os.environ["AZURE_OPENAI_DEPLOYMENT"]


# Create Azure OpenAI client
client = OpenAI(
    api_key=api_key,
    base_url=endpoint.rstrip("/") + "/",
)


# Send a simple request to GPT-4.1-mini
response = client.responses.create(
    model=deployment,
    input="Explain what Kubernetes CrashLoopBackOff means in one simple paragraph.",
)


# Print the model response
print("Response:")
print(response.output_text)