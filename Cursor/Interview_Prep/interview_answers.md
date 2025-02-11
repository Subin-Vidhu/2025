# AI/ML Technical Interview Questions & Answers

## Table of Contents
1. Artificial Neural Networks (ANN)
2. Natural Language Processing (NLP)
3. Transformers and Extended Architecture
4. Large Language Models (LLMs)
5. RAG and Multimodal RAG
6. Fine-tuning and Model Optimization
7. Vector Databases
8. LLMOps & System Design
9. Evaluation Methods

## 1. Artificial Neural Networks (ANN)

Q: What is an Artificial Neural Network, and how does it work?
A: An Artificial Neural Network (ANN) is a computational model inspired by the human brain's biological neural networks. It consists of:
- Input Layer: Receives raw data
- Hidden Layers: Processes information
- Output Layer: Produces final results

Example implementation:
```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(10,)),
    tf.keras.layers.Dense(32, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
```

Q: What are activation functions, and what are their types?
A: Activation functions introduce non-linearity into neural networks. Common types include:

1. ReLU (Rectified Linear Unit):
```python
def relu(x):
    return max(0, x)
```
- Most commonly used
- Prevents vanishing gradient

2. Sigmoid:
```python
def sigmoid(x):
    return 1 / (1 + np.exp(-x))
```
- Used for binary classification
- Output range: [0,1]

[Previous code examples remain for other activation functions...]

Q: How do you handle class imbalance in machine learning models?
A: There are several strategies:

1. Resampling:
```python
from imblearn.over_sampling import SMOTE

def balance_dataset(X, y):
    smote = SMOTE(random_state=42)
    X_balanced, y_balanced = smote.fit_resample(X, y)
    return X_balanced, y_balanced
```

2. Class Weights:
```python
from sklearn.utils.class_weight import compute_class_weight

weights = compute_class_weight('balanced', 
                             classes=np.unique(y), 
                             y=y)
model.fit(X, y, class_weight=dict(enumerate(weights)))
```

## 2. Natural Language Processing (NLP)

Q: What is tokenization? How does it differ from lemmatization and stemming?
A: These are text preprocessing techniques:

1. Tokenization: Breaks text into tokens
```python
from nltk.tokenize import word_tokenize
text = "I love NLP!"
tokens = word_tokenize(text)  # ['I', 'love', 'NLP', '!']
```

2. Lemmatization vs Stemming:
```python
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Lemmatization preserves meaning
print(lemmatizer.lemmatize("better"))  # "good"
# Stemming just truncates
print(stemmer.stem("better"))  # "bet"
```

[Previous code examples remain for other NLP concepts...]

## 3. Transformers and Extended Architecture

Q: What problems do transformer models solve that RNNs cannot?
A: Transformers address several RNN limitations:
1. Parallel Processing: Can process entire sequences simultaneously
2. Long-range Dependencies: Self-attention mechanism captures global context
3. No Vanishing Gradient: Direct connections between any positions

Example of self-attention:
```python
def self_attention(query, key, value):
    scores = tf.matmul(query, key, transpose_b=True)
    scaled_scores = scores / tf.math.sqrt(tf.cast(tf.shape(key)[-1], tf.float32))
    weights = tf.nn.softmax(scaled_scores, axis=-1)
    return tf.matmul(weights, value)
```

[Previous transformer-related code examples remain...]

## 4. Large Language Models (LLMs)

Q: What is the difference between pre-training and fine-tuning in LLMs?
A: 
- Pre-training: Initial training on large corpus of text
- Fine-tuning: Adapting pre-trained model for specific tasks

Example of fine-tuning:
```python
from transformers import AutoModelForSequenceClassification

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2
)

trainer = Trainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    compute_metrics=compute_metrics
)
```

## 5. RAG and Multimodal RAG

Q: What is Retrieval-Augmented Generation (RAG)?
A: RAG combines retrieval and generation:
```python
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

def setup_rag():
    tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
    retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq")
    model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")
    return tokenizer, retriever, model
```

[Previous RAG-related code examples remain...]

## 6. Vector Databases

Q: How do vector databases differ from traditional databases?
A: Vector databases are optimized for similarity search:
```python
import faiss

# Create index
dimension = 128
index = faiss.IndexFlatL2(dimension)

# Add vectors
vectors = np.random.random((1000, dimension)).astype('float32')
index.add(vectors)

# Search
query = np.random.random((1, dimension)).astype('float32')
D, I = index.search(query, k=5)
```

[Previous vector database examples remain...]

## 7. Evaluation Methods

Q: What metrics would you use to evaluate an LLM?
A: Common metrics include:
```python
def evaluate_llm(predictions, references):
    metrics = {
        'bleu': calculate_bleu(predictions, references),
        'rouge': calculate_rouge(predictions, references),
        'perplexity': calculate_perplexity(model, test_data),
        'human_eval_score': human_evaluation(predictions)
    }
    return metrics
```

[Previous evaluation code examples remain...]

## 8. System Design and Best Practices

Q: How would you design a scalable LLM-based system?
A: Key considerations:
1. Model Serving:
```python
from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()
model = pipeline('text-generation')

@app.post("/generate")
async def generate_text(prompt: str):
    return {"response": model(prompt)[0]['generated_text']}
```

2. Load Balancing:
```python
from concurrent.futures import ThreadPoolExecutor

class ModelServer:
    def __init__(self, num_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.models = [load_model() for _ in range(num_workers)]
    
    async def process_request(self, prompt):
        return await self.executor.submit(self.models[worker_id].generate, prompt)
```

## Best Practices and Tips

1. Model Development:
- Start simple, add complexity as needed
- Use appropriate evaluation metrics
- Document code and decisions
- Version control models and data

2. Deployment:
- Implement proper error handling
- Set up monitoring and logging
- Plan for scalability
- Have fallback mechanisms

3. Maintenance:
- Regular model retraining
- Monitor for drift
- Keep dependencies updated
- Maintain test coverage

Remember:
- Stay updated with research
- Consider ethical implications
- Focus on practical applications
- Document thoroughly 