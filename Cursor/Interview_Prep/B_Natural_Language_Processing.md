# Section B: Classical Natural Language Processing

## Q15: What is tokenization? Give me a difference between lemmatization and stemming?

**Answer:**
Tokenization is the process of breaking text into smaller units (tokens) such as words or subwords. Lemmatization and stemming are text normalization techniques that reduce words to their base or root form.

**Implementation Examples:**

1. **Tokenization:**
```python
from nltk.tokenize import word_tokenize, sent_tokenize

# Word tokenization
text = "Natural language processing is fascinating!"
word_tokens = word_tokenize(text)
print(word_tokens)  # ['Natural', 'language', 'processing', 'is', 'fascinating', '!']

# Sentence tokenization
text = "First sentence. Second sentence. Third sentence."
sent_tokens = sent_tokenize(text)
print(sent_tokens)  # ['First sentence.', 'Second sentence.', 'Third sentence.']
```

2. **Lemmatization vs Stemming:**
```python
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

# Example words
words = ['running', 'better', 'fishing', 'argued', 'flies']

# Lemmatization
lemmas = [lemmatizer.lemmatize(word) for word in words]
print("Lemmatization:", lemmas)  
# Output: ['running', 'better', 'fishing', 'argued', 'fly']

# Stemming
stems = [stemmer.stem(word) for word in words]
print("Stemming:", stems)  
# Output: ['run', 'bet', 'fish', 'argu', 'fli']
```

Key Differences:
- Lemmatization uses vocabulary and morphological analysis
- Stemming uses simple rules to chop off word endings
- Lemmatization produces valid words
- Stemming may produce invalid words but is faster

## Q16: Explain the concept of Bag of Words (BoW) and its limitations

**Answer:**
Bag of Words is a text representation technique that creates a vocabulary of unique words and represents documents as vectors based on word frequencies.

**Implementation:**
```python
from sklearn.feature_extraction.text import CountVectorizer

# Sample documents
documents = [
    "I love machine learning",
    "I love deep learning",
    "Neural networks are amazing"
]

# Create BoW representation
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(documents)

# Get vocabulary
vocab = vectorizer.get_feature_names_out()
print("Vocabulary:", vocab)

# Get document vectors
print("Document vectors:\n", X.toarray())
```

**Limitations:**
1. Loses word order information
2. Ignores semantics and context
3. High dimensionality with large vocabularies
4. Sparse representation
5. Cannot handle out-of-vocabulary words

## Q17: How does TF-IDF work, and how is it different from simple word frequency?

**Answer:**
TF-IDF (Term Frequency-Inverse Document Frequency) is a numerical statistic that reflects the importance of a word in a document relative to a collection of documents.

**Implementation:**
```python
from sklearn.feature_extraction.text import TfidfVectorizer

# Sample documents
documents = [
    "I love machine learning",
    "I love deep learning",
    "Neural networks are amazing"
]

# Create TF-IDF representation
tfidf = TfidfVectorizer()
X = tfidf.fit_transform(documents)

# Get feature names
feature_names = tfidf.get_feature_names_out()

# Print TF-IDF weights
for doc_idx, doc in enumerate(documents):
    print(f"\nDocument {doc_idx+1}:")
    for feat_idx, feature in enumerate(feature_names):
        score = X[doc_idx, feat_idx]
        if score > 0:
            print(f"{feature}: {score:.3f}")
```

**Differences from Word Frequency:**
1. Considers document frequency
2. Penalizes common words
3. Highlights distinctive terms
4. Better for information retrieval
5. More meaningful for document comparison

## Q18: What is word embedding, and why is it useful in NLP?

**Answer:**
Word embeddings are dense vector representations of words that capture semantic relationships and meaning in a continuous vector space.

