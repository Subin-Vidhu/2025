# Section A: Artificial Neural Networks (ANN)

## Q1: What is an Artificial Neural Network, and how does it work?

**Answer:**
An Artificial Neural Network (ANN) is a computational model inspired by the biological neural networks in human brains. It consists of interconnected nodes (neurons) organized in layers that process and transform input data into meaningful outputs.

**Key Components:**
1. Input Layer: Receives raw data
2. Hidden Layers: Processes information through weighted connections
3. Output Layer: Produces final predictions
4. Weights & Biases: Parameters that are learned during training
5. Activation Functions: Introduce non-linearity

**Example Implementation:**
```python
import tensorflow as tf

def create_simple_nn():
    model = tf.keras.Sequential([
        # Input layer
        tf.keras.layers.Input(shape=(10,)),
        
        # Hidden layers
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(32, activation='relu'),
        
        # Output layer
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(
        optimizer='adam',
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    return model

# Usage example
model = create_simple_nn()
print(model.summary())
```

## Q2: What are activation functions, and what are their types?

**Answer:**
Activation functions introduce non-linearity into neural networks, allowing them to learn complex patterns. They determine whether a neuron should be activated or not.

**Common Types:**

1. **ReLU (Rectified Linear Unit)**
```python
def relu(x):
    return max(0, x)

# TensorFlow implementation
tf.keras.layers.Dense(64, activation='relu')
```
- Most commonly used
- Helps prevent vanishing gradient
- Simple and computationally efficient

2. **Sigmoid**
```python
import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# TensorFlow implementation
tf.keras.layers.Dense(1, activation='sigmoid')
```
- Output range: [0,1]
- Used for binary classification
- Can suffer from vanishing gradient

3. **Tanh**
```python
def tanh(x):
    return np.tanh(x)

# TensorFlow implementation
tf.keras.layers.Dense(64, activation='tanh')
```
- Output range: [-1,1]
- Zero-centered
- Stronger gradients than sigmoid

4. **Softmax**
```python
def softmax(x):
    exp_x = np.exp(x)
    return exp_x / exp_x.sum()

# TensorFlow implementation
tf.keras.layers.Dense(num_classes, activation='softmax')
```
- Used for multi-class classification
- Outputs sum to 1
- Represents probability distribution

## Q3: What is backpropagation, and how does it work?

**Answer:**
Backpropagation is the algorithm used to train neural networks by minimizing the error between predicted and actual outputs. It works by calculating gradients of the loss function with respect to each weight and updating them accordingly.

**Process:**
1. Forward Pass: Compute predictions
2. Calculate Loss: Compare predictions with actual values
3. Backward Pass: Compute gradients
4. Update Weights: Adjust parameters to minimize loss

**Implementation Example:**
```python
def simple_backprop():
    # Initialize network
    network = {
        'W1': np.random.randn(input_size, hidden_size),
        'b1': np.zeros(hidden_size),
        'W2': np.random.randn(hidden_size, output_size),
        'b2': np.zeros(output_size)
    }
    
    def forward(X):
        # Forward pass
        z1 = np.dot(X, network['W1']) + network['b1']
        a1 = relu(z1)
        z2 = np.dot(a1, network['W2']) + network['b2']
        y_pred = sigmoid(z2)
        return y_pred, (z1, a1, z2)
    
    def backward(X, y, y_pred, cache):
        z1, a1, z2 = cache
        m = X.shape[0]
        
        # Backward pass
        dz2 = y_pred - y
        dW2 = np.dot(a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0) / m
        
        da1 = np.dot(dz2, network['W2'].T)
        dz1 = da1 * (z1 > 0)  # ReLU derivative
        dW1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0) / m
        
        return {'W1': dW1, 'b1': db1, 'W2': dW2, 'b2': db2}
    
    return forward, backward

# Usage
forward_pass, backward_pass = simple_backprop()
```

## Q4: Explain Different Types of Neural Networks

**Answer:**
There are several types of neural networks designed for different tasks:

1. **Feedforward Neural Network (FNN):**
```python
import torch.nn as nn

class FeedForwardNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )
    
    def forward(self, x):
        return self.layers(x)
```

