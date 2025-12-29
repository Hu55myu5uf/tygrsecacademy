"""
Simplified Tier 1 seeding - all 25 lessons
Avoids f-string interpolation issues
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def create_lesson(db, module_id, order, title, desc, minutes, content):
    """Create or update a lesson"""
    existing = db.query(Lesson).filter(
        Lesson.module_id == module_id,
        Lesson.order == order
    ).first()
    
    if not existing:
        lesson = Lesson(
            module_id=module_id,
            order=order,
            title=title,
            description=desc,
            duration_minutes=minutes,
            content_markdown=content,
            is_published=True
        )
        db.add(lesson)
        print(f"  ✅ Created: {title}")
    else:
        existing.title = title
        existing.description = desc
        existing.duration_minutes = minutes
        existing.content_markdown = content
        existing.is_published = True
        print(f"  ✅ Updated: {title}")

def seed_tier1(db):
    print("🚀 Seeding Tier 1: AI in Cybersecurity")
    print("=" * 60)
    
    # Get modules
    ml_net = db.query(Module).filter(Module.title == "ML for Network Security").first()
    llm_soc = db.query(Module).filter(Module.title == "LLMs for SOC Operations").first()
    ai_code = db.query(Module).filter(Module.title == "AI-Powered Secure Coding").first()
    
    if not all([ml_net, llm_soc, ai_code]):
        print("❌ Modules not found!")
        return
    
    # Module 5: ML for Network Security
    print("\n📚 Module 5: ML for Network Security")
    
    create_lesson(db, ml_net.id, 1, "Network Traffic Analysis with ML", 
        "Learn feature extraction from network packets and build ML models for traffic classification", 45,
        """# Network Traffic Analysis with ML

## Overview
Apply machine learning to analyze network traffic and detect threats. Learn to extract features from packets and build classification models.

## Feature Extraction
```python
from scapy.all import rdpcap

def extract_features(pcap_file):
    packets = rdpcap(pcap_file)
    features = []
    for pkt in packets:
        if pkt.haslayer('IP'):
            features.append({
                'src_ip': pkt['IP'].src,
                'dst_ip': pkt['IP'].dst,
                'protocol': pkt['IP'].proto,
                'length': len(pkt)
            })
    return features
```

## Building Classifier
```python
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

data = pd.read_csv('network_traffic.csv')
X = data[['duration', 'protocol', 'src_bytes', 'dst_bytes']]
y = data['label']

model = RandomForestClassifier()
model.fit(X, y)
print("Trained successfully!")
```

## Key Takeaways
- Feature extraction is critical for ML-based network analysis
- Use datasets like CICIDS2017 for training
- Balance accuracy with real-time performance
- Combine ML with signature-based detection

**Resources:** CICIDS dataset, scikit-learn documentation, Scapy tutorial
""")

    create_lesson(db, ml_net.id, 2, "Building Intrusion Detection Systems",
        "Create ML-based IDS using supervised learning techniques", 50,
        """# Building Intrusion Detection Systems

## IDS Types
**Signature-Based:** Match known attack patterns
**Anomaly-Based (ML):** Detect deviations from normal behavior

## ML-Based IDS
```python
from sklearn.ensemble import IsolationForest

# Train on normal traffic
normal_traffic = load_normal_data()
model = IsolationForest(contamination=0.01)
model.fit(normal_traffic)

# Detect anomalies
predictions = model.predict(new_traffic)
anomalies = new_traffic[predictions == -1]
```

## Evaluation
```python
from sklearn.metrics import classification_report
print(classification_report(y_true, y_pred))
```

## Best Practices
- Balance false positives and false negatives
- Continuous learning from new data
- Human analyst oversight essential
- Integration with existing security infrastructure

**Resources:** Snort, Suricata, Zeek
""")

    create_lesson(db, ml_net.id, 3, "DDoS Detection and Mitigation",
        "Detect and respond to distributed denial of service attacks using ML", 45,
        """# DDoS Detection and Mitigation

## Understanding DDoS
Distributed Denial of Service attacks overwhelm systems with traffic from multiple sources.

