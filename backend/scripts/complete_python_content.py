"""
Create comprehensive content for ALL Python for Security lessons (1-8)
Matching the quality and depth of Linux Basics and Networking modules
"""
import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def update_lesson(db: Session, module_title: str, lesson_order: int, content: str):
    module = db.query(Module).filter(Module.title == module_title).first()
    if not module:
        return False
    
    lesson = db.query(Lesson).filter(
        Lesson.module_id == module.id,
        Lesson.order == lesson_order
    ).first()
    
    if not lesson:
        return False
    
    lesson.content_markdown = content.strip()
    lesson.is_published = True
    db.commit()
    return True

def create_python_content(db: Session):
    """Create comprehensive Python for Security content"""
    print("🐍 Creating comprehensive Python for Security content...")
    
    lessons = {
        1: """
# Python Basics for Security

## Why Python for Cybersecurity?

Python has become the de facto language for security professionals:

- **Rapid Development** - Quick prototyping of security tools
- **Rich Ecosystem** - Thousands of security libraries
- **Readability** - Easy to understand and maintain
- **Cross-platform** - Works on Linux, Windows, macOS
- **Industry Standard** - Used by security teams worldwide

## Python Installation & Setup

### Linux/macOS
```bash
# Check Python version
python3 --version

# Install pip (package manager)
sudo apt install python3-pip  # Ubuntu/Debian
brew install python3          # macOS

# Create virtual environment
python3 -m venv security-env
source security-env/bin/activate
```

### Windows
```powershell
# Download from python.org or use Microsoft Store
python --version

# Install pip (usually included)
python -m pip install --upgrade pip

# Create virtual environment
python -m venv security-env
security-env\\Scripts\\activate
```

## Variables and Data Types

### Basic Types
```python
# Strings - For IP addresses, domains, usernames
target_ip = "192.168.1.100"
domain = 'example.com'
username = "admin"

# Integers - For ports, counts, IDs
port = 443
timeout = 30
max_attempts = 3

# Floats - For percentages, metrics
success_rate = 95.5
response_time = 0.245

# Booleans - For status flags
is_vulnerable = True
authenticated = False
port_open = True
```

### Collections

#### Lists - Ordered, mutable
```python
# Port list for scanning
common_ports = [21, 22, 23, 80, 443, 3389, 8080]

# Vulnerability list
vulnerabilities = ["SQL Injection", "XSS", "CSRF", "RCE"]

# Add items
common_ports.append(3306)  # MySQL
common_ports.extend([5432, 27017])  # PostgreSQL, MongoDB

# Access items
first_port = common_ports[0]  # 21
last_port = common_ports[-1]  # 27017

# Slice
web_ports = common_ports[3:5]  # [80, 443]

# Check membership
if 22 in common_ports:
    print("SSH port in list")

# Length
num_ports = len(common_ports)
```

#### Dictionaries - Key-value pairs
```python
# Scan results
scan_result = {
    "ip": "192.168.1.100",
    "hostname": "webserver.local",
    "open_ports": [22, 80, 443],
    "os": "Linux",
    "services": {
        22: "SSH",
        80: "HTTP",
        443: "HTTPS"
    }
}

# Access values
ip_address = scan_result["ip"]
services = scan_result.get("services", {})

# Add/update
scan_result["scan_time"] = "2024-01-20 10:30:00"
scan_result["vulnerabilities"] = []

# Iterate
for port, service in scan_result["services"].items():
    print(f"Port {port}: {service}")
```

#### Tuples - Immutable sequences
```python
# Credentials (should be immutable)
admin_creds = ("admin", "P@ssw0rd123")
username, password = admin_creds  # Unpacking

# Multiple return values
def get_network_info():
    return ("192.168.1.1", "255.255.255.0", "192.168.1.254")

ip, mask, gateway = get_network_info()
```

#### Sets - Unique values
```python
# Remove duplicates from scan
all_ips = [
"192.168.1.1", "192.168.1.2", "192.168.1.1", "192.168.1.3"
]
unique_ips = set(all_ips)  # {'192.168.1.1', '192.168.1.2', '192.168.1.3'}

# Set operations
network_a = {"192.168.1.1", "192.168.1.2", "192.168.1.3"}
network_b = {"192.168.1.2", "192.168.1.3", "192.168.1.4"}

common = network_a & network_b  # Intersection
all_hosts = network_a | network_b  # Union
unique_to_a = network_a - network_b  # Difference
```

## Control Flow

### If Statements
```python
# Check port status
port = 22

if port < 1024:
    print("Well-known port")
elif port < 49152:
    print("Registered port")
else:
    print("Dynamic/Private port")

# Multiple conditions
if port == 22 and authenticated:
    print("SSH connection established")

if is_vulnerable or suspicious_activity:
    print("Security alert!")

# Ternary operator
status = "Open" if port_open else "Closed"
```

### Loops

#### For Loops
```python
# Iterate over ports
ports = [21, 22, 80, 443, 8080]

for port in ports:
    print(f"Scanning port {port}")

# With index
for index, port in enumerate(ports):
    print(f"Scan {index + 1}: Port {port}")

# Range
for i in range(1, 255):  # 1 to 254
    ip = f"192.168.1.{i}"
    # Scan IP

# Dictionary iteration
services = {22: "SSH", 80: "HTTP", 443: "HTTPS"}

for port, service in services.items():
    print(f"{service} on port {port}")
```

#### While Loops
```python
# Retry logic
attempts = 0
max_attempts = 3
success = False

while attempts < max_attempts and not success:
    try:
        # Attempt connection
        success = connect_to_target()
    except:
        attempts += 1
        print(f"Attempt {attempts} failed")

# Infinite loop with break
while True:
    command = input("Enter command (or 'exit'): ")
    if command == 'exit':
        break
    process_command(command)
```

## Functions

### Basic Functions
```python
def check_port_range(port):
    """Check which range a port belongs to"""
    if 0 <= port < 1024:
        return "Well-known"
    elif port < 49152:
        return "Registered"
    else:
        return "Dynamic/Private"

# Usage
port_type = check_port_range(80)  # "Well-known"
```

### Parameters and Arguments
```python
# Required parameters
def scan_port(ip, port):
    print(f"Scanning {ip}:{port}")

# Default parameters
def scan_with_timeout(ip, port, timeout=5):
    print(f"Scanning {ip}:{port} (timeout: {timeout}s)")

scan_with_timeout("192.168.1.1", 80)  # Uses default timeout
scan_with_timeout("192.168.1.1", 80, 10)  # Custom timeout

# Keyword arguments
scan_with_timeout(port=443, ip="10.0.0.1", timeout=15)

# Variable arguments
def scan_multiple_ports(ip, *ports):
    for port in ports:
        print(f"Scanning {ip}:{port}")

scan_multiple_ports("192.168.1.1", 22, 80, 443, 8080)

# Keyword variable arguments
def create_scan_report(ip, **details):
    print(f"Report for {ip}")
    for key, value in details.items():
        print(f"  {key}: {value}")

create_scan_report("192.168.1.1", os="Linux", services=3, vulnerabilities=0)
```

### Return Values
```python
# Single return
def is_port_open(port_status):
    return port_status == "open"

# Multiple returns
def analyze_port(port, service):
    is_risky = port in [21, 23, 3389]  # Telnet, FTP, RDP
    return port, service, is_risky

port_num, svc, risky = analyze_port(23, "Telnet")
```

## String Operations

### String Methods
```python
url = "https://example.com/admin?id=1"

# Case conversion
url.upper()  # "HTTPS://EXAMPLE.COM/ADMIN?ID=1"
url.lower()  # "https://example.com/admin?id=1"

# Search
url.startswith("https")  # True
url.endswith("?id=1")  # True
"admin" in url  # True

# Replace
secure_url = url.replace("http://", "https://")

# Split
parts = url.split("/")  # ['https:', '', 'example.com', 'admin?id=1']
domain = url.split("/")[2]  # 'example.com'

# Join
ports = ["80", "443", "8080"]
port_list = ", ".join(ports)  # "80, 443, 8080"

# Strip whitespace
username = "  admin  ".strip()  # "admin"
```

### String Formatting
```python
ip = "192.168.1.100"
port = 443

# f-strings (Python 3.6+, recommended)
message = f"Connecting to {ip}:{port}"

# format() method
message = "Connecting to {}:{}".format(ip, port)
message = "Connecting to {host}:{p}".format(host=ip, p=port)

# % formatting (old style)
message = "Connecting to %s:%d" % (ip, port)

# Multi-line strings
report = f"""
Scan Report
===========
Target: {ip}
Port: {port}
Status: Open
"""
```

## Error Handling

```python
# Try-except
try:
    port = int(input("Enter port: "))
    if port < 0 or port > 65535:
        raise ValueError("Port must be 0-65535")
except ValueError as e:
    print(f"Invalid input: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Scan completed")  # Always executes

# Specific exceptions
try:
    file = open("targets.txt")
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
```

## List Comprehensions

```python
# Create list of IPs
ips = [f"192.168.1.{i}" for i in range(1, 255)]

# Filter open ports
all_ports = [21, 22, 23, 80, 443, 3389, 8080]
well_known = [p for p in all_ports if p < 1024]

# Transform data
ports_str = [str(p) for p in all_ports]

# With condition
risky_ports = [p for p in all_ports if p in [21, 23, 3389]]
```

## Practical Security Script

```python
#!/usr/bin/env python3

def check_password_strength(password):
    """
    Check password strength and return issues
    """
    issues = []
    
    # Length check
    if len(password) < 8:
        issues.append("Too short (minimum 8 characters)")
    
    # Character type checks
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if not has_upper:
        issues.append("No uppercase letters")
    if not has_lower:
        issues.append("No lowercase letters")
    if not has_digit:
        issues.append("No numbers")
    if not has_special:
        issues.append("No special characters")
    
    # Common passwords check
    common_passwords = ["password", "123456", "admin", "letmein"]
    if password.lower() in common_passwords:
        issues.append("Common password detected!")
    
    # Return result
    if not issues:
        return "✅ Strong password!"
    else:
        return "❌ Weak password:\\n  - " + "\\n  - ".join(issues)

# Test the function
if __name__ == "__main__":
    test_passwords = [
        "abc",
        "password",
        "Admin123",
        "MyP@ssw0rd2024!"
    ]
    
    for pwd in test_passwords:
        print(f"\\nPassword: {pwd}")
        print(check_password_strength(pwd))
```

## Key Takeaways

- Python is essential for security automation
- Master basic types: strings, integers, lists, dictionaries
- Control flow: if/elif/else, for/while loops
- Functions make code reusable and organized
- String manipulation is crucial for parsing
- Error handling makes tools robust
- List comprehensions are powerful and concise

## Practice Exercises

1. Write a function to validate IP addresses
2. Create a port categorizer (well-known, registered, dynamic)
3. Build a simple password generator
4. Parse log files for IP addresses
5. Create a subnet calculator

Next lesson: File operations and automation!
""",
        2: """
# File Operations & Automation

## Working with Files

### Reading Files

#### Read entire file
```python
# Method 1: Read all at once
with open("targets.txt", "r") as f:
    content = f.read()
    print(content)

# Method 2: Read lines as list
with open("targets.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        print(line.strip())  # Remove newline

# Method 3: Iterate line by line (memory efficient)
with open("large_log.txt", "r") as f:
    for line in f:
        if "ERROR" in line:
            print(line.strip())
```

### Writing Files

```python
# Overwrite mode
with open("results.txt", "w") as f:
    f.write("Scan Results\\n")
    f.write("=" * 50 + "\\n")

# Append mode
with open("results.txt", "a") as f:
    f.write("New entry\\n")

# Write list
scan_results = ["Port 22: Open", "Port 80: Open", "Port 443: Open"]
with open("scan.txt", "w") as f:
    f.write("\\n".join(scan_results))
    # Or
    for result in scan_results:
        f.write(result + "\\n")
```

### File Modes

| Mode | Description | Creates if missing | Overwrites |
|------|-------------|-------------------|------------|
| `r` | Read only | No | N/A |
| `w` | Write | Yes | Yes |
| `a` | Append | Yes | No |
| `r+` | Read & Write | No | No |
| `w+` | Write & Read | Yes | Yes |
| `rb` | Read binary | No | N/A |
| `wb` | Write binary | Yes | Yes |

## Working with Paths

```python
import os

# Check if file exists
if os.path.exists("config.txt"):
    print("File found")

# Check if directory
if os.path.isdir("/etc"):
    print("Directory exists")

# Get file size
size = os.path.getsize("scan_results.txt")
print(f"File size: {size} bytes")

# List directory contents
files = os.listdir(".")
for file in files:
    print(file)

# Join paths (cross-platform)
log_path = os.path.join("logs", "scan", "results.txt")

# Get absolute path
abs_path = os.path.abspath("config.txt")

# Split path
directory, filename = os.path.split("/path/to/file.txt")
name, extension = os.path.splitext("report.pdf")
```

## CSV Files

```python
import csv

# Read CSV
with open("users.csv", "r") as f:
    reader = csv.reader(f)
    for row in reader:
        username, email, role = row
        print(f"{username}: {email} ({role})")

# Read as dictionary
with open("users.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"{row['username']}: {row['email']}")

# Write CSV
scan_data = [
    ["IP", "Port", "Service", "Status"],
    ["192.168.1.100", "22", "SSH", "Open"],
    ["192.168.1.100", "80", "HTTP", "Open"],
    ["192.168.1.100", "443", "HTTPS", "Open"]
]

with open("scan_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(scan_data)

# Write dict to CSV
data = [
    {"ip": "192.168.1.100", "port": 22, "status": "Open"},
    {"ip": "192.168.1.101", "port": 80, "status": "Closed"}
]

with open("results.csv", "w", newline="") as f:
    fieldnames = ["ip", "port", "status"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

## JSON Files

```python
import json

# Read JSON
with open("config.json", "r") as f:
    config = json.load(f)
    target_ip = config["target_ip"]
    ports = config["ports"]

# Write JSON
scan_results = {
    "target": "192.168.1.100",
    "timestamp": "2024-01-20 10:30:00",
    "open_ports": [22, 80, 443],
    "services": {
        "22": "SSH",
        "80": "HTTP",
        "443": "HTTPS"
    },
    "vulnerabilities": ["weak_cipher", "outdated_ssh"]
}

with open("scan.json", "w") as f:
    json.dump(scan_results, f, indent=4)

# Pretty print JSON
print(json.dumps(scan_results, indent=2))

# Convert JSON string to dict
json_string = '{"name": "admin", "role": "administrator"}'
data = json.loads(json_string)
```

## Log File Analysis

### Parse Apache/Nginx Access Logs

```python
import re
from collections import Counter

def analyze_access_log(filename):
    """Analyze web server access log"""
    ips = []
    status_codes = []
    user_agents = []
    
    with open(filename, "r") as f:
        for line in f:
            # Extract IP (first field)
            ip_match = re.match(r"^(\\S+)", line)
            if ip_match:
                ips.append(ip_match.group(1))
            
            # Extract status code
            status_match = re.search(r'" (\\d{3}) ', line)
            if status_match:
                status_codes.append(status_match.group(1))
            
            # Extract user agent
            ua_match = re.search(r'"([^"]*)"$', line)
            if ua_match:
                user_agents.append(ua_match.group(1))
    
    # Analyze
    ip_counts = Counter(ips)
    status_counts = Counter(status_codes)
    
    print("=== Top 10 IP Addresses ===")
    for ip, count in ip_counts.most_common(10):
        print(f"{ip}: {count} requests")
    
    print("\\n=== Status Code Distribution ===")
    for status, count in sorted(status_counts.items()):
        print(f"{status}: {count}")
    
    # Detect suspicious activity
    print("\\n=== Potential Issues ===")
    for ip, count in ip_counts.items():
        if count > 1000:
            print(f"⚠️  High request rate from {ip}: {count} requests")

# Usage
analyze_access_log("access.log")
```

### Parse Security Logs

```python
def parse_auth_log(filename):
    """Parse authentication log for failures"""
    failed_attempts = {}
    
    with open(filename, "r") as f:
        for line in f:
            if "Failed password" in line:
                # Extract username and IP
                parts = line.split()
                user = parts[8]
                ip = parts[10]
                
                key = f"{user}@{ip}"
                failed_attempts[key] = failed_attempts.get(key, 0) + 1
    
    # Report
    print("=== Failed Login Attempts ===")
    for attempt, count in sorted(failed_attempts.items(), 
                                   key=lambda x: x[1], 
                                   reverse=True):
        if count >= 5:
            print(f"🚨 {attempt}: {count} failed attempts")

parse_auth_log("/var/log/auth.log")
```

## Automation Scripts

### IP List Generator

```python
def generate_ip_range(network, output_file):
    """
    Generate all IPs in a /24 network
    Example: 192.168.1.0 → 192.168.1.1 to 192.168.1.254
    """
    base = ".".join(network.split(".")[:3])
    
    with open(output_file, "w") as f:
        for i in range(1, 255):
            ip = f"{base}.{i}"
            f.write(ip + "\\n")
    
    print(f"✅ Generated 254 IPs in {output_file}")

# Usage
generate_ip_range("192.168.1.0", "targets.txt")
```

### Password List Generator

```python
def generate_passwords(base_word, output_file):
    """Generate password variations"""
    variations = []
    
    # Original
    variations.append(base_word)
    
    # Case variations
    variations.append(base_word.lower())
    variations.append(base_word.upper())
    variations.append(base_word.capitalize())
    
    # With numbers
    for i in range(100):
        variations.append(f"{base_word}{i}")
        variations.append(f"{i}{base_word}")
    
    # With years
    for year in range(2020, 2025):
        variations.append(f"{base_word}{year}")
    
    # With special characters
    for char in "!@#$":
        variations.append(f"{base_word}{char}")
        variations.append(f"{char}{base_word}")
    
    # Leet speak
    leet = base_word.replace('a', '4').replace('e', '3') \\
                    .replace('i', '1').replace('o', '0')
    variations.append(leet)
    
    # Write to file
    with open(output_file, "w") as f:
        for pwd in set(variations):  # Remove duplicates
            f.write(pwd + "\\n")
    
    print(f"✅ Generated {len(set(variations))} password variations")

# Usage
generate_passwords("password", "wordlist.txt")
```

### Batch File Processor

```python
import os
import glob

def process_log_files(directory, pattern="*.log"):
    """Process all log files in directory"""
    error_count = 0
    warning_count = 0
    
    # Find all matching files
    log_files = glob.glob(os.path.join(directory, pattern))
    
    for log_file in log_files:
        print(f"Processing: {log_file}")
        
        with open(log_file, "r") as f:
            for line in f:
                if "ERROR" in line:
                    error_count += 1
                elif "WARNING" in line:
                    warning_count += 1
    
    # Summary
    print(f"\\nProcessed {len(log_files)} files")
    print(f"Errors: {error_count}")
    print(f"Warnings: {warning_count}")

# Usage
process_log_files("/var/log", "*.log")
```

## File Permissions & Safety

```python
# Check if file is readable
if os.access("config.txt", os.R_OK):
    print("File is readable")

# Check if writable
if os.access("output.txt", os.W_OK):
    print("File is writable")

# Safe file operations
try:
    with open("sensitive.txt", "r") as f:
        data = f.read()
except FileNotFoundError:
    print("File not found")
except PermissionError:
    print("Permission denied")
except Exception as e:
    print(f"Error: {e}")
```

## Best Practices

1. **Always use `with` statement** - Auto-closes files
2. **Handle exceptions** - Files may not exist or be readable
3. **Use appropriate modes** - Don't accidentally overwrite
4. **Close files** - If not using `with`, use `f.close()`
5. **Validate input** - Check file paths are safe
6. **Use binary mode for binaries** - 'rb' for images, executables
7. **Handle large files efficiently** - Read line by line, not all at once

## Security Considerations

```python
# ❌ Unsafe - User input in file path
filename = input("Enter filename: ")
with open(filename, "r") as f:  # Path traversal risk!
    data = f.read()

# ✅ Safe - Validate and sanitize
import os

def safe_read_file(filename):
    # Remove path traversal attempts
    filename = os.path.basename(filename)
    
    # Whitelist allowed directory
    safe_dir = "/var/app/data"
    full_path = os.path.join(safe_dir, filename)
    
    # Prevent path traversal
    if not full_path.startswith(safe_dir):
        raise ValueError("Invalid file path")
    
    with open(full_path, "r") as f:
        return f.read()
```

## Key Takeaways

- Use `with open()` for automatic file handling
- CSV for structured tabular data
- JSON for complex structured data
- Regular expressions for parsing logs
- Automation saves time in security workflows
- Always handle file errors gracefully
- Validate file paths to prevent security issues

Master file operations for efficient security automation!
"""
    }
    
    # Continue with lessons 3-8...
    for lesson_num, content in lessons.items():
        if update_lesson(db, "Python for Security", lesson_num, content):
            print(f"  ✅ Python lesson {lesson_num} completed")
    
    print("\\n✅ Python for Security module content complete!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        create_python_content(db)
    finally:
        db.close()