2. **Convolutional Neural Network (CNN):**
```python
class ConvNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(16, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )
        self.fc_layers = nn.Sequential(
            nn.Linear(32 * 8 * 8, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
    
    def forward(self, x):
        x = self.conv_layers(x)
        x = x.view(x.size(0), -1)
        return self.fc_layers(x)
```

3. **Recurrent Neural Network (RNN):**
```python
class SimpleRNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.rnn = nn.RNN(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        output, hidden = self.rnn(x)
        return self.fc(output[:, -1, :])
```

## Q5: What are Loss Functions and Optimizers?

**Answer:**
Loss functions measure model performance, while optimizers update model parameters to minimize the loss.

1. **Common Loss Functions:**
```python
import torch.nn.functional as F

# Binary Cross Entropy
def binary_cross_entropy(y_pred, y_true):
    return F.binary_cross_entropy(y_pred, y_true)

# Categorical Cross Entropy
def categorical_cross_entropy(y_pred, y_true):
    return F.cross_entropy(y_pred, y_true)

# Mean Squared Error
def mse_loss(y_pred, y_true):
    return F.mse_loss(y_pred, y_true)
```

2. **Popular Optimizers:**
```python
import torch.optim as optim

def configure_optimizers(model, lr=0.001):
    # Adam optimizer
    adam = optim.Adam(model.parameters(), lr=lr)
    
    # SGD with momentum
    sgd = optim.SGD(model.parameters(), lr=lr, momentum=0.9)
    
    # RMSprop
    rmsprop = optim.RMSprop(model.parameters(), lr=lr)
    
    return {
        'adam': adam,
        'sgd': sgd,
        'rmsprop': rmsprop
    }

# Training loop example
def train_step(model, optimizer, x_batch, y_batch):
    optimizer.zero_grad()
    outputs = model(x_batch)
    loss = F.cross_entropy(outputs, y_batch)
    loss.backward()
    optimizer.step()
    return loss.item()
```

## Q6: Explain Regularization Techniques

**Answer:**
Regularization helps prevent overfitting in neural networks.

1. **Dropout:**
```python
class RegularizedNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, dropout_rate=0.5):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(hidden_size, output_size)
        )
    
    def forward(self, x):
        return self.layers(x)
```

2. **L1/L2 Regularization:**
```python
def add_weight_regularization(model, loss, lambda_l1=0.01, lambda_l2=0.01):
    # L1 regularization
    l1_reg = torch.tensor(0.)
    for param in model.parameters():
        l1_reg += torch.norm(param, 1)
    
    # L2 regularization
    l2_reg = torch.tensor(0.)
    for param in model.parameters():
        l2_reg += torch.norm(param, 2)
    
    # Total loss with regularization
    total_loss = loss + lambda_l1 * l1_reg + lambda_l2 * l2_reg
    return total_loss
```

3. **Batch Normalization:**
```python
class BatchNormNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(input_size, hidden_size),
            nn.BatchNorm1d(hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, output_size)
        )
    
    def forward(self, x):
        return self.layers(x)
```

## Q7: How to Handle Vanishing/Exploding Gradients?

**Answer:**
Techniques to address gradient problems:

1. **Gradient Clipping:**
```python
def train_with_gradient_clipping(model, optimizer, x_batch, y_batch, max_grad_norm=1.0):
    optimizer.zero_grad()
    outputs = model(x_batch)
    loss = F.cross_entropy(outputs, y_batch)
    loss.backward()
    
    # Clip gradients
    torch.nn.utils.clip_grad_norm_(model.parameters(), max_grad_norm)
    
    optimizer.step()
    return loss.item()
```

2. **Custom Weight Initialization:**
```python
def initialize_weights(model):
    for module in model.modules():
        if isinstance(module, nn.Linear):
            # He initialization
            nn.init.kaiming_normal_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Conv2d):
            # Xavier initialization
            nn.init.xavier_uniform_(module.weight)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
```

3. **Residual Connections:**
```python
class ResidualBlock(nn.Module):
    def __init__(self, channels):
        super().__init__()
        self.conv1 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(channels)
        self.conv2 = nn.Conv2d(channels, channels, kernel_size=3, padding=1)
        self.bn2 = nn.BatchNorm2d(channels)
    
    def forward(self, x):
        residual = x
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        out += residual  # Skip connection
        return F.relu(out)
```

