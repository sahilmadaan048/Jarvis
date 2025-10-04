from langchain_core.runnables.utils import Input
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.prompts import PromptTemplate
import torch

# Check if GPU is available
print(torch.cuda.is_available())
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))

# device 0 is GPU
model = pipeline(
    "text-generation",
    model="mistralai/Mistral-7B-Instruct-v0.1",
    device=0,  # note: it's device, not devices
    max_length=256,
    truncation=True,
)

llm = HuggingFacePipeline(pipeline=model)

# Create the prompt template
template = PromptTemplate.from_template("Explain {topic} in detail for a {age} year old child")

# Compose the chain
chain = template | llm

# Define inputs
topic = Input("topic")
age = Input("age")

response = chain.invoke({"topic": topic, "age": age})
print(response)