## ML Detection
```python
def detect_ddos(traffic_features):
    # Features: packet rate, unique IPs, request patterns
    model = train_ddos_classifier()
    prediction = model.predict(traffic_features)
    return prediction == 'ddos'
```

## Mitigation Strategies
1. Traffic filtering
2. Rate limiting
3. Blackhole routing
4. CDN protection

## Key Metrics
- Requests per second
- Unique source IPs
- Traffic patterns
- Response times

**Tools:** Cloudflare, AWS Shield, Azure DDoS Protection
""")

    create_lesson(db, ml_net.id, 4, "Botnet Detection",
        "Identify botnet traffic patterns and C&C communications", 50,
        """# Botnet Detection

## Botnet Characteristics
- Command and Control (C&C) communication
- Synchronized behavior
- Periodic beaconing
- DNS anomalies

## Detection Techniques
```python
def analyze_dns_patterns(dns_logs):
    # Look for:
    # - DGA (Domain Generation Algorithm) domains
    # - Unusual query patterns
    # - High entropy domain names
    features = extract_dns_features(dns_logs)
    return model.predict(features)
```

## Network Behavior Analysis
- Traffic flow analysis
- Communication patterns
- Protocol anomalies

**Resources:** P2P botnet research, DNS security extensions
""")

    create_lesson(db, ml_net.id, 5, "Encrypted Traffic Analysis",
        "Analyze encrypted traffic metadata for threat detection", 55,
        """#  Encrypted Traffic Analysis

## Challenge
Most traffic is encrypted (HTTPS, TLS) - can't inspect payload

## Metadata Analysis
```python
def analyze_tls_metadata(connection):
    features = {
        'cert_length': len(connection.certificate),
        'cipher_suite': connection.cipher,
        'tls_version': connection.version,
        'cert_validity': connection.cert_valid_days,
        'sni': connection.server_name
    }
    return classify_traffic(features)
```

## TLS Fingerprinting
- JA3 fingerprints
- Certificate analysis
- Timing patterns

## Privacy Considerations
- Respect user privacy
- Comply with regulations
- Minimize data retention

**Tools:** Zeek, JA3, Suricata
""")

    create_lesson(db, ml_net.id, 6, "Network Anomaly Detection",
        "Use unsupervised learning for detecting network anomalies", 50,
        """# Network Anomaly Detection

## Unsupervised Learning
Detect unusual patterns without labeled data

## Techniques
```python
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN

# Isolation Forest
iso_forest = IsolationForest(contamination=0.1)
iso_forest.fit(network_data)
anomalies = iso_forest.predict(new_data)

# DBSCAN Clustering
dbscan = DBSCAN(eps=0.3, min_samples=10)
clusters = dbscan.fit_predict(network_data)
# Points with label -1 are outliers
```

## Baseline Creation
1. Collect normal traffic
2. Extract features
3. Build baseline model
4. Monitor deviations

**Applications:** Zero-day detection, insider threats, APTs
""")

    create_lesson(db, ml_net.id, 7, "Protocol Analysis with ML",
        "Apply ML to protocol-specific traffic analysis", 45,
        """# Protocol Analysis with ML

## Protocol-Specific Features
Different protocols have unique attack vectors

## HTTP/HTTPS Analysis
```python
http_features = {
    'method': request.method,
    'path_length': len(request.path),
    'user_agent': request.headers['User-Agent'],
    'status_code': response.status,
    'response_size': len(response.body)
}
```

## DNS Analysis
- Query type distribution
- Response codes
- Query frequency
- Domain entropy

## SMB Analysis
- File access patterns
- Lateral movement indicators
- Unusual shares

**Use Cases:** Web attacks, DNS tunneling, lateral movement detection
""")

    create_lesson(db, ml_net.id, 8, "Adversarial ML in Networks",
        "Understand and defend against adversarial attacks on ML models", 50,
        """# Adversarial ML in Networks

## Threat Model
Attackers can manipulate input to evade ML detection

