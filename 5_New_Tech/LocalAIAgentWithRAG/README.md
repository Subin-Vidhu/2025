# LocalAIAgentWithRAG

A local implementation of a Retrieval-Augmented Generation (RAG) system for restaurant review analysis and question answering. This project demonstrates how to combine local LLMs with vector databases to create an intelligent query system for domain-specific data.

## Overview

This project implements a RAG-based question-answering system that processes restaurant reviews and answers user queries using local AI models. It leverages Ollama for LLM operations and Chroma for vector storage, making it completely independent of cloud services.

## Features

- 🤖 Local LLM integration using Ollama
- 📚 Vector database storage with Chroma
- 🔍 Intelligent context retrieval
- 💬 Interactive question-answering interface
- 📊 Restaurant review analysis
- 🏪 Persistent data storage
- 🏷️ Unique review identification system (Review #ID - 'Title' format)
- 📝 Detailed review metadata tracking
- 🌊 Real-time streaming responses for better user experience

## Prerequisites

- Python 3.x
- Ollama installed and running locally
- Sufficient storage space for vector database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/LocalAIAgentWithRAG.git
cd LocalAIAgentWithRAG
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure Ollama is running with required models:
   - mxbai-embed-large (for embeddings)
   - llama3.2 (for text generation)

## Usage

1. Start the application:
```bash
python main.py
```

2. Enter your questions when prompted
3. Type 'q' to quit the application
4. Watch as responses stream in real-time

### Example Interaction:
```
-------------------------------
Ask your question (q to quit): What are the best rated restaurants?

[Response streams in real-time, word by word]
"According to Review #5 - 'Perfect thin crust' (Rating: 5/5), the restaurant excels in..."
```

## Project Structure

```
LocalAIAgentWithRAG/
├── chrome_langchain_db/     # Vector database storage
├── realistic_restaurant_reviews.csv  # Source data
├── requirements.txt         # Project dependencies
├── vector.py               # Vector database setup
└── main.py                 # Main application logic with streaming support
```

## Detailed Code Explanation

### 1. Vector Database Setup (vector.py)

The `vector.py` file handles the creation and management of the vector database:

```python
# Key Components:
- OllamaEmbeddings: Generates embeddings using mxbai-embed-large model
- Chroma: Vector store for efficient similarity search
- Document Processing: Converts CSV data into document format with metadata
```

Key functionalities:
- Loads restaurant reviews from CSV
- Generates embeddings for each review
- Creates and maintains a persistent vector database
- Sets up a retriever with k=5 most relevant documents
- Formats reviews with unique identifiers (e.g., "Review #1 - 'Best Pizza in Town'")
- Stores comprehensive metadata including ratings, dates, titles, and review IDs

### 2. Main Application (main.py)

The `main.py` file implements the interactive QA system:

```python
# Key Components:
- OllamaLLM: Local language model integration with streaming
- ChatPromptTemplate: Structured prompt generation
- Interactive Loop: Continuous Q&A interface
- Streaming Support: Real-time response generation
```

Key functionalities:
- Initializes the LLM with llama3.2 model and streaming enabled
- Creates a specialized prompt template for restaurant-related queries
- Implements an interactive question-answering loop
- Retrieves relevant context for each query
- Generates contextual responses with specific review references
- Streams responses in real-time for better user experience
- Formats responses to include both review IDs and titles

### 3. Data Flow

1. **Input Processing**:
   - User inputs a question
   - Question is used to retrieve relevant reviews

2. **Context Retrieval**:
   - Vector database searches for similar reviews
   - Top 5 most relevant reviews are selected
   - Each review is referenced by both ID and title

3. **Response Generation**:
   - Retrieved reviews are combined with the question
   - Prompt instructs the model to reference reviews specifically
   - Responses include review IDs and titles for clear reference
   - Response is streamed in real-time to the user
   - Contextual response is generated with specific citations

## Technical Details

### Vector Database
- Uses Chroma for vector storage
- Embeddings generated using mxbai-embed-large
- Persistent storage in chrome_langchain_db/
- Retrieves 5 most similar documents per query
- Stores structured metadata for each review
- Implements unique review identification system

### Language Model
- Uses Ollama's llama3.2 model
- Runs completely locally
- Streaming support for real-time responses
- Specialized prompt template for restaurant domain
- Context-aware response generation
- Structured review referencing format

### Data Management
- Reviews stored in CSV format
- Metadata includes:
  - Review ID
  - Title
  - Rating
  - Date
- Vector embeddings persist between sessions
- Efficient retrieval system for real-time responses

## Dependencies

- langchain: Core RAG implementation
- langchain-ollama: Local LLM integration with streaming support
- langchain-chroma: Vector database management
- pandas: Data processing

## Best Practices

1. **Data Management**:
   - Keep the review database up to date
   - Regularly maintain vector database
   - Monitor embedding quality
   - Use consistent review ID-Title formatting

2. **System Performance**:
   - Adjust retrieval count (k) based on needs
   - Balance context length with response quality
   - Monitor LLM response times
   - Maintain clean review references
   - Optimize streaming buffer size if needed

3. **Query Optimization**:
   - Use specific, clear questions
   - Consider context window limitations
   - Structure complex queries appropriately
   - Reference reviews by both ID and title

## Contributing

Feel free to contribute to this project by:
- Submitting bug reports
- Proposing new features
- Improving documentation
- Adding test cases
- Enhancing review reference system
- Optimizing streaming performance

## License

[Add appropriate license information]

## Acknowledgments

- LangChain for the RAG framework
- Ollama for local LLM capabilities
- Chroma for vector database functionality