## Q8: Model Training and Validation

**Answer:**
Implementation of model training and validation procedures:

```python
import torch
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split

class ModelTrainer:
    def __init__(self, model, criterion, optimizer, device='cuda'):
        self.model = model.to(device)
        self.criterion = criterion
        self.optimizer = optimizer
        self.device = device
        self.history = {'train_loss': [], 'val_loss': []}
    
    def train_epoch(self, train_loader):
        """Train for one epoch"""
        self.model.train()
        total_loss = 0
        
        for batch_x, batch_y in train_loader:
            batch_x = batch_x.to(self.device)
            batch_y = batch_y.to(self.device)
            
            # Forward pass
            self.optimizer.zero_grad()
            outputs = self.model(batch_x)
            loss = self.criterion(outputs, batch_y)
            
            # Backward pass
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        return total_loss / len(train_loader)
    
    def validate(self, val_loader):
        """Validate the model"""
        self.model.eval()
        total_loss = 0
        
        with torch.no_grad():
            for batch_x, batch_y in val_loader:
                batch_x = batch_x.to(self.device)
                batch_y = batch_y.to(self.device)
                
                outputs = self.model(batch_x)
                loss = self.criterion(outputs, batch_y)
                total_loss += loss.item()
        
        return total_loss / len(val_loader)
    
    def train(self, train_loader, val_loader, epochs=10):
        """Full training loop"""
        for epoch in range(epochs):
            train_loss = self.train_epoch(train_loader)
            val_loss = self.validate(val_loader)
            
            self.history['train_loss'].append(train_loss)
            self.history['val_loss'].append(val_loss)
            
            print(f"Epoch {epoch+1}/{epochs}")
            print(f"Train Loss: {train_loss:.4f}")
            print(f"Val Loss: {val_loss:.4f}")

# Usage example
def training_example():
    # Create model and training components
    model = FeedForwardNN(input_size=10, hidden_size=64, output_size=1)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters())
    
    # Create data loaders
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
    train_loader = DataLoader(
        list(zip(X_train, y_train)),
        batch_size=32,
        shuffle=True
    )
    val_loader = DataLoader(
        list(zip(X_val, y_val)),
        batch_size=32
    )
    
    # Train model
    trainer = ModelTrainer(model, criterion, optimizer)
    trainer.train(train_loader, val_loader)
    
    return trainer.history

## Q9: Model Evaluation and Metrics

**Answer:**
Implementation of various evaluation metrics and techniques:

```python
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import matplotlib.pyplot as plt

class ModelEvaluator:
    def __init__(self, model, device='cuda'):
        self.model = model.to(device)
        self.device = device
    
    def predict(self, loader):
        """Make predictions"""
        self.model.eval()
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for batch_x, batch_y in loader:
                batch_x = batch_x.to(self.device)
                outputs = self.model(batch_x)
                preds = outputs.argmax(dim=1).cpu().numpy()
                all_preds.extend(preds)
                all_labels.extend(batch_y.numpy())
        
        return np.array(all_preds), np.array(all_labels)
    
    def calculate_metrics(self, y_true, y_pred):
        """Calculate various metrics"""
        accuracy = accuracy_score(y_true, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='weighted'
        )
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1
        }
    
    def plot_confusion_matrix(self, y_true, y_pred, classes):
        """Plot confusion matrix"""
        cm = confusion_matrix(y_true, y_pred)
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm,
            annot=True,
            fmt='d',
            xticklabels=classes,
            yticklabels=classes
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.show()
    
    def plot_learning_curves(self, history):
        """Plot training history"""
        plt.figure(figsize=(10, 5))
        plt.plot(history['train_loss'], label='Train Loss')
        plt.plot(history['val_loss'], label='Validation Loss')
        plt.title('Learning Curves')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

# Usage example
def evaluation_example():
    # Create evaluator
    evaluator = ModelEvaluator(model)
    
    # Make predictions
    y_pred, y_true = evaluator.predict(test_loader)
    
    # Calculate metrics
    metrics = evaluator.calculate_metrics(y_true, y_pred)
    
    # Plot results
    evaluator.plot_confusion_matrix(
        y_true,
        y_pred,
        classes=['Class 0', 'Class 1']
    )
    evaluator.plot_learning_curves(trainer.history)
    
    return metrics

