"""
Complete AI & ML Basics module with professional foundation content
"""
import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def update_lesson(db: Session, module_name: str, lesson_num: int, title: str, content: str):
    module = db.query(Module).filter(Module.title == module_name).first()
    if not module:
        return False
    
    lesson = db.query(Lesson).filter(
        Lesson.module_id == module.id,
        Lesson.order == lesson_num
    ).first()
    
    if lesson:
        lesson.content_markdown = content.strip()
        lesson.is_published = True
        db.commit()
        return True
    return False

def create_aiml_content(db: Session):
    """Create AI & ML Basics content"""
    print("🤖 Creating AI & ML Basics content...")
    
    aiml_lessons = [
        (1, "Introduction to AI/ML", """
# Introduction to AI/ML

## What is Artificial Intelligence?

**Artificial Intelligence (AI)** - Computer systems that perform tasks requiring human intelligence

### AI Categories

**Narrow AI (Weak AI)**
- Designed for specific tasks
- Current state of AI
- Examples: Spam filters, voice assistants, chess programs

**General AI (Strong AI)**  
- Human-level intelligence across domains
- Can learn and transfer knowledge
- Doesn't exist yet

**Super AI**
- Beyond human intelligence
- Theoretical concept

## AI vs ML vs DL

```
Artificial Intelligence
  └── Machine Learning
        └── Deep Learning
```

**Artificial Intelligence**
- Broad field of intelligent machines
- Includes rule-based systems
- Example: Chess AI with programmed rules

**Machine Learning**
- Learn from data without explicit programming
- Subset of AI
- Example: Email spam detection that improves over time

**Deep Learning**
- Neural networks with many layers  
- Subset of ML
- Example: Image recognition, language models

## Types of Machine Learning

### 1. Supervised Learning

**Learn from labeled examples**

```python
# Training data with labels
examples = [
    ("192.168.1.1", "normal"),
    ("10.0.0.1", "malicious"),
    ("172.16.0.1", "normal")
]

# Model learns patterns
model.train(examples)

# Make predictions
prediction = model.predict("192.168.2.1")
```

**Security Applications:**
- Malware classification (malicious/benign)
- Phishing detection (phishing/legitimate)
- Intrusion detection (attack/normal)

### 2. Unsupervised Learning

**Find patterns in unlabeled data**

```python
# Data without labels
network_traffic = [packet1, packet2, packet3, ...]

# Find patterns
clusters = model.cluster(network_traffic)

# Anomalies are outliers
anomalies = model.detect_anomalies(network_traffic)
```

**Security Applications:**
- Zero-day attack detection
- User behavior analytics
- Network traffic analysis

### 3. Reinforcement Learning

**Learn through trial and error with rewards**

```
Agent → Action → Environment → Reward → Learn
```

**Security Applications:**
- Automated penetration testing
- Adaptive defense systems
- Game simulations

## ML in Cybersecurity

### Threat Detection
- **Malware Detection** - Identify malicious files
- **Network Intrusion** - Spot unusual traffic
- **Phishing** - Classify suspicious emails

### Automation
- **Log Analysis** - Parse millions of events
- **Incident Triage** - Prioritize alerts
- **Vulnerability Assessment** - Rank risks

### Adversarial Use
- **AI-powered attacks** - Automated exploitation
- **Deepfakes** - Fake media
- **Social engineering** - Targeted phishing

## Key Terminology

| Term | Definition |
|------|------------|
| **Model** | Learned representation of patterns |
| **Training** | Teaching model from data |
| **Features** | Input variables for prediction |
| **Label** | Target variable (answer) |
| **Dataset** | Collection of training examples |
| **Accuracy** | % of correct predictions |
| **Overfitting** | Model too specific to training data |

## Simple ML Example

```python
from sklearn.tree import DecisionTreeClassifier

# Training data: [file_size, has_packer, num_imports]
X_train = [
    [1024, 1, 50],    # Malware
    [2048, 0, 20],    # Benign
    [5120, 1, 100],   # Malware
    [1536, 0, 15]     # Benign
]
y_train = ['malware', 'benign', 'malware', 'benign']

# Train model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Predict new file
new_file = [[3000, 1, 75]]
prediction = model.predict(new_file)
print(prediction)  # ['malware']
```

## Challenges in Security ML

1. **Adversarial Attacks** - Attackers trick models
2. **Data Quality** - Need labeled security data
3. **False Positives** - Too many false alerts
4. **Explainability** - Why did model decide?
5. **Evasion** - Attacks adapt to bypass detection

## Ethics & Bias

- ML models can inherit biases from data
- Privacy concerns with data collection
- Accountability for AI decisions
- Transparency vs black box models

## Key Takeaways

- AI ⊃ ML ⊃ DL (nested relationship)
- Supervised, unsupervised, reinforcement learning
- ML powerful for security automation
- Also creates new attack vectors
- Understanding ML crucial for modern security

**Next:** Machine learning fundamentals
"""),
        
        (2, "Machine Learning Fundamentals", """
# Machine Learning Fundamentals

## The ML Workflow

```
1. Problem Definition → What are we predicting?
2. Data Collection → Gather training data
3. Data Preprocessing → Clean and prepare
4. Feature Engineering → Select important features
5. Model Selection → Choose algorithm
6. Training → Teach the model
7. Evaluation → Test performance
8. Deployment → Use in production
```

## Core Concepts

### Features (X)
Input variables used for prediction

```python
# Network traffic features
features = {
    'packet_size': 1500,
    'duration': 0.5,
    'protocol': 'TCP',
    'port': 443
}
```

### Labels (y)
Target variable to predict

```python
label = 'normal'  # or 'attack'
```

### Training vs Testing Data

```python
from sklearn.model_selection import train_test_split

# Split 80/20
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train on training data
model.fit(X_train, y_train)

# Test on unseen data
accuracy = model.score(X_test, y_test)
```

## Common Algorithms

### 1. Decision Trees

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Makes yes/no decisions at each node
```

### 2. Random Forest

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Multiple decision trees voting
```

### 3. K-Nearest Neighbors

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# Classifies based on similar examples
```

### 4. Logistic Regression

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)

# Binary classification
```

## Evaluation Metrics

```python
from sklearn.metrics import accuracy_score, precision_score, recall_score

predictions = model.predict(X_test)

# Accuracy: Overall correctness
accuracy = accuracy_score(y_test, predictions)

# Precision: Of predicted positives, how many correct?
precision = precision_score(y_test, predictions)

# Recall: Of actual positives, how many found?
recall = recall_score(y_test, predictions)

print(f"Accuracy: {accuracy:.2f}")
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
```

### Confusion Matrix

```
                Predicted
               Pos    Neg
Actual  Pos    TP     FN
        Neg    FP     TN

TP = True Positive
TN = True Negative
FP = False Positive (False alarm)
FN = False Negative (Missed attack)
```

## Practical Example: Malware Detection

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Load data
data = pd.read_csv('malware_dataset.csv')

# Features
X = data[['file_size', 'entropy', 'num_imports', 'has_packer']]
y = data['label']  # 'malware' or 'benign'

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print(f"Accuracy: {accuracy:.2%}")

# Predict new file
new_file = [[5000, 7.8, 150, 1]]
prediction = model.predict(new_file)
print(f"Prediction: {prediction[0]}")
```

## Overfitting vs Underfitting

**Overfitting**
- Model too complex
- Memorizes training data
- Poor on new data

**Underfitting**
- Model too simple
- Doesn't capture patterns
- Poor everywhere

**Solution:** Cross-validation, regularization

## Cross-Validation

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5)
print(f"Average accuracy: {scores.mean():.2f}")
```

## Feature Importance

```python
# Which features matter most?
importances = model.feature_importances_
for feature, importance in zip(feature_names, importances):
    print(f"{feature}: {importance:.3f}")
```

## Key Takeaways

- ML workflow: data → train → evaluate → deploy
- Choose appropriate algorithm for your problem
- Always split into training and testing data
- Multiple metrics beyond accuracy
- Beware overfitting

**Next:** Data preprocessing techniques
"""),
        
        (3, "Data Preprocessing", """
# Data Preprocessing

## Why Preprocessing Matters

```
Garbage In = Garbage Out

Quality data = Better models
```

## Handling Missing Data

```python
import pandas as pd
import numpy as np

# Create dataset with missing values
data = pd.DataFrame({
    'ip': ['192.168.1.1', '10.0.0.1', None],
    'port': [80, 443, 22],
    'packets': [100, None, 50]
})

# Option 1: Remove rows with missing data
data_clean = data.dropna()

# Option 2: Fill with specific value
data_filled = data.fillna(0)

# Option 3: Fill with mean
data['packets'].fillna(data['packets'].mean(), inplace=True)
```

## Encoding Categorical Data

```python
from sklearn.preprocessing import LabelEncoder

# Convert text labels to numbers
data = ['HTTP', 'SSH', 'FTP', 'HTTP', 'SSH']

encoder = LabelEncoder()
encoded = encoder.fit_transform(data)
# Result: [0, 1, 2, 0, 1]

# Decode back
decoded = encoder.inverse_transform(encoded)
```

## Feature Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Standard Scaling (mean=0, std=1)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Min-Max Scaling (0 to 1)
scaler = MinMaxScaler()
X_normalized = scaler.fit_transform(X)
```

Why? Algorithms like KNN and SVM sensitive to scale.

## Feature Engineering

Create new features from existing ones:

```python
# Extract features from timestamp
data['hour'] = pd.to_datetime(data['timestamp']).dt.hour
data['day_of_week'] = pd.to_datetime(data['timestamp']).dt.dayofweek

# Create ratio features
data['failed_login_rate'] = data['failed_logins'] / data['total_logins']

# Combine features
data['port_protocol'] = data['port'].astype(str) + '_' + data['protocol']
```

## Outlier Detection

```python
# Z-score method
from scipy import stats

z_scores = np.abs(stats.zscore(data['packet_size']))
outliers = np.where(z_scores > 3)

# IQR method
Q1 = data['packet_size'].quantile(0.25)
Q3 = data['packet_size'].quantile(0.75)
IQR = Q3 - Q1

outliers = (data['packet_size'] < Q1 - 1.5*IQR) | (data['packet_size'] > Q3 + 1.5*IQR)
```

## Data Balancing

```python
from imblearn.over_sampling import SMOTE

# Deal with imbalanced classes
# (e.g., 95% normal, 5% attack)

smote = SMOTE()
X_balanced, y_balanced = smote.fit_resample(X, y)
```

## Complete Preprocessing Pipeline

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# Load data
data = pd.read_csv('network_traffic.csv')

# Handle missing values
data = data.dropna()

# Encode categorical variables
le = LabelEncoder()
data['protocol'] = le.fit_transform(data['protocol'])

# Select features
X = data[['src_port', 'dst_port', 'protocol', 'packet_size']]
y = data['label']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier()
model.fit(X_train_scaled, y_train)

# Evaluate
accuracy = model.score(X_test_scaled, y_test)
print(f"Accuracy: {accuracy:.2%}")
```

## Best Practices

1. **Understand your data** - Explore before preprocessing
2. **Handle missing data appropriately** - Don't just delete
3. **Scale features** - Especially for distance-based algorithms
4. **Engineer meaningful features** - Domain knowledge helps
5. **Keep test data separate** - No data leakage
6. **Document your pipeline** - Reproducibility matters

## Key Takeaways

- Clean data is crucial for ML success
- Handle missing values appropriately
- Encode categorical variables
- Scale numerical features
- Engineer domain-specific features
- Watch for data leakage

**Next:** Classification algorithms
"""),
        
        (4, "Classification Algorithms", """
# Classification Algorithms

## What is Classification?

Predicting categorical labels:
- Spam or not spam?
- Malware or benign?
- Attack type? (DoS, Scan, Normal)

## Decision Trees

**How it works:** Series of yes/no questions

```
Is file_size > 5000?
├─ Yes: Is entropy > 7.0?
│  ├─ Yes: MALWARE
│  └─ No: BENIGN
└─ No: BENIGN
```

```python
from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=5)
model.fit(X_train, y_train)

# Visualize importance
importances = model.feature_importances_
```

**Pros:** Easy to understand, fast
**Cons:** Can overfit, unstable

## Random Forest

**Ensemble of many decision trees**

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(
    n_estimators=100,  # Number of trees
    max_depth=10,
    random_state=42
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

**Pros:** Accurate, handles overfitting better
**Cons:** Slower, harder to interpret

## Support Vector Machines (SVM)

**Find optimal boundary between classes**

```python
from sklearn.svm import SVC

model = SVC(kernel='rbf', C=1.0)
model.fit(X_train, y_train)
```

**Pros:** Effective in high dimensions
**Cons:** Slow on large datasets, needs scaling

## K-Nearest Neighbors (KNN)

**Classify based on k closest examples**

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
```

**Pros:** Simple, no training needed
**Cons:** Slow predictions, sensitive to scale

## Logistic Regression

**Despite name, used for classification**

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)

# Get probabilities
probabilities = model.predict_proba(X_test)
```

**Pros:** Fast, interpretable, probabilistic output
**Cons:** Assumes linear decision boundary

## Naive Bayes

**Based on Bayes' theorem**

```python
from sklearn.naive_bayes import GaussianNB

model = GaussianNB()
model.fit(X_train, y_train)
```

**Pros:** Fast, works well with text
**Cons:** Assumes feature independence

## Comparison Table

| Algorithm | Speed | Accuracy | Interpretability |
|-----------|-------|----------|------------------|
| Decision Tree | Fast | Medium | High |
| Random Forest | Medium | High | Medium |
| SVM | Slow | High | Low |
| KNN | Slow | Medium | Medium |
| Logistic Reg | Fast | Medium | High |
| Naive Bayes | Fast | Medium | High |

## Practical: Email Phishing Detection

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Sample data
emails = [
    "Urgent: Verify your account now!",
    "Meeting tomorrow at 3pm",
    "You won a prize! Click here",
    "Project update attached"
]
labels = ['phishing', 'legitimate', 'phishing', 'legitimate']

# Convert text to features
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(emails)

# Train classifier
model = RandomForestClassifier()
model.fit(X, labels)

# Predict new email
new_email = ["Confirm your password immediately"]
X_new = vectorizer.transform(new_email)
prediction = model.predict(X_new)
print(f"Prediction: {prediction[0]}")
```

## Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

# Grid search
grid_search = GridSearchCV(
    RandomForestClassifier(),
    param_grid,
    cv=5,
    scoring='accuracy'
)

grid_search.fit(X_train, y_train)

# Best parameters
print(grid_search.best_params_)
best_model = grid_search.best_estimator_
```

## Key Takeaways

- Different algorithms for different problems
- Random Forest: good default choice  
- SVM: when accuracy critical
- Logistic Regression: when speed matters
- Always tune hyperparameters
- Evaluate on multiple metrics

**Next:** Neural networks introduction
"""),
        
        (5, "Neural Networks Intro", """
# Neural Networks Introduction

## What are Neural Networks?

Inspired by the human brain, neural networks learn complex patterns.

```
Input Layer → Hidden Layer(s) → Output Layer
```

## Perceptron (Simple Neuron)

```python
import numpy as np

def perceptron(inputs, weights, bias):
    # Weighted sum
    total = np.dot(inputs, weights) + bias
    
    # Activation (step function)
    return 1 if total > 0 else 0

# Example
inputs = [1, 0, 1]  # Features
weights = [0.5, -0.3, 0.8]
bias = 0.1

output = perceptron(inputs, weights, bias)
```

## Multi-Layer Neural Network

```python
from sklearn.neural_network import MLPClassifier

# Create neural network
model = MLPClassifier(
    hidden_layer_sizes=(100, 50),  # Two hidden layers
    activation='relu',
    max_iter=1000
)

model.fit(X_train, y_train)
predictions = model.predict(X_test)
```

## Activation Functions

```python
# ReLU (Rectified Linear Unit)
def relu(x):
    return max(0, x)

# Sigmoid
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Tanh
def tanh(x):
    return np.tanh(x)
```

## Deep Learning with Keras

```python
from tensorflow import keras
from tensorflow.keras import layers

# Build model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=(10,)),
    layers.Dropout(0.2),
    layers.Dense(32, activation='relu'),
    layers.Dense(1, activation='sigmoid')
])

# Compile
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

# Train
history = model.fit(
    X_train, y_train,
    epochs=10,
    batch_size=32,
    validation_split=0.2
)

# Evaluate
loss, accuracy = model.evaluate(X_test, y_test)
```

## Convolutional Neural Networks (CNN)

For image analysis (malware visualization):

```python
model = keras.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(10, activation='softmax')
])
```

## Recurrent Neural Networks (RNN)

For sequence data (network traffic over time):

```python
from tensorflow.keras.layers import LSTM

model = keras.Sequential([
    LSTM(50, return_sequences=True, input_shape=(100, 5)),
    LSTM(50),
    layers.Dense(1, activation='sigmoid')
])
```

## Security Applications

### Malware Detection
```python
# Image representation of binary
from PIL import Image

def binary_to_image(binary_path):
    with open(binary_path, 'rb') as f:
        data = f.read()
    
    # Convert to grayscale image
    # Feed to CNN
```

### Network Intrusion Detection
```python
# Time series of network packets
# Use LSTM to detect anomalies
```

### Phishing Detection
```python
# Text classification
# Use word embeddings + neural network
```

## Challenges

**Overfitting**
```python
# Use dropout and regularization
layers.Dropout(0.5)
```

**Vanishing Gradients**
```python
# Use ReLU activation
# Use batch normalization
```

**Computational Cost**
```python
# Use GPU acceleration
# Start with smaller networks
```

## Key Concepts

- **Epoch:** One pass through entire dataset
- **Batch Size:** Samples processed before update
- **Learning Rate:** How fast model learns
- **Dropout:** Randomly disable neurons (prevent overfitting)

## Key Takeaways

- Neural networks learn complex patterns
- Multiple layers = deep learning
- Different architectures for different data
- CNN for images, RNN for sequences
- Requires more data and computation
- Powerful but can be black box

**Next:** AI for security applications
"""),
        
        (6, "AI for Security Applications", """
# AI for Security Applications

## Malware Detection

### Traditional vs ML Approach

**Traditional (Signatures)**
```
Known malware hash → Database → Match/No match
```
- Fast but only catches known malware
- Zero-day attacks slip through

**ML Approach**
```
File features → ML Model → Malicious/Benign score
```
- Can detect unknown malware
- Based on behavior patterns

### Feature Extraction

```python
import pefile

def extract_features(file_path):
    pe = pefile.PE(file_path)
    
    features = {
        'file_size': os.path.getsize(file_path),
        'num_sections': len(pe.sections),
        'num_imports': len(pe.DIRECTORY_ENTRY_IMPORT),
        'entropy': calculate_entropy(file_path),
        'has_packer': detect_packer(pe)
    }
    
    return features

# Train classifier
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)  # X = features, y = labels

# Classify new file
features = extract_features("suspicious.exe")
prediction = model.predict([list(features.values())])
```

## Network Intrusion Detection

### Anomaly-Based IDS

```python
from sklearn.ensemble import IsolationForest

# Train on normal traffic
normal_traffic = load_normal_traffic()

model = IsolationForest(contamination=0.01)
model.fit(normal_traffic)

# Detect anomalies
new_traffic = capture_traffic()
predictions = model.predict(new_traffic)

# -1 = anomaly, 1 = normal
anomalies = new_traffic[predictions == -1]
```

### Deep Learning for Traffic Analysis

```python
from tensorflow import keras

# LSTM for sequential packet analysis
model = keras.Sequential([
    keras.layers.LSTM(64, input_shape=(100, 10)),
    keras.layers.Dense(32, activation='relu'),
    keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy')
model.fit(X_train, y_train, epochs=10)
```

## Phishing Detection

### URL Analysis

```python
def extract_url_features(url):
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    
    features = {
        'length': len(url),
        'num_dots': url.count('.'),
        'has_ip': bool(re.match(r'\\d+\\.\\d+\\.\\d+\\.\\d+', parsed.netloc)),
        'uses_https': parsed.scheme == 'https',
        'has_suspicious_words': any(word in url.lower() for word in ['login', 'verify', 'account'])
    }
    
    return features

# Train classifier
from sklearn.ensemble import GradientBoostingClassifier

model = GradientBoostingClassifier()
model.fit(url_features, labels)

# Predict
new_url = "http://paypa1.com/verify"
features = extract_url_features(new_url)
is_phishing = model.predict([list(features.values())])
```

### Email Content Analysis

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

# Vectorize email text
vectorizer = TfidfVectorizer(max_features=1000)
X = vectorizer.fit_transform(email_texts)

# Train classifier
model = MultinomialNB()
model.fit(X, labels)

# Classify new email
new_email = ["Urgent: Verify your account"]
X_new = vectorizer.transform(new_email)
prediction = model.predict(X_new)
```

##User Behavior Analytics (UBA)

```python
# Detect anomalous user behavior
from sklearn.ensemble import IsolationForest

# Features: login times, locations, actions
user_activities = [
    [9, 'office', 50],    # hour, location, num_actions
    [14, 'office', 45],
    [2, 'foreign', 200]   # Anomaly!
]

model = IsolationForest()
model.fit(user_activities)

# Predict
new_activity = [[3, 'foreign', 150]]
is_anomaly = model.predict(new_activity)
```

## Threat Intelligence

### Automated IOC Extraction

```python
import re

def extract_iocs(text):
    iocs = {
        'ips': re.findall(r'\\d+\\.\\d+\\.\\d+\\.\\d+', text),
        'domains': re.findall(r'[a-zA-Z0-9-]+\\.[a-zA-Z]{2,}', text),
        'hashes': re.findall(r'\\b[a-f0-9]{32,64}\\b', text)
    }
    return iocs

# Process threat report
report = "Malware 5f4dcc3b5aa765d61d8327deb882cf99 contacted 192.168.1.1"
iocs = extract_iocs(report)
```

## Adversarial Machine Learning

### Evasion Attacks

```python
# Attacker modifies malware to evade detection
# Add benign features, reduce malicious features

original_features = [5000, 7.8, 150, 1]  # Detected as malware

# Modify slightly
evaded_features = [5000, 6.9, 145, 0]  # May evade

prediction = model.predict([evaded_features])
```

### Defense

```python
# Adversarial training
from cleverhans.tf2.attacks import fast_gradient_method

# Generate adversarial examples during training
# Makes model more robust
```

## Automated Vulnerability Assessment

```python
# ML to prioritize vulnerabilities

vuln_features = [
    [9.8, 1, 1, 0],  # CVSS, exploited, public_exploit, patch_available
    [5.0, 0, 0, 1]
]

# Predict risk level
risk_model.predict(vuln_features)
```

## Best Practices

1. **Start simple** - Baseline models first
2. **Feature engineering** - Domain knowledge crucial
3. **Handle imbalanced data** - Attacks are rare
4. **Continuous retraining** - Threats evolve
5. **Human in the loop** - ML assists, not replaces
6. **Monitor for adversarial attacks** - Attackers adapt

## Real-World Tools

- **Cylance** - ML-based antivirus
- **Darktrace** - AI-powered network defense
- **Vectra** - Network threat detection
- **Splunk UBA** - User behavior analytics

## Key Takeaways

- ML enhances traditional security
- Malware detection, intrusion detection, phishing
- Anomaly detection for unknown threats
- Adversarial ML is arms race
- Combine ML with human expertise
- Continuous adaptation required

---

## 🎉 Tier 0 Complete!

**Congratulations!** You've completed all foundational modules:
- ✅ Linux Basics
- ✅ Networking Fundamentals  
- ✅ Python for Security
- ✅ AI & ML Basics

**You're now ready for Tier 1: AI in Cybersecurity!**
"""
        )
    ]
    
    for num, title, content in aiml_lessons:
        if update_lesson(db, "AI & ML Basics", num, title, content):
            print(f"  ✅ Lesson {num}: {title}")
    
    print("\\n✅ AI & ML Basics complete!")
    print("\\n🎉🎉🎉 TIER 0 FULLY COMPLETE! 🎉🎉🎉")
    print("All 36 lessons across 4 modules now have professional content!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_aiml_content(db)
    finally:
        db.close()
