from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from vector import retriever
import sys

# Initialize the model with streaming enabled
model = OllamaLLM(
    model="llama3.2",
    streaming=True
)

template = """
You are an expert in answering questions about restaurants and their reviews.

Here are some relevant reviews to consider:
{reviews}

Please provide a detailed answer to this question, referencing the reviews by both their ID and title (e.g., "Review #12 - 'Perfect Crust'"): {question}

Remember to:
1. Always reference reviews using both their ID and title (e.g., "Review #5 - 'Best Pizza in Town'")
2. Include relevant ratings when discussing quality
3. Be specific about what each review praised or criticized
4. Use direct quotes from reviews when relevant
"""
prompt = ChatPromptTemplate.from_template(template)

# Create a streaming chain
chain = prompt | model | StrOutputParser()

def process_stream(chunk: str):
    """Process each chunk of the stream."""
    print(chunk, end="", flush=True)

while True:
    print("\n\n-------------------------------")
    question = input("Ask your question (q to quit): ")
    print("\n\n")
    if question == "q":
        break
    
    reviews = retriever.invoke(question)
    
    # Stream the response
    for chunk in chain.stream({"reviews": reviews, "question": question}):
        process_stream(chunk)
    print("\n")