## Q10: Transfer Learning and Fine-tuning

**Answer:**
Implementation of transfer learning and model fine-tuning:

```python
import torchvision.models as models

class TransferLearner:
    def __init__(self, num_classes, freeze_backbone=True):
        # Load pre-trained model
        self.model = models.resnet50(pretrained=True)
        
        # Freeze backbone if specified
        if freeze_backbone:
            for param in self.model.parameters():
                param.requires_grad = False
        
        # Replace final layer
        in_features = self.model.fc.in_features
        self.model.fc = nn.Linear(in_features, num_classes)
    
    def configure_optimizer(self, lr=0.001):
        """Configure optimizer for fine-tuning"""
        if self.freeze_backbone:
            # Only optimize the final layer
            params = self.model.fc.parameters()
        else:
            # Optimize all parameters
            params = self.model.parameters()
        
        return optim.Adam(params, lr=lr)
    
    def unfreeze_layers(self, num_layers):
        """Unfreeze the last n layers for fine-tuning"""
        layers = list(self.model.children())
        for layer in layers[-num_layers:]:
            for param in layer.parameters():
                param.requires_grad = True

class ProgressiveFineTuner:
    def __init__(self, model, num_epochs_per_stage=5):
        self.model = model
        self.num_epochs_per_stage = num_epochs_per_stage
    
    def fine_tune(self, train_loader, val_loader):
        """Progressive fine-tuning"""
        stages = [
            {'lr': 1e-3, 'unfreeze_layers': 0},  # Train only final layer
            {'lr': 5e-4, 'unfreeze_layers': 1},  # Unfreeze last block
            {'lr': 1e-4, 'unfreeze_layers': 2},  # Unfreeze more layers
            {'lr': 5e-5, 'unfreeze_layers': 3}   # Unfreeze even more
        ]
        
        history = []
        for stage in stages:
            # Configure stage
            self.model.unfreeze_layers(stage['unfreeze_layers'])
            optimizer = self.model.configure_optimizer(lr=stage['lr'])
            
            # Train for this stage
            trainer = ModelTrainer(
                self.model,
                nn.CrossEntropyLoss(),
                optimizer
            )
            trainer.train(
                train_loader,
                val_loader,
                epochs=self.num_epochs_per_stage
            )
            
            history.append(trainer.history)
        
        return history

# Usage example
def transfer_learning_example():
    # Create transfer learner
    transfer_learner = TransferLearner(num_classes=10)
    
    # Fine-tune progressively
    fine_tuner = ProgressiveFineTuner(transfer_learner)
    history = fine_tuner.fine_tune(train_loader, val_loader)
    
    return history
```

## Q11: Advanced Architectures and Techniques

**Answer:**
Implementation of advanced neural network architectures and techniques:

```python
import torch.nn as nn
import torch.nn.functional as F

class DenseNet(nn.Module):
    def __init__(self, input_size, growth_rate=32):
        super().__init__()
        self.dense1 = self._make_dense_block(input_size, growth_rate)
        self.dense2 = self._make_dense_block(input_size + growth_rate, growth_rate)
        self.dense3 = self._make_dense_block(input_size + 2 * growth_rate, growth_rate)
        self.out = nn.Linear(input_size + 3 * growth_rate, 10)
    
    def _make_dense_block(self, in_features, growth_rate):
        return nn.Sequential(
            nn.Linear(in_features, growth_rate),
            nn.BatchNorm1d(growth_rate),
            nn.ReLU(inplace=True)
        )
    
    def forward(self, x):
        out1 = self.dense1(x)
        concat1 = torch.cat([x, out1], dim=1)
        
        out2 = self.dense2(concat1)
        concat2 = torch.cat([concat1, out2], dim=1)
        
        out3 = self.dense3(concat2)
        concat3 = torch.cat([concat2, out3], dim=1)
        
        return self.out(concat3)

class HighwayNetwork(nn.Module):
    def __init__(self, size, num_layers=10):
        super().__init__()
        self.num_layers = num_layers
        self.nonlinear = nn.ModuleList([nn.Linear(size, size) for _ in range(num_layers)])
        self.gate = nn.ModuleList([nn.Linear(size, size) for _ in range(num_layers)])
    
    def forward(self, x):
        for layer in range(self.num_layers):
            gate = torch.sigmoid(self.gate[layer](x))
            nonlinear = F.relu(self.nonlinear[layer](x))
            x = gate * nonlinear + (1 - gate) * x
        return x
```