**Implementation using Word2Vec:**
```python
from gensim.models import Word2Vec

# Sample sentences
sentences = [
    ['I', 'love', 'machine', 'learning'],
    ['neural', 'networks', 'are', 'fascinating'],
    ['deep', 'learning', 'is', 'powerful']
]

# Train Word2Vec model
model = Word2Vec(sentences, 
                vector_size=100,  # Embedding dimension
                window=5,         # Context window
                min_count=1,      # Minimum word frequency
                workers=4)        # Number of threads

# Get word vector
vector = model.wv['learning']

# Find similar words
similar_words = model.wv.most_similar('learning')
print("Similar words:", similar_words)

# Word arithmetic
result = model.wv.most_similar(
    positive=['king', 'woman'],
    negative=['man']
)
print("king - man + woman =", result[0][0])
```

**Benefits:**
1. Captures semantic relationships
2. Reduces dimensionality
3. Enables transfer learning
4. Supports analogical reasoning
5. Improves generalization

## Q19: Explain Text Classification and Its Implementation

**Answer:**
Text classification is the task of assigning predefined categories to text documents.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

class TextClassifier:
    def __init__(self):
        self.pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(max_features=10000)),
            ('classifier', LogisticRegression())
        ])
    
    def train(self, texts, labels):
        """Train the text classifier"""
        self.pipeline.fit(texts, labels)
    
    def predict(self, texts):
        """Predict labels for new texts"""
        return self.pipeline.predict(texts)
    
    def predict_proba(self, texts):
        """Get prediction probabilities"""
        return self.pipeline.predict_proba(texts)

# Usage example
def text_classification_example():
    # Sample data
    texts = [
        "This movie is great!",
        "Terrible waste of time",
        "I loved this film"
    ]
    labels = [1, 0, 1]  # 1: positive, 0: negative
    
    # Train classifier
    classifier = TextClassifier()
    classifier.train(texts, labels)
    
    # Make predictions
    new_texts = ["Amazing performance!", "Not worth watching"]
    predictions = classifier.predict(new_texts)
    return predictions
```

## Q20: Named Entity Recognition (NER) Implementation

**Answer:**
NER identifies and classifies named entities (person names, organizations, locations, etc.) in text.

```python
import spacy

class NamedEntityRecognizer:
    def __init__(self, model="en_core_web_sm"):
        self.nlp = spacy.load(model)
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        return entities
    
    def visualize_entities(self, text):
        """Visualize entities in text"""
        doc = self.nlp(text)
        return spacy.displacy.render(
            doc,
            style="ent",
            options={"colors": {"PERSON": "#ff0000", "ORG": "#00ff00"}}
        )

# Custom NER training
def train_custom_ner(training_data):
    """Train a custom NER model"""
    nlp = spacy.blank("en")
    ner = nlp.add_pipe("ner")
    
    # Add labels
    for _, annotations in training_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    
    # Training loop
    optimizer = nlp.begin_training()
    for iteration in range(100):
        losses = {}
        for text, annotations in training_data:
            nlp.update(
                [text],
                [annotations],
                drop=0.5,
                losses=losses
            )
    
    return nlp
```

## Q21: Text Summarization Techniques

**Answer:**
Implementation of extractive and abstractive text summarization:

1. **Extractive Summarization:**
```python
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np

class ExtractiveSummarizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def sentence_similarity(self, sent1, sent2):
        """Calculate similarity between two sentences"""
        words1 = [word.lower() for word in sent1 if word.lower() not in self.stop_words]
        words2 = [word.lower() for word in sent2 if word.lower() not in self.stop_words]
        
        all_words = list(set(words1 + words2))
        vector1 = [1 if word in words1 else 0 for word in all_words]
        vector2 = [1 if word in words2 else 0 for word in all_words]
        
        return 1 - cosine_distance(vector1, vector2)
    
    def build_similarity_matrix(self, sentences):
        """Build similarity matrix for sentences"""
        similarity_matrix = np.zeros((len(sentences), len(sentences)))
        
        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 != idx2:
                    similarity_matrix[idx1][idx2] = self.sentence_similarity(
                        sentences[idx1], sentences[idx2]
                    )
        
        return similarity_matrix
    
    def summarize(self, text, num_sentences=3):
        """Generate summary"""
        sentences = sent_tokenize(text)
        similarity_matrix = self.build_similarity_matrix(sentences)
        
        # PageRank algorithm
        scores = np.array([1] * len(sentences))
        for _ in range(10):  # Power iteration
            scores = np.matmul(similarity_matrix, scores)
        
        # Select top sentences
        ranked_sentences = [
            (score, idx, sent)
            for idx, (score, sent) in enumerate(zip(scores, sentences))
        ]
        ranked_sentences.sort(reverse=True)
        
        return " ".join([sent for _, _, sent in ranked_sentences[:num_sentences]])