## Evasion Attacks
```python
# Attacker modifies malicious traffic slightly
original_features = extract_features(malicious_packet)
# Modify to evade classifier
evaded_features = perturb_features(original_features)
```

## Defenses
1. **Adversarial Training** - Train on adversarial examples
2. **Feature Randomization** - Make evasion harder
3. **Ensemble Models** - Harder to fool multiple models
4. **Anomaly Detection** - Catch unusual manipulations

## Model Poisoning
Attacker corrupts training data

**Defense:** Data validation, model monitoring, diverse data sources
""")

    create_lesson(db, ml_net.id, 9, "Real-time Threat Intelligence",
        "Process streaming network data for real-time threat detection", 50,
        """# Real-time Threat Intelligence

## Streaming Data Processing
```python
from kafka import KafkaConsumer

consumer = KafkaConsumer('network-traffic')
for message in consumer:
    packet_data = parse(message.value)
    threat_level = model.predict(packet_data)
    if threat_level == 'high':
        alert_security_team(packet_data)
```

## Online Learning
Update models with new data in real-time
```python
from river import tree

model = tree.HoeffdingTreeClassifier()
for features, label in stream:
    prediction = model.predict_one(features)
    model.learn_one(features, label)
```

## Challenges
- Low latency requirements
- Concept drift
- Resource constraints

**Tools:** Apache Kafka, Apache Flink, River ML
""")

    create_lesson(db, ml_net.id, 10, "Deploying ML Models in Production",
        "Best practices for deploying and maintaining ML models in production", 50,
        """# Deploying ML Models in Production

## Deployment Strategies
1. **Batch Processing** - Periodic analysis
2. **Real-time API** - On-demand predictions
3. **Edge Deployment** - Local processing

## Model Serving
```python
from flask import Flask, request
import joblib

app = Flask(__name__)
model = joblib.load('model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([data['features']])
    return {'prediction': prediction[0]}
```

## Monitoring
- Prediction latency
- Model accuracy over time
- Data drift detection
- Error rates

## Model Updates
1. A/B testing new models
2. Gradual rollout
3. Rollback capability
4. Version control

## Best Practices
- Containerization (Docker)
- CI/CD pipelines
- Logging and alerts
- Regular retraining

**Tools:** MLflow, KubeFlow, TensorFlow Serving
""")

    # Module 6: LLMs for SOC Operations
    print("\n🤖 Module 6: LLMs for SOC Operations")
    
    create_lesson(db, llm_soc.id, 1, "Understanding Large Language Models",
        "Learn LLM fundamentals and their security applications", 40,
        """# Understanding Large Language Models

## What are LLMs?
Large Language Models (GPT-4, Claude, Llama) are neural networks trained on vast text data.

## Capabilities
- Natural language understanding
- Text generation
- Code analysis
- Pattern recognition

## Security Applications
```python
import openai

def analyze_log(log_entry):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a security analyst."},
            {"role": "user", "content": f"Analyze: {log_entry}"}
        ]
    )
    return response.choices[0].message.content
```

## Prompt Engineering
Clear, specific prompts get better results

## Limitations
- Can hallucinate
- No real-time knowledge
- Privacy concerns

**Use responsibly** - Verify LLM outputs, protect sensitive data
""")

    create_lesson(db, llm_soc.id, 2, "LLMs for Log Analysis",
        "Use LLMs to parse and analyze security logs", 50,
        """# LLMs for Log Analysis

## Log Parsing
```python
def parse_log_with_llm(log_text):
    prompt = f"Parse this security log into JSON: {log_text}"
    response = call_llm(prompt)
    return json.loads(response)
```

## Anomaly Detection
Ask LLM to identify unusual patterns in logs

## Alert Summarization
```python
def summarize_alerts(alerts):
    prompt = f"Summarize these {len(alerts)} alerts"
    return call_llm(prompt)
```

## Best Practices
- Batch processing
- Structured outputs
- Validation of results

**Integration:** Splunk, Elastic, Datadog
""")

    create_lesson(db, llm_soc.id, 3, "Automated Incident Triage",
        "Automate alert prioritization and response with LLMs", 45,
        """# Automated Incident Triage