## Q12: Model Interpretability

**Answer:**
Implementation of techniques for interpreting neural networks:

```python
import torch
import numpy as np
from torch.autograd import Variable
import matplotlib.pyplot as plt

class ModelInterpreter:
    def __init__(self, model):
        self.model = model
        self.model.eval()
    
    def compute_gradients(self, input_data, target_class):
        """Compute gradients with respect to input"""
        input_var = Variable(input_data, requires_grad=True)
        
        # Forward pass
        output = self.model(input_var)
        
        # Zero gradients
        self.model.zero_grad()
        
        # Backward pass
        output[0, target_class].backward()
        
        return input_var.grad.data.numpy()
    
    def generate_saliency_map(self, input_data, target_class):
        """Generate saliency map for input"""
        gradients = self.compute_gradients(input_data, target_class)
        saliency = np.abs(gradients).max(axis=1)[0]
        
        return saliency
    
    def integrated_gradients(self, input_data, target_class, steps=50):
        """Compute integrated gradients"""
        baseline = torch.zeros_like(input_data)
        scaled_inputs = [baseline + (float(i) / steps) * (input_data - baseline) 
                        for i in range(steps + 1)]
        
        grads = [self.compute_gradients(scaled_input, target_class) 
                for scaled_input in scaled_inputs]
        
        integrated_grads = np.average(grads[:-1], axis=0)
        return integrated_grads * (input_data.numpy() - baseline.numpy())
    
    def plot_attribution(self, attribution_map, title="Attribution Map"):
        """Plot attribution map"""
        plt.figure(figsize=(10, 5))
        plt.imshow(attribution_map, cmap='viridis')
        plt.colorbar()
        plt.title(title)
        plt.show()

# Usage example
def interpretability_example():
    interpreter = ModelInterpreter(model)
    
    # Generate saliency map
    saliency = interpreter.generate_saliency_map(input_data, target_class)
    interpreter.plot_attribution(saliency, "Saliency Map")
    
    # Compute integrated gradients
    ig = interpreter.integrated_gradients(input_data, target_class)
    interpreter.plot_attribution(ig, "Integrated Gradients")
```

## Q13: Advanced Training Strategies

**Answer:**
Implementation of advanced training strategies:

```python
class AdvancedTrainer:
    def __init__(self, model, optimizer, scheduler):
        self.model = model
        self.optimizer = optimizer
        self.scheduler = scheduler
        self.scaler = torch.cuda.amp.GradScaler()  # For mixed precision
    
    def train_with_mixed_precision(self, data_loader):
        """Training with mixed precision"""
        self.model.train()
        total_loss = 0
        
        for batch_x, batch_y in data_loader:
            # Forward pass with mixed precision
            with torch.cuda.amp.autocast():
                outputs = self.model(batch_x)
                loss = F.cross_entropy(outputs, batch_y)
            
            # Backward pass with gradient scaling
            self.optimizer.zero_grad()
            self.scaler.scale(loss).backward()
            self.scaler.step(self.optimizer)
            self.scaler.update()
            
            total_loss += loss.item()
        
        return total_loss / len(data_loader)
    
    def train_with_gradient_accumulation(self, data_loader, accumulation_steps=4):
        """Training with gradient accumulation"""
        self.model.train()
        total_loss = 0
        self.optimizer.zero_grad()
        
        for i, (batch_x, batch_y) in enumerate(data_loader):
            outputs = self.model(batch_x)
            loss = F.cross_entropy(outputs, batch_y)
            loss = loss / accumulation_steps
            loss.backward()
            
            if (i + 1) % accumulation_steps == 0:
                self.optimizer.step()
                self.optimizer.zero_grad()
            
            total_loss += loss.item()
        
        return total_loss / len(data_loader)
    
    def train_with_curriculum(self, data_loaders, epochs_per_stage=5):
        """Curriculum learning"""
        stages = len(data_loaders)
        history = []
        
        for stage in range(stages):
            print(f"Training Stage {stage + 1}/{stages}")
            data_loader = data_loaders[stage]
            
            for epoch in range(epochs_per_stage):
                loss = self.train_with_mixed_precision(data_loader)
                self.scheduler.step()
                history.append({'stage': stage, 'epoch': epoch, 'loss': loss})
        
        return history

# Usage example
def advanced_training_example():
    trainer = AdvancedTrainer(model, optimizer, scheduler)
    
    # Train with mixed precision
    loss = trainer.train_with_mixed_precision(train_loader)
    
    # Train with gradient accumulation
    loss = trainer.train_with_gradient_accumulation(train_loader)
    
    # Train with curriculum learning
    history = trainer.train_with_curriculum([easy_loader, medium_loader, hard_loader])
```

