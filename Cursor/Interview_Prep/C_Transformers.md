# Section C: Transformers and Extended Architecture

## Q27: Describe the concept of learning rate scheduling

**Answer:**
Learning rate scheduling is a technique to dynamically adjust the learning rate during training to optimize the model's convergence.

**Implementation Examples:**

1. **Step Decay Schedule:**
```python
import tensorflow as tf

def step_decay_schedule(initial_lr=1e-3, decay_factor=0.75, step_size=10):
    def schedule(epoch):
        return initial_lr * (decay_factor ** (epoch // step_size))
    
    return tf.keras.callbacks.LearningRateScheduler(schedule)

# Usage
model.fit(
    X_train, y_train,
    callbacks=[step_decay_schedule()],
    epochs=100
)
```

2. **Cosine Decay Schedule:**
```python
def cosine_decay_schedule(initial_lr=1e-3, total_epochs=100):
    def schedule(epoch):
        return initial_lr * (1 + tf.math.cos(epoch * tf.math.pi / total_epochs)) / 2
    
    return tf.keras.callbacks.LearningRateScheduler(schedule)
```

## Q28: Transfer Learning in NLP

**Answer:**
Transfer learning in NLP involves using pre-trained language models and adapting them for specific tasks.

**Implementation Example:**
```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from torch.optim import AdamW

def setup_transfer_learning():
    # Load pre-trained model and tokenizer
    model_name = "bert-base-uncased"
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2  # Binary classification
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Freeze base layers
    for param in model.base_model.parameters():
        param.requires_grad = False
    
    # Configure optimizer for fine-tuning
    optimizer = AdamW(model.parameters(), lr=2e-5)
    
    return model, tokenizer, optimizer

# Usage
model, tokenizer, optimizer = setup_transfer_learning()
```

## Q29: GPT vs BERT Differences

**Answer:**
Key differences between GPT and BERT architectures:

1. **Directionality:**
- GPT: Unidirectional (left-to-right)
- BERT: Bidirectional

2. **Pre-training Tasks:**
```python
# GPT-style pre-training (language modeling)
def gpt_style_training(text):
    # Generate next token prediction
    input_ids = tokenizer(text, return_tensors="pt").input_ids
    outputs = model(input_ids)
    next_token_logits = outputs.logits[:, -1, :]
    return next_token_logits

# BERT-style pre-training (masked language modeling)
def bert_style_training(text):
    # Mask random tokens
    inputs = tokenizer(text, return_tensors="pt")
    masked_inputs = mask_random_tokens(inputs)
    outputs = model(**masked_inputs)
    return outputs.logits
```

3. **Architecture Differences:**
```python
# GPT-style architecture (decoder only)
class GPTStyle(nn.Module):
    def __init__(self):
        super().__init__()
        self.decoder = TransformerDecoder()
    
    def forward(self, x):
        return self.decoder(x)

# BERT-style architecture (encoder only)
class BERTStyle(nn.Module):
    def __init__(self):
        super().__init__()
        self.encoder = TransformerEncoder()
    
    def forward(self, x):
        return self.encoder(x)
```

## Q30: Problems Solved by Transformers

**Answer:**
Transformers solve several limitations of RNNs:

1. **Parallel Processing:**
```python
# Transformer parallel processing
def transformer_forward(self, x):
    # Process all tokens simultaneously
    attention_outputs = self.self_attention(x)
    return self.feed_forward(attention_outputs)

# RNN sequential processing
def rnn_forward(self, x):
    # Process tokens one by one
    hidden = None
    for token in x:
        hidden = self.rnn_cell(token, hidden)
    return hidden
```

2. **Long-range Dependencies:**
```python
def self_attention(query, key, value):
    # Direct connections between any positions
    attention_scores = torch.matmul(query, key.transpose(-2, -1))
    attention_scores = attention_scores / math.sqrt(key.size(-1))
    attention_weights = F.softmax(attention_scores, dim=-1)
    return torch.matmul(attention_weights, value)
```

## Q31: Transformer vs RNN/LSTM

**Answer:**
Key differences in implementation:

```python
# Transformer Implementation
class TransformerLayer(nn.Module):
    def __init__(self, d_model, nhead):
        super().__init__()
        self.self_attn = MultiheadAttention(d_model, nhead)
        self.feed_forward = FeedForward(d_model)
        self.norm1 = LayerNorm(d_model)
        self.norm2 = LayerNorm(d_model)
    
    def forward(self, x):
        # Self-attention
        attn_output = self.self_attn(x, x, x)
        x = self.norm1(x + attn_output)
        
        # Feed-forward
        ff_output = self.feed_forward(x)
        x = self.norm2(x + ff_output)
        return x

# LSTM Implementation
class LSTMLayer(nn.Module):
    def __init__(self, input_size, hidden_size):
        super().__init__()
        self.lstm = nn.LSTM(input_size, hidden_size)
    
    def forward(self, x, hidden=None):
        # Sequential processing
        output, (hidden, cell) = self.lstm(x, hidden)
        return output, (hidden, cell)
```

## Q31a: Attention Mechanism Implementation

**Answer:**
Detailed implementation of the attention mechanism used in Transformers:

```python
import torch
import torch.nn as nn
import math

class MultiHeadAttention(nn.Module):
    def __init__(self, d_model, num_heads):
        super().__init__()
        assert d_model % num_heads == 0
        
        self.d_model = d_model
        self.num_heads = num_heads
        self.d_k = d_model // num_heads
        
        self.W_q = nn.Linear(d_model, d_model)
        self.W_k = nn.Linear(d_model, d_model)
        self.W_v = nn.Linear(d_model, d_model)
        self.W_o = nn.Linear(d_model, d_model)
    
    def scaled_dot_product_attention(self, Q, K, V, mask=None):
        """Scaled dot-product attention"""
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, -1e9)
        
        attention_weights = torch.softmax(scores, dim=-1)
        output = torch.matmul(attention_weights, V)
        return output, attention_weights
    
    def split_heads(self, x):
        """Split the last dimension into (num_heads, d_k)"""
        batch_size = x.size(0)
        return x.view(batch_size, -1, self.num_heads, self.d_k).transpose(1, 2)
    
    def forward(self, query, key, value, mask=None):
        batch_size = query.size(0)
        
        # Linear projections and split heads
        Q = self.split_heads(self.W_q(query))
        K = self.split_heads(self.W_k(key))
        V = self.split_heads(self.W_v(value))
        
        # Apply attention
        scaled_attention, attention_weights = self.scaled_dot_product_attention(
            Q, K, V, mask
        )
        
        # Concatenate heads and apply final linear layer
        scaled_attention = scaled_attention.transpose(1, 2).contiguous().view(
            batch_size, -1, self.d_model
        )
        output = self.W_o(scaled_attention)
        
        return output, attention_weights

## Q31b: Position-wise Feed-Forward Networks

**Answer:**
Implementation of the feed-forward network used in Transformer layers:

```python
class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super().__init__()
        self.linear1 = nn.Linear(d_model, d_ff)
        self.linear2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)
        self.activation = nn.ReLU()
    
    def forward(self, x):
        """
        x: Input tensor [batch_size, seq_len, d_model]
        """
        x = self.linear1(x)
        x = self.activation(x)
        x = self.dropout(x)
        x = self.linear2(x)
        return x

## Q31c: Positional Encoding

**Answer:**
Implementation of positional encoding for Transformer models:

```python
class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_seq_length=5000):
        super().__init__()
        
        # Create positional encoding matrix
        pe = torch.zeros(max_seq_length, d_model)
        position = torch.arange(0, max_seq_length, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        
        # Calculate positional encodings
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # Add batch dimension and register as buffer
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
    
    def forward(self, x):
        """
        x: Input tensor [batch_size, seq_len, d_model]
        """
        return x + self.pe[:, :x.size(1)]

## Q31d: Complete Transformer Implementation

**Answer:**
Implementation of a complete Transformer model:

```python
class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff, dropout=0.1):
        super().__init__()
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.feed_forward = PositionwiseFeedForward(d_model, d_ff, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Multi-head attention
        attn_output, _ = self.attention(x, x, x, mask)
        x = self.norm1(x + self.dropout(attn_output))
        
        # Feed forward
        ff_output = self.feed_forward(x)
        x = self.norm2(x + self.dropout(ff_output))
        
        return x

class Transformer(nn.Module):
    def __init__(self, vocab_size, d_model, num_heads, num_layers, d_ff, max_seq_length=5000, dropout=0.1):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, d_model)
        self.positional_encoding = PositionalEncoding(d_model, max_seq_length)
        
        self.transformer_blocks = nn.ModuleList([
            TransformerBlock(d_model, num_heads, d_ff, dropout)
            for _ in range(num_layers)
        ])
        
        self.final_layer = nn.Linear(d_model, vocab_size)
        self.dropout = nn.Dropout(dropout)
    
    def forward(self, x, mask=None):
        # Embedding and positional encoding
        x = self.embedding(x)
        x = self.positional_encoding(x)
        x = self.dropout(x)
        
        # Transformer blocks
        for transformer_block in self.transformer_blocks:
            x = transformer_block(x, mask)
        
        # Final layer
        output = self.final_layer(x)
        return output

# Usage example
def transformer_example():
    # Model parameters
    vocab_size = 10000
    d_model = 512
    num_heads = 8
    num_layers = 6
    d_ff = 2048
    
    # Create model
    model = Transformer(
        vocab_size=vocab_size,
        d_model=d_model,
        num_heads=num_heads,
        num_layers=num_layers,
        d_ff=d_ff
    )
    
    # Example forward pass
    batch_size = 32
    seq_length = 100
    x = torch.randint(0, vocab_size, (batch_size, seq_length))
    output = model(x)
    
    return output.shape  # [batch_size, seq_length, vocab_size]
```

## Q31e: Transformer Training Techniques

**Answer:**
Implementation of specialized training techniques for Transformers:

```python
class TransformerTrainer:
    def __init__(self, model, optimizer, scheduler):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.criterion = nn.CrossEntropyLoss(ignore_index=0)  # 0 is padding token
    
    def create_mask(self, src, tgt):
        """Create masks for transformer training"""
        src_mask = (src != 0).unsqueeze(1).unsqueeze(2)
        
        tgt_mask = (tgt != 0).unsqueeze(1).unsqueeze(3)
        seq_length = tgt.size(1)
        nopeak_mask = (1 - torch.triu(
            torch.ones(1, seq_length, seq_length),
            diagonal=1
        )).bool()
        tgt_mask = tgt_mask & nopeak_mask
        
        return src_mask, tgt_mask
    
    def train_step(self, src, tgt):
        """Single training step"""
        self.model.train()
        self.optimizer.zero_grad()
        
        # Create masks
        src_mask, tgt_mask = self.create_mask(src, tgt)
        
        # Forward pass
        output = self.model(src, src_mask)
        loss = self.criterion(
            output.view(-1, output.size(-1)),
            tgt.view(-1)
        )
        
        # Backward pass
        loss.backward()
        
        # Clip gradients
        torch.nn.utils.clip_grad_norm_(self.model.parameters(), max_norm=1.0)
        
        # Update parameters
        self.optimizer.step()
        self.scheduler.step()
        
        return loss.item()
    
    def train_epoch(self, data_loader):
        """Train for one epoch"""
        total_loss = 0
        for batch in data_loader:
            src, tgt = batch
            loss = self.train_step(src, tgt)
            total_loss += loss
        
        return total_loss / len(data_loader)

# Usage example
def transformer_training_example():
    # Create model and training components
    model = Transformer(vocab_size=10000, d_model=512, num_heads=8, num_layers=6, d_ff=2048)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001, betas=(0.9, 0.98), eps=1e-9)
    scheduler = torch.optim.lr_scheduler.WarmupLinearSchedule(optimizer, warmup_steps=4000)
    
    # Create trainer
    trainer = TransformerTrainer(model, optimizer, scheduler)
    
    # Train model
    for epoch in range(num_epochs):
        loss = trainer.train_epoch(train_loader)
        print(f"Epoch {epoch+1}, Loss: {loss:.4f}")
```

[End of Transformers Section] 