```

2. **Abstractive Summarization:**
```python
from transformers import pipeline

class AbstractiveSummarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.summarizer = pipeline(
            "summarization",
            model=model_name,
            tokenizer=model_name
        )
    
    def summarize(self, text, max_length=130, min_length=30):
        """Generate abstractive summary"""
        summary = self.summarizer(
            text,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )
        return summary[0]['summary_text']

# Usage example
def summarization_example():
    text = """
    Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence 
    concerned with the interactions between computers and human language. It is used to apply algorithms to identify 
    and extract natural language rules such that unstructured language data is converted into a form that computers 
    can understand. The goal is a computer capable of understanding the contents of documents, including the contextual 
    nuances of the language within them. The technology can then accurately extract information and insights contained 
    in the documents as well as categorize and organize the documents themselves.
    """
    
    # Extractive summary
    ext_summarizer = ExtractiveSummarizer()
    ext_summary = ext_summarizer.summarize(text)
    
    # Abstractive summary
    abs_summarizer = AbstractiveSummarizer()
    abs_summary = abs_summarizer.summarize(text)
    
    return {
        'extractive': ext_summary,
        'abstractive': abs_summary
    }
```

## Q22: Topic Modeling and Document Clustering

**Answer:**
Implementation of topic modeling using Latent Dirichlet Allocation (LDA) and document clustering:

```python
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans

class TopicModeler:
    def __init__(self, n_topics=5):
        self.vectorizer = CountVectorizer(max_features=1000, stop_words='english')
        self.lda = LatentDirichletAllocation(
            n_components=n_topics,
            random_state=42
        )
    
    def fit(self, documents):
        """Fit the topic model"""
        self.doc_term_matrix = self.vectorizer.fit_transform(documents)
        self.lda.fit(self.doc_term_matrix)
    
    def get_topics(self, n_words=10):
        """Get top words for each topic"""
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(self.lda.components_):
            top_words = [
                feature_names[i]
                for i in topic.argsort()[:-n_words-1:-1]
            ]
            topics.append({
                'topic_id': topic_idx,
                'words': top_words
            })
        
        return topics
    
    def get_document_topics(self, documents):
        """Get topic distribution for documents"""
        doc_term_matrix = self.vectorizer.transform(documents)
        return self.lda.transform(doc_term_matrix)

class DocumentClusterer:
    def __init__(self, n_clusters=5):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.kmeans = KMeans(n_clusters=n_clusters)
    
    def fit(self, documents):
        """Fit the clustering model"""
        self.doc_vectors = self.vectorizer.fit_transform(documents)
        self.kmeans.fit(self.doc_vectors)
    
    def predict(self, documents):
        """Predict clusters for new documents"""
        vectors = self.vectorizer.transform(documents)
        return self.kmeans.predict(vectors)
    
    def get_cluster_keywords(self, n_words=10):
        """Get representative keywords for each cluster"""
        feature_names = self.vectorizer.get_feature_names_out()
        clusters = []
        
        for cluster_idx in range(self.kmeans.n_clusters):
            center = self.kmeans.cluster_centers_[cluster_idx]
            top_indices = center.argsort()[::-1][:n_words]
            keywords = [feature_names[i] for i in top_indices]
            clusters.append({
                'cluster_id': cluster_idx,
                'keywords': keywords
            })
        
        return clusters

