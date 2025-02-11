# Section D: RAG and Vector Databases

## Q32: Explain Retrieval-Augmented Generation (RAG)

**Answer:**
RAG is a hybrid approach that combines retrieval-based and generative methods to produce more accurate and contextually relevant responses.

**Implementation Example:**
```python
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration
import torch

def setup_rag_model():
    # Initialize RAG components
    tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
    retriever = RagRetriever.from_pretrained(
        "facebook/rag-sequence-nq",
        index_name="exact",
        use_dummy_dataset=True
    )
    model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")
    
    return model, tokenizer, retriever

def generate_rag_response(question, model, tokenizer, retriever):
    # Encode input
    inputs = tokenizer(question, return_tensors="pt")
    
    # Generate response
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            max_length=200
        )
    
    # Decode response
    generated_text = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return generated_text[0]
```

## Q33: Vector Databases and Their Role in RAG

**Answer:**
Vector databases store and efficiently retrieve high-dimensional vector representations of data, crucial for semantic search and RAG systems.

**Implementation Example using FAISS:**
```python
import numpy as np
import faiss

class VectorDatabase:
    def __init__(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.texts = []
    
    def add_documents(self, documents, embeddings):
        """
        Add documents and their embeddings to the database
        """
        self.index.add(embeddings)
        self.texts.extend(documents)
    
    def search(self, query_embedding, k=5):
        """
        Search for similar documents
        """
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1),
            k
        )
        return [
            (self.texts[i], distances[0][idx])
            for idx, i in enumerate(indices[0])
        ]

# Usage example
def setup_vector_db():
    # Initialize vector database
    db = VectorDatabase(dimension=768)  # BERT embedding dimension
    
    # Add sample documents
    documents = ["Sample text 1", "Sample text 2"]
    embeddings = np.random.rand(2, 768).astype('float32')
    db.add_documents(documents, embeddings)
    
    return db
```

## Q34: Semantic Search Implementation

**Answer:**
Semantic search uses vector embeddings to find relevant documents based on meaning rather than exact keyword matches.

```python
from sentence_transformers import SentenceTransformer
import numpy as np

class SemanticSearch:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.vector_db = None
    
    def index_documents(self, documents):
        # Generate embeddings
        embeddings = self.model.encode(documents)
        
        # Initialize and populate vector database
        self.vector_db = VectorDatabase(dimension=embeddings.shape[1])
        self.vector_db.add_documents(documents, embeddings)
    
    def search(self, query, k=5):
        # Generate query embedding
        query_embedding = self.model.encode(query)
        
        # Search vector database
        results = self.vector_db.search(query_embedding, k)
        return results

# Usage
def semantic_search_example():
    searcher = SemanticSearch()
    
    # Index documents
    documents = [
        "Machine learning is a subset of artificial intelligence",
        "Natural language processing deals with text and speech",
        "Deep learning uses neural networks for complex tasks"
    ]
    searcher.index_documents(documents)
    
    # Perform search
    results = searcher.search("AI and ML concepts")
    return results
```

## Q35: Hybrid Search Systems

**Answer:**
Hybrid search combines multiple search approaches (keyword-based, semantic, etc.) for better results.

```python
from rank_bm25 import BM25Okapi
from nltk.tokenize import word_tokenize

class HybridSearch:
    def __init__(self):
        self.semantic_search = SemanticSearch()
        self.documents = []
        self.bm25 = None
    
    def index_documents(self, documents):
        self.documents = documents
        
        # Index for semantic search
        self.semantic_search.index_documents(documents)
        
        # Index for keyword search
        tokenized_docs = [word_tokenize(doc.lower()) for doc in documents]
        self.bm25 = BM25Okapi(tokenized_docs)
    
    def search(self, query, k=5, semantic_weight=0.7):
        # Semantic search
        semantic_results = self.semantic_search.search(query, k)
        semantic_scores = {doc: score for doc, score in semantic_results}
        
        # Keyword search
        tokenized_query = word_tokenize(query.lower())
        keyword_scores = self.bm25.get_scores(tokenized_query)
        
        # Combine scores
        final_scores = []
        for idx, doc in enumerate(self.documents):
            semantic_score = semantic_scores.get(doc, 0)
            keyword_score = keyword_scores[idx]
            
            combined_score = (
                semantic_weight * semantic_score +
                (1 - semantic_weight) * keyword_score
            )
            final_scores.append((doc, combined_score))
        
        # Sort and return top k results
        return sorted(final_scores, key=lambda x: x[1], reverse=True)[:k]
```

## Q36: Vector Database Optimization

**Answer:**
Techniques to optimize vector database performance:

1. **Indexing Strategies:**
```python
import faiss

def create_optimized_index(dimension, n_lists=100):
    # Create IVF index for faster search
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFFlat(
        quantizer,
        dimension,
        n_lists,
        faiss.METRIC_L2
    )
    return index

def create_compressed_index(dimension, n_lists=100):
    # Create IVF-PQ index for memory efficiency
    quantizer = faiss.IndexFlatL2(dimension)
    index = faiss.IndexIVFPQ(
        quantizer,
        dimension,
        n_lists,
        8,  # M = number of sub-vectors
        8   # nbits = bits per sub-vector
    )
    return index
```

2. **Batch Processing:**
```python
def batch_process_documents(documents, batch_size=1000):
    """Process documents in batches to manage memory"""
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        embeddings = generate_embeddings(batch)
        index.add(embeddings)
```

3. **Sharding:**
```python
class ShardedVectorDB:
    def __init__(self, dimension, n_shards=3):
        self.shards = [
            VectorDatabase(dimension)
            for _ in range(n_shards)
        ]
    
    def add_documents(self, documents, embeddings):
        # Distribute documents across shards
        for i, (doc, emb) in enumerate(zip(documents, embeddings)):
            shard_idx = i % len(self.shards)
            self.shards[shard_idx].add_documents([doc], emb.reshape(1, -1))
    
    def search(self, query_embedding, k=5):
        # Search all shards and merge results
        all_results = []
        for shard in self.shards:
            results = shard.search(query_embedding, k)
            all_results.extend(results)
        
        # Sort and return top k
        return sorted(all_results, key=lambda x: x[1])[:k]
```

[Continue with remaining questions...] 