## Alert Prioritization
```python
def prioritize_alert(alert):
    prompt = f"Score severity 1-10: {alert}"
    severity = call_llm(prompt)
    return int(severity)
```

## Context Gathering
LLMs can correlate alerts with threat intelligence

## Response Recommendations
Generate next steps for analysts

## Integration
- SIEM platforms
- Ticketing systems
- Runbooks

**Benefits:** Faster response, consistent triage, reduced analyst fatigue
""")

    create_lesson(db, llm_soc.id, 4, "Threat Intelligence with LLMs",
        "Extract and correlate threat intelligence using LLMs", 50,
        """# Threat Intelligence with LLMs

## IOC Extraction
```python
def extract_iocs(threat_report):
    prompt = "Extract all IPs, domains, and hashes from this report"
    iocs = call_llm(prompt)
    return parse_iocs(iocs)
```

## Report Summarization
Quickly digest long threat reports

## Intelligence Correlation
Connect related threats across sources

**Applications:** Threat feeds, vendor reports, OSINT
""")

    create_lesson(db, llm_soc.id, 5, "Security Query Assistants",
        "Build natural language interfaces for security tools", 45,
        """# Security Query Assistants

## Natural Language to SIEM Queries
```python
def nl_to_siem_query(question):
    prompt = f"Convert to Splunk query: {question}"
    query = call_llm(prompt)
    return execute_splunk_query(query)
```

## Chatbot Interface
Build conversational security assistant

## Benefits
- Easier for non-technical users
- Faster query creation
- Knowledge sharing

**Use Cases:** Junior analysts, executives, auditors
""")

    create_lesson(db, llm_soc.id, 6, "Phishing Detection and Analysis",
        "Use LLMs for advanced phishing detection", 40,
        """# Phishing Detection and Analysis

## Email Analysis
```python
def analyze_email(email_content):
    prompt = "Is this phishing? Analyze urgency, sender, links"
    analysis = call_llm(prompt)
    return analysis
```

## URL Analysis
LLMs can detect suspicious URL patterns

## Social Engineering Detection
Identify manipulation tactics

**Accuracy:** Combine with traditional methods for best results
""")

    create_lesson(db, llm_soc.id, 7, "Vulnerability Analysis and Remediation",
        "Analyze CVEs and generate remediation guidance", 50,
        """# Vulnerability Analysis and Remediation

## CVE Analysis
```python
def analyze_cve(cve_id):
    prompt = f"Explain CVE-{cve_id} and impact"
    return call_llm(prompt)
```

## Patch Recommendations
Generate remediation steps

## Risk Assessment
Prioritize vulnerabilities based on context

**Integration:** Vulnerability scanners, patch management systems
""")

    create_lesson(db, llm_soc.id, 8, "Building a Security Copilot",
        "Create an AI assistant for security operations", 55,
        """# Building a Security Copilot

## RAG (Retrieval Augmented Generation)
Combine LLM with your security knowledge base

```python
def security_copilot(question):
    # 1. Retrieve relevant docs
    docs = vector_search(question)
    # 2. Generate answer with context
    prompt = f"Context: {docs}\\nQuestion: {question}"
    return call_llm(prompt)
```

## Integration Points
- Runbooks
- Past incidents
- Threat intelligence
- Security tools

## Benefits
- 24/7 availability
- Consistent responses
- Knowledge retention

**Future:** Full automation of routine SOC tasks
""")

    # Module 7: AI-Powered Secure Coding
    print("\n💻 Module 7: AI-Powered Secure Coding")
    
    create_lesson(db, ai_code.id, 1, "Secure Coding Principles",
        "Deep dive into OWASP Top 10 and secure development", 40,
        """# Secure Coding Principles

## OWASP Top 10
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration

## SQL Injection Prevention
```python
# ❌ Vulnerable
query = f"SELECT * FROM users WHERE username = '{username}'"

# ✅ Secure
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

## XSS Prevention
```python
from html import escape
output = f"<div>{escape(user_input)}</div>"
```

## Best Practices
- Input validation
- Output encoding
- Least privilege
- Defense in depth

**Resources:** OWASP, CWE Top 25
""")

    create_lesson(db, ai_code.id, 2, "Static Code Analysis with AI",
        "Use AI for automated vulnerability detection", 50,
        """# Static Code Analysis with AI

## AI-Powered SAST
```python
from transformers import pipeline

analyzer = pipeline("code-analysis")
vulnerabilities = analyzer(code)
```

## Pattern Detection
```python
import ast

class VulnerabilityDetector(ast.NodeVisitor):
    def visit_Call(self, node):
        if node.func.id in ['eval', 'exec']:
            self.issues.append(f"Dangerous: {node.func.id}")
```

## Tools
- Semgrep
- CodeQL
- Snyk
- SonarQube

**Integration:** CI/CD pipelines, pre-commit hooks
""")

    create_lesson(db, ai_code.id, 3, "Automated Code Review",
        "Implement AI-assisted code review processes", 45,
        """# Automated Code Review

## AI Code Review
```python
def ai_code_review(pull_request):
    prompt = f"Review for security issues:\\n{pull_request.diff}"
    issues = call_llm(prompt)
    post_comments(pull_request, issues)
```

## Integration
- GitHub/GitLab
- Pull request workflows
- Automated feedback

**Benefits:** Faster reviews, consistent standards, education
""")

    create_lesson(db, ai_code.id, 4, "Vulnerability Prediction",
        "Predict vulnerable code components using ML", 50,
        """# Vulnerability Prediction

## Predictive Models
```python
def predict_vulnerable_files(codebase):
    features = extract_code_metrics(codebase)
    # Complexity, dependencies, change frequency
    predictions = model.predict(features)
    return high_risk_files(predictions)
```

## Code Metrics
- Cyclomatic complexity
- Lines of code
- Number of dependencies
- Change frequency

**Application:** Prioritize security reviews
""")

    create_lesson(db, ai_code.id, 5, "AI-Assisted Penetration Testing",
        "Leverage AI for smarter penetration testing", 55,
        """# AI-Assisted Penetration Testing

## Automated Fuzzing
```python
def ai_fuzzer(api_endpoint):
    # Generate test cases
    test_cases = llm_generate_payloads(api_endpoint)
    for payload in test_cases:
        response = send_request(api_endpoint, payload)
        if is_vulnerable(response):
            report_finding(payload, response)
```

## Intelligent Testing
AI helps generate creative test cases

## Exploit Generation
ML can suggest exploitation techniques

**Ethics:** Only test authorized systems
""")

    create_lesson(db, ai_code.id, 6, "Secure Code Generation with LLMs",
        "Use GitHub Copilot and LLMs securely", 45,
        """# Secure Code Generation with LLMs

## Using GitHub Copilot Safely
```python
# Prompt for secure code
# "Generate a secure password hashing function using bcrypt"

import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)
```

## Validation
Always review and test AI-generated code

## Best Practices
- Specific security prompts
- Code review
- Security testing
- Don't blindly trust

**Remember:** AI assists, humans verify
""")

    create_lesson(db, ai_code.id, 7, "DevSecOps Integration",
        "Integrate AI security tools into CI/CD pipelines", 45,
        """# DevSecOps Integration

## CI/CD Security
```yaml
# .github/workflows/security.yml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: AI Security Scanner
        run: python ai_security_scan.py
      - name: Dependency Check
        run: snyk test
```

## Shift Left
Catch security issues early in development

## Automation
- Static analysis
- Dependency scanning
- Secret detection
- Security testing

## Continuous Monitoring
Monitor deployed applications

**Goal:** Security at the speed of DevOps
""")

    db.commit()
    
    print("\n" + "=" * 60)
    print("✅ TIER 1 COMPLETE!")
    print("   📊 ML for Network Security: 10 lessons")
    print("   📊 LLMs for SOC Operations: 8 lessons")
    print("   📊 AI-Powered Secure Coding: 7 lessons")
    print("   🎯 Total: 25 lessons")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_tier1(db)
    finally:
        db.close()