# Usage example
def topic_modeling_example():
    documents = [
        "Machine learning algorithms require significant computational resources",
        "Deep learning models have achieved remarkable results in computer vision",
        "Natural language processing helps computers understand human language",
        "Neural networks are inspired by biological brain structures",
        "Artificial intelligence is transforming various industries"
    ]
    
    # Topic modeling
    topic_modeler = TopicModeler(n_topics=2)
    topic_modeler.fit(documents)
    topics = topic_modeler.get_topics()
    
    # Document clustering
    clusterer = DocumentClusterer(n_clusters=2)
    clusterer.fit(documents)
    clusters = clusterer.get_cluster_keywords()
    
    return {
        'topics': topics,
        'clusters': clusters
    }
```

## Q23: Text Generation with N-grams

**Answer:**
Implementation of N-gram based text generation:

```python
from collections import defaultdict
import random
import nltk
from nltk.util import ngrams

class NgramGenerator:
    def __init__(self, n=2):
        self.n = n
        self.model = defaultdict(list)
    
    def train(self, text):
        """Train the N-gram model"""
        # Tokenize text
        tokens = nltk.word_tokenize(text.lower())
        
        # Generate n-grams
        for i in range(len(tokens) - self.n):
            context = tuple(tokens[i:i+self.n-1])
            next_word = tokens[i+self.n-1]
            self.model[context].append(next_word)
    
    def generate(self, seed_words, length=50):
        """Generate text using the trained model"""
        if len(seed_words) != self.n - 1:
            raise ValueError(f"Seed words must be of length {self.n-1}")
        
        current = tuple(seed_words)
        result = list(seed_words)
        
        for _ in range(length):
            if current not in self.model:
                break
                
            next_word = random.choice(self.model[current])
            result.append(next_word)
            current = tuple(result[-(self.n-1):])
        
        return ' '.join(result)

class MarkovChainGenerator:
    def __init__(self):
        self.transitions = defaultdict(lambda: defaultdict(int))
        self.totals = defaultdict(int)
    
    def train(self, text):
        """Train the Markov Chain model"""
        tokens = nltk.word_tokenize(text.lower())
        
        for i in range(len(tokens) - 1):
            current = tokens[i]
            next_word = tokens[i + 1]
            self.transitions[current][next_word] += 1
            self.totals[current] += 1
    
    def generate(self, seed_word, length=50):
        """Generate text using the Markov Chain"""
        if seed_word not in self.transitions:
            raise ValueError("Seed word not in training data")
        
        current = seed_word
        result = [current]
        
        for _ in range(length):
            if current not in self.transitions:
                break
                
            # Calculate probabilities
            probabilities = {
                word: count / self.totals[current]
                for word, count in self.transitions[current].items()
            }
            
            # Choose next word based on probabilities
            words = list(probabilities.keys())
            probs = list(probabilities.values())
            next_word = random.choices(words, weights=probs)[0]
            
            result.append(next_word)
            current = next_word
        
        return ' '.join(result)

# Usage example
def text_generation_example():
    # Sample text
    text = """
    Natural language processing is a fascinating field of study.
    It combines linguistics, computer science, and artificial intelligence.
    Researchers in NLP work on various challenging problems.
    """
    
    # N-gram generation
    ngram_gen = NgramGenerator(n=3)
    ngram_gen.train(text)
    ngram_text = ngram_gen.generate(['natural', 'language'])
    
    # Markov Chain generation
    markov_gen = MarkovChainGenerator()
    markov_gen.train(text)
    markov_text = markov_gen.generate('natural')
    
    return {
        'ngram_text': ngram_text,
        'markov_text': markov_text
    }
