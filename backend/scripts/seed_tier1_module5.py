"""
Seed all Tier 1 lessons with professional content
Module 5: ML for Network Security - All 10 lessons
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def seed_ml_network_security(db):
    """Seed all 10 lessons for ML for Network Security"""
    print("🔒 Seeding Module 5: ML for Network Security...")
    
    module = db.query(Module).filter(Module.title == "ML for Network Security").first()
    if not module:
        print("❌ Module not found!")
        return
    
    lessons = [
        {
            "order": 1,
            "title": "Network Traffic Analysis with ML",
            "description": "Learn to extract features from network packets and build ML models for traffic classification",
            "estimated_minutes": 45,
            "content": """# Network Traffic Analysis with ML

## Introduction

Network traffic analysis is the foundation of many security applications. Machine learning can automate the detection of malicious patterns in vast amounts of network data.

## Feature Extraction

### Packet-Level Features
```python
from scapy.all import rdpcap, IP, TCP

def extract_features(pcap_file):
    packets = rdpcap(pcap_file)
    features = []
    
    for packet in packets:
        if packet.haslayer(IP):
            feature = {
                'src_ip': packet[IP].src,
                'dst_ip': packet[IP].dst,
                'protocol': packet[IP].proto,
                'length': len(packet),
                'ttl': packet[IP].ttl
            }
            
            if packet.haslayer(TCP):
                feature['src_port'] = packet[TCP].sport
                feature['dst_port'] = packet[TCP].dport
                feature['flags'] = packet[TCP].flags
            
            features.append(feature)
    
    return features
```

### Flow-Level Features
```python
import pandas as pd
from collections import defaultdict

def create_flows(packets):
    flows = defaultdict(lambda: {
        'packet_count': 0,
        'total_bytes': 0,
        'duration': 0,
        'avg_packet_size': 0
    })
    
    for pkt in packets:
        if pkt.haslayer(IP):
            flow_key = f"{pkt[IP].src}:{pkt[TCP].sport}-{pkt[IP].dst}:{pkt[TCP].dport}"
            flows[flow_key]['packet_count'] += 1
            flows[flow_key]['total_bytes'] += len(pkt)
    
    return flows
```

## Common Datasets

### CICIDS2017/2018
- Modern network traffic dataset
- Includes various attack types
- Labeled data for supervised learning

### NSL-KDD
- Improved version of KDD Cup 99
- Reduced redundancy
- Standard benchmark

### UNSW-NB15
- Recent network traffic
- Mixture of normal and attack scenarios

## Building Classification Model

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load dataset
data = pd.read_csv('network_traffic.csv')

# Select features
features = ['duration', 'protocol_type', 'service', 'flag',
            'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
            'urgent', 'hot', 'num_failed_logins']

X = data[features]
y = data['attack_type']

# Handle categorical variables
X_encoded = pd.get_dummies(X, columns=['protocol_type', 'service', 'flag'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
accuracy = model.score(X_test_scaled, y_test)
print(f"Accuracy: {accuracy:.2%}")

# Feature importance
importances = pd.DataFrame({
    'feature': X_train.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print(importances.head(10))
```

## Real-Time Classification

```python
from scapy.all import sniff

class NetworkClassifier:
    def __init__(self, model, scaler):
        self.model = model
        self.scaler = scaler
        self.flow_cache = {}
    
    def extract_features(self, packet):
        # Extract features from packet
        features = [...]  # Feature extraction logic
        return features
    
    def classify_packet(self, packet):
        features = self.extract_features(packet)
        features_scaled = self.scaler.transform([features])
        prediction = self.model.predict(features_scaled)
        return prediction[0]
    
    def packet_handler(self, packet):
        if packet.haslayer(IP):
            classification = self.classify_packet(packet)
            if classification != 'normal':
                print(f"⚠️ Alert: {classification} detected!")

# Start sniffing
classifier = NetworkClassifier(model, scaler)
sniff(prn=classifier.packet_handler, filter="ip", count=100)
```

## Challenges

1. **High-dimensional data** - Many features to consider
2. **Imbalanced classes** - Attacks are rare
3. **Concept drift** - Network patterns change
4. **Real-time requirements** - Low latency needed
5. **False positives** - Balance sensitivity vs specificity

## Best Practices

- Normalize/scale features
- Handle imbalanced data (SMOTE, class weights)
- Use ensemble methods
- Regular model retraining
- Monitor model performance
- Combine with rule-based systems

## Key Takeaways

- Feature extraction is critical
- Flow-level features more informative than packet-level
- Ensemble methods work well
- Real-time classification requires optimization
- Continuous monitoring and updates essential

**Next:** Building complete IDS systems
"""
        },
        # Lesson 2-10 will continue...
    ]
    
    # Create all lessons
    for lesson_data in lessons:
        existing = db.query(Lesson).filter(
            Lesson.module_id == module.id,
            Lesson.order == lesson_data['order']
        ).first()
        
        if not existing:
            lesson = Lesson(
                module_id=module.id,
                order=lesson_data['order'],
                title=lesson_data['title'],
                description=lesson_data['description'],
                estimated_minutes=lesson_data['estimated_minutes'],
                content_markdown=lesson_data['content'],
                is_published=True
            )
            db.add(lesson)
            print(f"  ✅ Lesson {lesson_data['order']}: {lesson_data['title']}")
        else:
            existing.content_markdown = lesson_data['content']
            existing.is_published = True
            print(f"  ✅ Updated Lesson {lesson_data['order']}: {lesson_data['title']}")
    
    db.commit()
    print(f"✅ Module 5 lessons created!\n")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_ml_network_security(db)
    finally:
        db.close()