## Q14: Model Deployment and Optimization

**Answer:**
Implementation of model deployment and optimization techniques:

```python
import torch.onnx
import torch.quantization

class ModelOptimizer:
    def __init__(self, model):
        self.model = model
    
    def quantize_model(self):
        """Quantize model to int8"""
        # Configure model for quantization
        self.model.qconfig = torch.quantization.get_default_qconfig('fbgemm')
        torch.quantization.prepare(self.model, inplace=True)
        
        # Calibrate with sample data
        self.model.eval()
        with torch.no_grad():
            for batch_x, _ in calibration_loader:
                self.model(batch_x)
        
        # Convert to quantized model
        torch.quantization.convert(self.model, inplace=True)
        return self.model
    
    def export_to_onnx(self, sample_input, path='model.onnx'):
        """Export model to ONNX format"""
        torch.onnx.export(
            self.model,
            sample_input,
            path,
            export_params=True,
            opset_version=11,
            do_constant_folding=True,
            input_names=['input'],
            output_names=['output'],
            dynamic_axes={
                'input': {0: 'batch_size'},
                'output': {0: 'batch_size'}
            }
        )
    
    def optimize_for_inference(self):
        """Optimize model for inference"""
        self.model.eval()
        
        # Fusion of operations
        self.model = torch.jit.script(self.model)
        self.model = torch.jit.freeze(self.model)
        
        return self.model
    
    def benchmark_model(self, input_shape, num_runs=100):
        """Benchmark model performance"""
        self.model.eval()
        device = next(self.model.parameters()).device
        dummy_input = torch.randn(input_shape).to(device)
        
        # Warm-up
        for _ in range(10):
            _ = self.model(dummy_input)
        
        # Benchmark
        start_time = time.time()
        for _ in range(num_runs):
            _ = self.model(dummy_input)
        end_time = time.time()
        
        avg_time = (end_time - start_time) / num_runs
        return {
            'average_time': avg_time,
            'fps': 1.0 / avg_time
        }

class ModelServer:
    def __init__(self, model):
        self.model = model
        self.model.eval()
    
    def preprocess_input(self, raw_input):
        """Preprocess input data"""
        # Implement preprocessing logic
        return processed_input
    
    def postprocess_output(self, model_output):
        """Postprocess model output"""
        # Implement postprocessing logic
        return processed_output
    
    def inference(self, input_data):
        """Run inference"""
        with torch.no_grad():
            processed_input = self.preprocess_input(input_data)
            output = self.model(processed_input)
            return self.postprocess_output(output)

# Usage example
def deployment_example():
    # Initialize optimizer
    optimizer = ModelOptimizer(model)
    
    # Quantize model
    quantized_model = optimizer.quantize_model()
    
    # Export to ONNX
    optimizer.export_to_onnx(sample_input)
    
    # Optimize for inference
    optimized_model = optimizer.optimize_for_inference()
    
    # Benchmark model
    benchmark_results = optimizer.benchmark_model((1, 3, 224, 224))
    
    # Deploy model
    server = ModelServer(optimized_model)
    result = server.inference(input_data)
    
    return benchmark_results
```

[End of Neural Networks Section] 