```

## Q24: Sentiment Analysis Implementation

**Answer:**
Implementation of sentiment analysis using different approaches:

```python
from textblob import TextBlob
from transformers import pipeline
import torch.nn as nn
import torch.nn.functional as F

class RuleBased:
    def __init__(self):
        self.positive_words = set(['good', 'great', 'excellent', 'amazing'])
        self.negative_words = set(['bad', 'poor', 'terrible', 'awful'])
    
    def analyze(self, text):
        """Simple rule-based sentiment analysis"""
        words = text.lower().split()
        pos_count = sum(1 for word in words if word in self.positive_words)
        neg_count = sum(1 for word in words if word in self.negative_words)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        return 'neutral'

class MLBasedSentiment:
    def __init__(self):
        self.classifier = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )
    
    def analyze(self, text):
        """ML-based sentiment analysis"""
        result = self.classifier(text)[0]
        return {
            'label': result['label'],
            'score': result['score']
        }

class CNNSentiment(nn.Module):
    def __init__(self, vocab_size, embedding_dim, n_filters, filter_sizes):
        super().__init__()
        
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.convs = nn.ModuleList([
            nn.Conv2d(1, n_filters, (fs, embedding_dim))
            for fs in filter_sizes
        ])
        self.fc = nn.Linear(len(filter_sizes) * n_filters, 2)
        self.dropout = nn.Dropout(0.5)
    
    def forward(self, text):
        # text = [batch size, sent len]
        embedded = self.embedding(text)
        # embedded = [batch size, sent len, emb dim]
        
        embedded = embedded.unsqueeze(1)
        # embedded = [batch size, 1, sent len, emb dim]
        
        conved = [F.relu(conv(embedded)).squeeze(3) for conv in self.convs]
        # conved_n = [batch size, n_filters, sent len - filter_sizes[n] + 1]
        
        pooled = [F.max_pool1d(conv, conv.shape[2]).squeeze(2) for conv in conved]
        # pooled_n = [batch size, n_filters]
        
        cat = self.dropout(torch.cat(pooled, dim=1))
        # cat = [batch size, n_filters * len(filter_sizes)]
        
        return self.fc(cat)

# Usage example
def sentiment_analysis_example():
    text = "This movie was absolutely amazing! The plot was great and the acting was excellent."
    
    # Rule-based analysis
    rule_based = RuleBased()
    rule_result = rule_based.analyze(text)
    
    # TextBlob analysis
    blob = TextBlob(text)
    blob_sentiment = blob.sentiment.polarity
    
    # ML-based analysis
    ml_based = MLBasedSentiment()
    ml_result = ml_based.analyze(text)
    
    return {
        'rule_based': rule_result,
        'textblob': blob_sentiment,
        'ml_based': ml_result
    }
```

## Q25: Question Answering Systems

**Answer:**
Implementation of different question answering approaches:

```python
from transformers import pipeline
import spacy
from sentence_transformers import SentenceTransformer, util

class ExtractiveQA:
    def __init__(self):
        self.qa_pipeline = pipeline(
            "question-answering",
            model="distilbert-base-cased-distilled-squad"
        )
    
    def answer(self, question, context):
        """Extract answer from context"""
        result = self.qa_pipeline(
            question=question,
            context=context
        )
        return {
            'answer': result['answer'],
            'score': result['score'],
            'start': result['start'],
            'end': result['end']
        }

class SemanticQA:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.nlp = spacy.load('en_core_web_sm')
    
    def prepare_knowledge_base(self, text):
        """Prepare knowledge base by splitting into sentences"""
        doc = self.nlp(text)
        self.sentences = [sent.text.strip() for sent in doc.sents]
        self.sentence_embeddings = self.model.encode(self.sentences)
    
    def answer(self, question, top_k=3):
        """Find most relevant sentences to answer the question"""
        question_embedding = self.model.encode(question)
        
        # Calculate similarities
        similarities = util.pytorch_cos_sim(
            question_embedding,
            self.sentence_embeddings
        )[0]
        
        # Get top-k most similar sentences
        top_results = []
        for idx in similarities.argsort(descending=True)[:top_k]:
            top_results.append({
                'sentence': self.sentences[idx],
                'similarity': similarities[idx].item()
            })
        
        return top_results

