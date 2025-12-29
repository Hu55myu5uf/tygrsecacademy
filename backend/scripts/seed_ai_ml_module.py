
import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson

def seed_ai_ml_module(db: Session):
    """Seed AI & ML Basics module for Tier 0"""
    print("Seeding AI & ML Basics module...")
    
    tier0 = db.query(Tier).filter(Tier.tier_number == 0).first()
    if not tier0:
        print("ERROR: Tier 0 not found!")
        return
    
    existing = db.query(Module).filter(
        Module.tier_id == tier0.id,
        Module.title == "AI & ML Basics"
    ).first()
    
    if existing:
        print("Module already exists. Skipping.")
        return
    
    ai_module = Module(
        tier_id=tier0.id,
        title="AI & ML Basics",
        description="Introduction to Artificial Intelligence and Machine Learning for cybersecurity. Learn fundamentals of AI/ML and their applications in security.",
        order=4,
        estimated_hours=5,
        is_published=True
    )
    
    db.add(ai_module)
    db.commit()
    db.refresh(ai_module)
    
    lessons = [
        {
            "title": "Introduction to AI/ML",
            "description": "AI vs ML vs DL, and use cases in cybersecurity",
            "duration": 40,
            "published": True,
            "content": """
# Introduction to AI/ML

## What is Artificial Intelligence?

**Definition:** Systems that can perform tasks that normally require human intelligence

### Types of AI

1. **Narrow AI (Weak AI)**
   - Designed for specific tasks
   - Example: Spam filters, voice assistants
   - **What we have today**

2. **General AI (Strong AI)**
   - Human-level intelligence across domains
   - Can transfer learning between tasks
   - **Doesn't exist yet**

3. **Super AI**
   - Surpasses human intelligence
   - Theoretical concept

## AI vs ML vs DL

```
Artificial Intelligence
  └── Machine Learning
        └── Deep Learning
```

### Artificial Intelligence
- Broad field of creating intelligent machines
- Includes rule-based systems, expert systems
- Example: Chess program with predefined rules

### Machine Learning
- **Subset of AI**
- Systems that learn from data without explicit programming
- Example: Email spam detection that improves over time

### Deep Learning
- **Subset of ML**
- Uses neural networks with multiple layers
- Example: Image recognition, language models

## Types of Machine Learning

### 1. Supervised Learning
**Definition:** Learn from labeled data

**Process:**
```
Input (features) + Label (answer) → Model → Predictions
```

**Examples:**
- **Classification:** Is this email spam or not?
- **Regression:** Predict network traffic volume

**Security Applications:**
- Malware detection (malicious/benign)
- Phishing detection (phishing/legitimate)
- Intrusion detection (attack/normal)

### 2. Unsupervised Learning
**Definition:** Find patterns in unlabeled data

**Process:**
```
Input (no labels) → Model → Patterns/Groups
```

**Examples:**
- **Clustering:** Group similar network traffic
- **Anomaly Detection:** Find unusual behavior

**Security Applications:**
- Detect zero-day attacks (unusual patterns)
- User behavior analytics
- Network traffic analysis

### 3. Reinforcement Learning
**Definition:** Learn through trial and error with rewards

**Process:**
```
Agent → Action → Environment → Reward → Learn
```

**Examples:**
- Game playing (AlphaGo)
- Robotics

**Security Applications:**
- Automated penetration testing
- Adaptive defense systems

## ML Workflow

```
1. Problem Definition
   ↓
2. Data Collection
   ↓
3. Data Preprocessing
   ↓
4. Feature Engineering
   ↓
5. Model Selection
   ↓
6. Training
   ↓
7. Evaluation
   ↓
8. Deployment
   ↓
9. Monitoring
```

## AI/ML in Cybersecurity

### Threat Detection
- **Malware Detection:** Identify malicious software
- **Anomaly Detection:** Spot unusual network behavior
- **Phishing Detection:** Classify emails

### Security Automation
- **Log Analysis:** Parse millions of logs automatically
- **Incident Response:** Automated threat triage
- **Vulnerability Assessment:** Prioritize vulnerabilities

### Adversarial Applications
- **Social Engineering:** AI-generated phishing
- **Deepfakes:** Fake videos/audio
- **Automated Attacks:** AI-powered hacking tools

## Key Terminology

| Term | Definition |
|------|------------|
| **Model** | Mathematical representation of learned patterns |
| **Training** | Process of teaching model from data |
| **Features** | Input variables used for prediction |
| **Label** | Target variable to predict |
| **Dataset** | Collection of examples for training |
| **Algorithm** | Method for learning from data |
| **Accuracy** | Percentage of correct predictions |
| **Overfitting** | Model too specific to training data |
| **Bias** | Systematic error in predictions |

## Simple Example: Email Classification

```python
# Pseudocode
def classify_email(email):
    features = extract_features(email)
    # Features: sender, keywords, links, attachments
    
    prediction = model.predict(features)
    # Returns: "spam" or "legitimate"
    
    return prediction

# Training
training_data = load_emails_with_labels()
model = train_ml_model(training_data)

# Prediction
new_email = receive_email()
result = classify_email(new_email)
print(f"Email is: {result}")
```

## Common ML Algorithms (Preview)

- **Decision Trees:** If-then rules
- **Random Forest:** Multiple decision trees
- **K-Nearest Neighbors:** Similar to neighbors
- **Logistic Regression:** Binary classification
- **Neural Networks:** Brain-inspired networks
- **Support Vector Machines:** Find best boundary

## Challenges in Security ML

1. **Adversarial Attacks:** Attackers can trick ML models
2. **Data Quality:** Need large, labeled datasets
3. **False Positives:** Too many alerts fatigue analysts
4. **Explainability:** Understanding why model made decision
5. **Evasion:** Attackers adapt to bypass detection

## Ethics & Considerations

- **Privacy:** ML models can leak sensitive data
- **Bias:** Models reflect biases in training data
- **Accountability:** Who's responsible for AI decisions?
- **Transparency:** Black box models are hard to trust

## Key Takeaways

1. **AI ⊃ ML ⊃ DL** (nested relationship)
2. **Supervised vs Unsupervised vs Reinforcement** learning
3. **ML is powerful for security automation**
4. **But also creates new attack vectors**
5. **Understanding ML is crucial for modern security**

Next: Dive into Machine Learning fundamentals!
            """
        }
    ]
    
    # Quick lessons
    quick_lessons = [
        {"title": "Machine Learning Fundamentals", "description": "Supervised, unsupervised, reinforcement learning", "duration": 50},
        {"title": "Data Preprocessing", "description": "Cleaning, normalization, feature engineering", "duration": 45},
        {"title": "Classification Algorithms", "description": "Decision trees, SVM, random forests", "duration": 50},
        {"title": "Neural Networks Intro", "description": "Perceptrons, backpropagation, deep learning", "duration": 55},
        {"title": "AI for Security Applications", "description": "Malware detection, anomaly detection", "duration": 50}
    ]
    
    # Create detailed lesson 1
    for index, lesson_data in enumerate(lessons, start=1):
        lesson = Lesson(
            module_id=ai_module.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            order=index,
            duration_minutes=lesson_data["duration"],
            content_markdown=lesson_data["content"].strip(),
            is_published=lesson_data["published"]
        )
        db.add(lesson)
    
    # Create structure for lessons 2-6
    for index, lesson_data in enumerate(quick_lessons, start=2):
        lesson = Lesson(
            module_id=ai_module.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            order=index,
            duration_minutes=lesson_data["duration"],
            content_markdown=f"# {lesson_data['title']}\\n\\n*Comprehensive lesson on {lesson_data['description']} - content in development*",
            is_published=False
        )
        db.add(lesson)
    
    db.commit()
    print(f"✅ Created AI & ML Basics module with 6 lessons")
    print(f"   - Lesson 1: Full content")
    print(f"   - Lessons 2-6: Structure created")
    print(f"\\n🎉 TIER 0 COMPLETE! All 4 modules created with 36 total lessons")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_ai_ml_module(db)
    finally:
        db.close()