class GenerativeQA:
    def __init__(self):
        self.generator = pipeline(
            "text2text-generation",
            model="google/flan-t5-small"
        )
    
    def answer(self, question, context=None):
        """Generate answer to question"""
        if context:
            prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
        else:
            prompt = f"Question: {question}\nAnswer:"
        
        response = self.generator(
            prompt,
            max_length=100,
            num_return_sequences=1
        )[0]['generated_text']
        
        return response

# Usage example
def question_answering_example():
    context = """
    Natural Language Processing (NLP) is a branch of artificial intelligence
    that helps computers understand, interpret, and manipulate human language.
    NLP combines computational linguistics, machine learning, and deep learning
    models to process and analyze large amounts of natural language data.
    """
    
    question = "What is NLP and what does it help with?"
    
    # Extractive QA
    extractive = ExtractiveQA()
    ext_answer = extractive.answer(question, context)
    
    # Semantic QA
    semantic = SemanticQA()
    semantic.prepare_knowledge_base(context)
    sem_answer = semantic.answer(question)
    
    # Generative QA
    generative = GenerativeQA()
    gen_answer = generative.answer(question, context)
    
    return {
        'extractive': ext_answer,
        'semantic': sem_answer,
        'generative': gen_answer
    }
```

## Q26: Text Style Transfer

**Answer:**
Implementation of text style transfer techniques:

```python
from transformers import MarianMTModel, MarianTokenizer
import torch

class StyleTransfer:
    def __init__(self):
        # Load models for different styles
        self.formal_model = self._load_model('Helsinki-NLP/opus-mt-en-en')
        self.simple_model = self._load_model('facebook/bart-large-cnn')
    
    def _load_model(self, model_name):
        """Load model and tokenizer"""
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return {'model': model, 'tokenizer': tokenizer}
    
    def to_formal(self, text):
        """Convert text to formal style"""
        tokenizer = self.formal_model['tokenizer']
        model = self.formal_model['model']
        
        inputs = tokenizer(f"make formal: {text}", return_tensors="pt")
        outputs = model.generate(**inputs)
        formal_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return formal_text
    
    def to_simple(self, text):
        """Convert text to simple style"""
        tokenizer = self.simple_model['tokenizer']
        model = self.simple_model['model']
        
        inputs = tokenizer(f"simplify: {text}", return_tensors="pt")
        outputs = model.generate(**inputs)
        simple_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return simple_text

class TextParaphraser:
    def __init__(self):
        self.model_name = "tuner007/pegasus_paraphrase"
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_name)
        self.model = PegasusForConditionalGeneration.from_pretrained(self.model_name)
    
    def paraphrase(self, text, num_variants=3):
        """Generate multiple paraphrases of the input text"""
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True)
        outputs = self.model.generate(
            **inputs,
            num_beams=10,
            num_return_sequences=num_variants,
            max_length=60
        )
        
        paraphrases = []
        for output in outputs:
            paraphrase = self.tokenizer.decode(
                output,
                skip_special_tokens=True
            )
            paraphrases.append(paraphrase)
        
        return paraphrases

# Usage example
def style_transfer_example():
    text = "yo, what's up? this is cool stuff!"
    
    # Style transfer
    transfer = StyleTransfer()
    formal_text = transfer.to_formal(text)
    simple_text = transfer.to_simple(text)
    
    # Paraphrasing
    paraphraser = TextParaphraser()
    paraphrases = paraphraser.paraphrase(text)
    
    return {
        'original': text,
        'formal': formal_text,
        'simple': simple_text,
        'paraphrases': paraphrases
    }
```

[End of Natural Language Processing Section] 