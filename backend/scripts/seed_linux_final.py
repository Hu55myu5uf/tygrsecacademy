
import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def seed_linux_lessons_7_to_12(db: Session):
    """Seed final lessons 7-12 for Linux Basics module"""
    print("Seeding Linux Basics lessons 7-12...")
    
    linux_module = db.query(Module).filter(Module.title == "Linux Basics").first()
    
    if not linux_module:
        print("ERROR: Linux Basics module not found!")
        return
    
    existing_count = db.query(Lesson).filter(Lesson.module_id == linux_module.id).count()
    if existing_count >= 12:
        print(f"All 12 lessons already exist. Skipping.")
        return
    
    lessons = [
        {
            "title": "Text Manipulation",
            "description": "Working with text files using cat, grep, sed, awk, and more",
            "duration": 50,
            "content": """
# Text Manipulation

Master the powerful text processing tools that make Linux a sysadmin's dream.

## Viewing Files

```bash
# cat - concatenate and display
cat file.txt

# less - paginated view (q to quit)
less large_file.txt

# head - first 10 lines
head file.txt
head -n 20 file.txt  # First 20 lines

# tail - last 10 lines
tail file.txt
tail -n 50 file.txt  # Last 50 lines
tail -f /var/log/syslog  # Follow live updates
```

## Searching with grep

```bash
# Basic search
grep "error" log.txt

# Case-insensitive
grep -i "ERROR" log.txt

# Show line numbers
grep -n "warning" log.txt

# Recursive search
grep -r "password" /etc/

# Invert match (lines NOT containing)
grep -v "success" log.txt

# Count matches
grep -c "failed" auth.log

# Multiple patterns
grep -E "error|warning|critical" log.txt

# Show context (3 lines before/after)
grep -C 3 "exception" app.log
```

## Stream Editing with sed

```bash
# Replace first occurrence
sed 's/old/new/' file.txt

# Replace all occurrences
sed 's/old/new/g' file.txt

# Replace in-place (edit file)
sed -i 's/old/new/g' file.txt

# Delete lines containing pattern
sed '/pattern/d' file.txt

# Print specific lines
sed -n '10,20p' file.txt  # Lines 10-20

# Multiple operations
sed -e 's/foo/bar/g' -e 's/hello/world/g' file.txt
```

## Advanced Processing with awk

```bash
# Print specific columns
awk '{print $1}' file.txt  # First column
awk '{print $1,$3}' file.txt  # Columns 1 and 3

# With field separator
awk -F: '{print $1}' /etc/passwd  # Usernames

# Pattern matching
awk '/error/ {print $0}' log.txt

# Calculations
awk '{sum+=$1} END {print sum}' numbers.txt

# Conditional
awk '$3 > 100 {print $1,$3}' data.txt
```

## Sorting and Uniqueness

```bash
# sort - sort lines
sort file.txt
sort -r file.txt  # Reverse
sort -n file.txt  # Numeric
sort -u file.txt  # Unique only

# uniq - remove duplicates (requires sorted input)
sort file.txt | uniq
sort file.txt | uniq -c  # Count occurrences
sort file.txt | uniq -d  # Only duplicates
```

## Cutting and Pasting

```bash
# cut - extract columns
cut -d: -f1 /etc/passwd  # Field 1, delimiter :
cut -c1-10 file.txt  # Characters 1-10

# paste - merge files line by line
paste file1.txt file2.txt
paste -d, file1.txt file2.txt  # With comma delimiter
```

## Word and Line Counting

```bash
# wc - word count
wc file.txt  # Lines, words, bytes
wc -l file.txt  # Lines only
wc -w file.txt  # Words only
wc -c file.txt  # Bytes only
```

## Text Transformation

```bash
# tr - translate characters
echo "hello" | tr 'a-z' 'A-Z'  # HELLO
tr -d '0-9' < file.txt  # Delete digits

# rev - reverse lines
echo "hello" | rev  # olleh

# tac - reverse file (opposite of cat)
tac file.txt
```

## Practical Examples

### 1. Extract IPs from Log
```bash
grep -oE '\b[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b' access.log | sort | uniq
```

### 2. Find Top 10 Error Messages
```bash
grep "ERROR" app.log | sort | uniq -c | sort -rn | head -10
```

### 3. Replace in Multiple Files
```bash
find . -name "*.conf" -exec sed -i 's/old_value/new_value/g' {} \;
```

### 4. Extract Email Addresses
```bash
grep -Eo '\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' file.txt
```

### 5. Column Statistics
```bash
awk '{sum+=$3; count++} END {print "Average:", sum/count}' data.txt
```

## Piping Power

```bash
# Chain multiple commands
cat access.log | grep "404" | awk '{print $1}' | sort | uniq -c | sort -rn

# Process CSV
cat data.csv | cut -d, -f2 | sort | uniq | wc -l
```

Text manipulation is essential for log analysis and automation!
            """
        },
        {
            "title": "Process Management",
            "description": "Viewing, managing, and controlling Linux processes",
            "duration": 40,
            "content": """
# Process Management

Learn to monitor and control running processes in Linux.

## Viewing Processes

### ps - Process Status
```bash
# Current user processes
ps

# All processes
ps aux

# Process tree
ps auxf

# Specific user
ps -u username

# By command name
ps aux | grep nginx
```

### top - Live Process Monitor
```bash
# Interactive view
top

# Key commands in top:
# q - quit
# k - kill process
# r - renice (change priority)
# M - sort by memory
# P - sort by CPU
# 1 - show individual CPUs
```

### htop - Better top (if installed)
```bash
sudo apt install htop
htop

# Features:
# - Color coded
# - Mouse support
# - Tree view (F5)
# - Search (F3)
# - Kill (F9)
```

## Process Information

```bash
# Process tree
pstree

# Specific process info
ps aux | grep httpd

# Process by PID
ps -p 1234

# All info about PID
cat /proc/1234/status
```

## Killing Processes

```bash
# Graceful termination
kill 1234

# Force kill
kill -9 1234
kill -SIGKILL 1234

# Kill by name
killall firefox
pkill nginx

# Kill all user processes
killall -u username
```

## Signal Types

| Signal | Number | Description |
|--------|--------|-------------|
| SIGHUP | 1 | Hangup |
| SIGINT | 2 | Interrupt (Ctrl+C) |
| SIGQUIT | 3 | Quit |
| SIGKILL | 9 | Force kill |
| SIGTERM | 15 | Termination (default) |
| SIGCONT | 18 | Continue if stopped |
| SIGSTOP | 19 | Stop process |

## Background Jobs

```bash
# Run in background
command &

# List background jobs
jobs

# Bring to foreground
fg %1

# Send to background
bg %1

# Detach from terminal
nohup command &

# Run even after logout
nohup long_process > output.log 2>&1 &
```

## Process Priority (nice)

```bash
# Check priority (-20 to 19, lower = higher priority)
ps -eo pid,ni,comm

# Run with low priority
nice -n 10 command

# Change priority of running process
renice 5 -p 1234

# Run with high priority (requires sudo)
sudo nice -n -10 command
```

## System Resource Monitoring

```bash
# CPU usage
uptime
mpstat

# Memory usage
free -h

# Disk I/O
iostat

# All in one
vmstat 1  # Update every second
```

## Advanced Tools

### lsof - List Open Files
```bash
# All open files
sudo lsof

# Files by user
sudo lsof -u username

# Files by process
sudo lsof -p 1234

# Network connections
sudo lsof -i
sudo lsof -i :80  # Port 80
```

### fuser - File User
```bash
# Who's using a file
fuser -v /var/log/syslog

# Kill processes using file
fuser -k /path/to/file
```

## Practical Examples

### 1. Find Memory Hog
```bash
ps aux --sort=-%mem | head -10
```

### 2. Find CPU Hog
```bash
ps aux --sort=-%cpu | head -10
```

### 3. Kill Zombie Processes
```bash
ps aux | grep 'Z'
kill -9 $(ps aux | grep 'Z' | awk '{print $2}')
```

### 4. Monitor Specific Process
```bash
watch -n 1 'ps aux | grep nginx'
```

### 5. Resource Limits
```bash
# View limits
ulimit -a

# Set max open files
ulimit -n 4096
```

Understanding processes is crucial for system administration and troubleshooting!
            """
        },
        {
            "title": "Package Management",
            "description": "Installing and managing software with apt, yum, and dnf",
            "duration": 35,
            "content": """
# Package Management

Learn to install, update, and manage software packages in Linux.

## APT (Debian/Ubuntu)

### Basic Operations
```bash
# Update package lists
sudo apt update

# Upgrade all packages
sudo apt upgrade

# Full upgrade (removes old packages)
sudo apt full-upgrade

# Install package
sudo apt install nginx

# Install multiple packages
sudo apt install vim git curl

# Remove package
sudo apt remove nginx

# Remove package and config files
sudo apt purge nginx

# Remove unused dependencies
sudo apt autoremove
```

### Searching and Information
```bash
# Search for package
apt search nginx

# Show package info
apt show nginx

# List installed packages
apt list --installed

# List upgradable packages
apt list --upgradable
```

### Advanced APT
```bash
# Download without installing
apt download package

# Simulate install (dry run)
sudo apt install -s nginx

# Fix broken dependencies
sudo apt --fix-broken install

# Clean package cache
sudo apt clean
sudo apt autoclean
```

## YUM/DNF (RedHat/CentOS/Fedora)

```bash
# Update package database
sudo yum check-update
sudo dnf check-update

# Install package
sudo yum install nginx
sudo dnf install nginx

# Update all packages
sudo yum update
sudo dnf upgrade

# Remove package
sudo yum remove nginx
sudo dnf remove nginx

# Search package
yum search nginx
dnf search nginx

# Package info
yum info nginx
dnf info nginx
```

## Manual Package Installation

### DEB Packages (Debian/Ubuntu)
```bash
# Install .deb file
sudo dpkg -i package.deb

# Fix dependencies after dpkg
sudo apt install -f

# Remove deb package
sudo dpkg -r package-name

# List installed from deb
dpkg -l
```

### RPM Packages (RedHat/Fedora)
```bash
# Install .rpm file
sudo rpm -i package.rpm

# Upgrade rpm
sudo rpm -U package.rpm

# Remove rpm
sudo rpm -e package-name

# Query installed
rpm -qa
```

## Snap Packages
```bash
# Install snap
sudo apt install snapd

# Install snap package
sudo snap install vlc

# List snaps
snap list

# Update snap
sudo snap refresh vlc

# Remove snap
sudo snap remove vlc
```

## Adding Repositories

### Ubuntu PPA
```bash
# Add PPA
sudo add-apt-repository ppa:author/ppa-name
sudo apt update

# Remove PPA
sudo add-apt-repository --remove ppa:author/ppa-name
```

### Manual Repository
```bash
# Edit sources list
sudo vim /etc/apt/sources.list

# Or add to sources.list.d/
sudo vim /etc/apt/sources.list.d/custom.list

# Add GPG key
wget -qO - https://example.com/key.gpg | sudo apt-key add -
```

## Package Verification

```bash
# Check package integrity (Debian)
debsums -c

# Verify RPM
rpm -V package-name

# Check which package owns file
dpkg -S /bin/ls
rpm -qf /bin/ls
```

## Holding Packages

```bash
# Prevent package from upgrading
sudo apt-mark hold package-name

# Remove hold
sudo apt-mark unhold package-name

# List held packages
apt-mark showhold
```

## Practical Examples

### 1. Install Development Tools
```bash
sudo apt install build-essential git vim curl wget
```

### 2. Install LAMP Stack
```bash
sudo apt install apache2 mysql-server php libapache2-mod-php
```

### 3. Clean System
```bash
sudo apt autoremove
sudo apt autoclean
sudo apt clean
```

### 4. Check Package Dependencies
```bash
apt-cache depends nginx
apt-cache rdepends nginx  # Reverse dependencies
```

### 5. Upgrade Specific Package
```bash
sudo apt install --only-upgrade nginx
```

## Security Best Practices

```bash
# Always update before installing
sudo apt update

# Check for security updates
sudo apt list --upgradable | grep security

# Enable automatic security updates
sudo apt install unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades
```

Proper package management keeps your system secure and up-to-date!
            """
        },
        {
            "title": "Networking Basics",
            "description": "IP configuration, connectivity testing, and network troubleshooting",
            "duration": 45,
            "content": """
# Networking Basics

Essential networking commands every Linux user should know.

## Network Configuration

### ip command (modern)
```bash
# Show all interfaces
ip addr
ip a

# Show specific interface
ip addr show eth0

# Show routing table
ip route
ip r

# Add IP address
sudo ip addr add 192.168.1.100/24 dev eth0

# Delete IP address
sudo ip addr del 192.168.1.100/24 dev eth0

# Bring interface up/down
sudo ip link set eth0 up
sudo ip link set eth0 down
```

### ifconfig (legacy, still useful)
```bash
# Show all interfaces
ifconfig

# Show specific interface
ifconfig eth0

# Configure IP
sudo ifconfig eth0 192.168.1.100 netmask 255.255.255.0

# Bring up/down
sudo ifconfig eth0 up
sudo ifconfig eth0 down
```

## Connectivity Testing

### ping - Test Reachability
```bash
# Ping host
ping google.com

# Ping with count
ping -c 4 8.8.8.8

# Ping fast (root only)
sudo ping -i 0.2 192.168.1.1

# Ping with size
ping -s 1000 google.com
```

### traceroute - Trace Route
```bash
# Trace path to host
traceroute google.com

# Use ICMP instead of UDP
sudo traceroute -I google.com

# Show IP addresses only
traceroute -n google.com
```

## DNS Resolution

### nslookup
```bash
# Query DNS
nslookup google.com

# Specify DNS server
nslookup google.com 8.8.8.8

# Reverse lookup
nslookup 8.8.8.8
```

### dig (more detailed)
```bash
# Basic query
dig google.com

# Short answer
dig +short google.com

# Query specific record
dig google.com MX
dig google.com TXT

# Reverse DNS
dig -x 8.8.8.8

# Trace DNS path
dig +trace google.com
```

### host
```bash
# Simple lookup
host google.com

# All records
host -a google.com
```

## Network Statistics

### netstat (legacy)
```bash
# All connections
netstat -a

# TCP connections
netstat -t

# UDP connections
netstat -u

# Listening ports
netstat -l

# Show programs
sudo netstat -tulpn

# Routing table
netstat -r
```

### ss (modern, faster)
```bash
# All sockets
ss -a

# TCP sockets
ss -t

# Listening sockets
ss -l

# Show processes
sudo ss -tulpn

# Specific port
ss -tulpn | grep :80
```

## Port Scanning

```bash
# Check if port is open
nc -zv google.com 80

# Scan range of ports
nc -zv 192.168.1.1 20-100

# nmap (if installed)
sudo apt install nmap
nmap 192.168.1.1
nmap -p 80,443 192.168.1.1
```

## File Transfer

### wget - Download Files
```bash
# Download file
wget https://example.com/file.zip

# Continue interrupted download
wget -c https://example.com/large-file.iso

# Download to specific location
wget -O /path/to/save https://example.com/file.zip

# Download entire website
wget -r -np -k https://example.com
```

### curl - Transfer Data
```bash
# Get webpage
curl https://example.com

# Save to file
curl -o file.html https://example.com

# Follow redirects
curl -L https://example.com

# Show headers
curl -I https://example.com

# POST data
curl -X POST -d "key=value" https://api.example.com
```

### scp - Secure Copy
```bash
# Copy to remote
scp file.txt user@remote:/path/to/destination

# Copy from remote
scp user@remote:/path/to/file.txt local_directory/

# Copy directory
scp -r directory/ user@remote:/path/

# Specify port
scp -P 2222 file.txt user@remote:/path/
```

## Network Monitoring

### tcpdump - Packet Capture
```bash
# Capture all traffic
sudo tcpdump

# Specific interface
sudo tcpdump -i eth0

# Save to file
sudo tcpdump -w capture.pcap

# Read from file
tcpdump -r capture.pcap

# Filter by host
sudo tcpdump host 192.168.1.100

# Filter by port
sudo tcpdump port 80
```

### iftop - Bandwidth Monitor
```bash
sudo apt install iftop
sudo iftop

# Specific interface
sudo iftop -i eth0
```

## Configuration Files

```bash
# Network interfaces
cat /etc/network/interfaces

# DNS servers
cat /etc/resolv.conf

# Hostname
cat /etc/hostname
hostnamectl

# Hosts file
cat /etc/hosts
```

## Practical Examples

### 1. Check Internet Connectivity
```bash
ping -c 3 8.8.8.8 && echo "Network OK" || echo "Network Down"
```

### 2. Find Your IP
```bash
# Private IP
hostname -I
ip addr show | grep "inet " | grep -v 127.0.0.1

# Public IP
curl ifconfig.me
wget -qO- ifconfig.me
```

### 3. Test Port Connectivity
```bash
telnet example.com 80
nc -zv example.com 80
```

### 4. Find Which Process Uses Port
```bash
sudo lsof -i :80
sudo netstat -tulpn | grep :80
```

### 5. Monitor Network in Real-time
```bash
watch -n 1 'ss -tulpn'
```

Network troubleshooting is an essential skill for any sysadmin!
            """
        },
        {
            "title": "Shell Scripting Introduction",
            "description": "Writing bash scripts with variables, loops, and conditionals",
            "duration": 50,
            "content": """
# Shell Scripting Introduction

Automate tasks with bash scripting - one of the most valuable Linux skills.

## Your First Script

```bash
#!/bin/bash
# This is a comment

echo "Hello, World!"
```

Save as `hello.sh`, make executable, and run:
```bash
chmod +x hello.sh
./hello.sh
```

## Variables

```bash
#!/bin/bash

# Define variables (no spaces!)
NAME="John"
AGE=25
PATH_TO_FILE="/home/user/file.txt"

# Use variables
echo "My name is $NAME"
echo "I am ${AGE} years old"

# Command substitution
CURRENT_DATE=$(date)
USER_COUNT=$(who | wc -l)

echo "Today is $CURRENT_DATE"
echo "Users logged in: $USER_COUNT"
```

## User Input

```bash
#!/bin/bash

# Read input
echo "What is your name?"
read NAME

echo "Hello, $NAME!"

# Read with prompt
read -p "Enter your age: " AGE
echo "You are $AGE years old"

# Read password (hidden)
read -sp "Enter password: " PASSWORD
echo
echo "Password received"
```

## Command Line Arguments

```bash
#!/bin/bash

# $0 = script name
# $1, $2, etc = arguments
# $# = number of arguments
# $@ = all arguments

echo "Script name: $0"
echo "First argument: $1"
echo "Second argument: $2"
echo "Number of arguments: $#"
echo "All arguments: $@"
```

Usage: `./script.sh arg1 arg2`

## Conditionals (if-else)

```bash
#!/bin/bash

read -p "Enter a number: " NUM

if [ $NUM -gt 10 ]; then
    echo "Number is greater than 10"
elif [ $NUM -eq 10 ]; then
    echo "Number is exactly 10"
else
    echo "Number is less than 10"
fi
```

### Comparison Operators

**Numeric:**
- `-eq` equal
- `-ne` not equal
- `-gt` greater than
- `-lt` less than
- `-ge` greater or equal
- `-le` less or equal

**String:**
- `=` equal
- `!=` not equal
- `-z` is empty
- `-n` is not empty

**File:**
- `-e` exists
- `-f` is regular file
- `-d` is directory
- `-r` is readable
- `-w` is writable
- `-x` is executable

### Examples

```bash
# Check if file exists
if [ -f "/etc/passwd" ]; then
    echo "File exists"
fi

# Check if directory exists
if [ -d "/home/user" ]; then
    echo "Directory exists"
fi

# String comparison
if [ "$USER" = "root" ]; then
    echo "Running as root"
fi

# Multiple conditions (AND)
if [ -f "file.txt" ] && [ -r "file.txt" ]; then
    echo "File exists and is readable"
fi

# Multiple conditions (OR)
if [ "$USER" = "root" ] || [ "$USER" = "admin" ]; then
    echo "Admin user"
fi
```

## Loops

### For Loop
```bash
#!/bin/bash

# Loop through list
for COLOR in red green blue; do
    echo "Color: $COLOR"
done

# Loop through files
for FILE in *.txt; do
    echo "Processing $FILE"
done

# C-style loop
for ((i=1; i<=5; i++)); do
    echo "Number: $i"
done

# Loop through command output
for USER in $(cat /etc/passwd | cut -d: -f1); do
    echo "User: $USER"
done
```

### While Loop
```bash
#!/bin/bash

COUNT=1
while [ $COUNT -le 5 ]; do
    echo "Count: $COUNT"
    COUNT=$((COUNT + 1))
done

# Read file line by line
while read LINE; do
    echo "Line: $LINE"
done < file.txt
```

### Until Loop
```bash
#!/bin/bash

COUNT=1
until [ $COUNT -gt 5 ]; do
    echo "$COUNT"
    COUNT=$((COUNT + 1))
done
```

## Functions

```bash
#!/bin/bash

# Define function
greet() {
    echo"Hello, $1!"
}

# Call function
greet "Alice"
greet "Bob"

# Function with return value
add() {
    local RESULT=$(($ + $2))
    echo $RESULT
}

SUM=$(add 5 3)
echo "5 + 3 = $SUM"
```

## Case Statement

```bash
#!/bin/bash

read -p "Enter a color (red/green/blue): " COLOR

case $COLOR in
    red)
        echo "You chose red"
        ;;
    green)
        echo "You chose green"
        ;;
    blue)
        echo "You chose blue"
        ;;
    *)
        echo "Unknown color"
        ;;
esac
```

## Practical Scripts

### 1. System Info
```bash
#!/bin/bash

echo "=== System Information ==="
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo "Users: $(who | wc -l)"
echo "Disk Usage:"
df -h /
```

### 2. Backup Script
```bash
#!/bin/bash

SOURCE="/home/user/documents"
DEST="/backup"
DATE=$(date +%Y%m%d)

tar -czf "$DEST/backup-$DATE.tar.gz" "$SOURCE"
echo "Backup completed: backup-$DATE.tar.gz"
```

### 3. User Management
```bash
#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 username"
    exit 1
fi

USERNAME=$1

if id "$USERNAME" &>/dev/null; then
    echo "User $USERNAME exists"
else
    echo "User $USERNAME does not exist"
fi
```

### 4. Log Monitor
```bash
#!/bin/bash

LOG_FILE="/var/log/syslog"
KEYWORD="error"

tail -f "$LOG_FILE" | while read LINE; do
    if echo "$LINE" | grep -q "$KEYWORD"; then
        echo "ALERT: $LINE"
    fi
done
```

## Best Practices

1. **Use shellcheck**
```bash
sudo apt install shellcheck
shellcheck script.sh
```

2. **Always quote variables**
```bash
# Bad
if [ $VAR = "value" ]

# Good
if [ "$VAR" = "value" ]
```

3. **Set error handling**
```bash
#!/bin/bash
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure
```

4. **Add help message**
```bash
if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <argument>"
    exit 1
fi
```

Shell scripting is the key to Linux automation mastery!
            """
        },
        {
            "title": "Linux for Security",
            "description": "Security tools, logs, user management, and system hardening",
            "duration": 55,
            "content": """
# Linux for Security

Essential security practices and tools for protecting your Linux system.

## User Management

### Creating Users
```bash
# Add user
sudo useradd -m -s /bin/bash alice

# Set password
sudo passwd alice

# Add user with home directory
sudo adduser bob  # Interactive

# Add to sudo group
sudo usermod -aG sudo alice
```

### Managing Users
```bash
# List all users
cat /etc/passwd

# List logged in users
who
w

# Check user groups
groups alice
id alice

# Delete user
sudo userdel alice

# Delete user and home
sudo userdel -r alice

# Lock user account
sudo usermod -L alice

# Unlock user account
sudo usermod -U alice
```

### Group Management
```bash
# Create group
sudo groupadd developers

# Add user to group
sudo usermod -aG developers alice

# Remove user from group
sudo gpasswd -d alice developers

# Delete group
sudo groupdel developers
```

## System Logs

### Important Log Files
```bash
# Authentication logs
/var/log/auth.log      # Debian/Ubuntu
/var/log/secure        # RedHat/CentOS

# System logs
/var/log/syslog        # Debian/Ubuntu
/var/log/messages      # RedHat

# Kernel logs
/var/log/kern.log
dmesg

# Application logs
/var/log/apache2/      # Web server
/var/log/mysql/        # Database
```

### Viewing Logs
```bash
# View auth log
sudo cat /var/log/auth.log

# Follow live updates
sudo tail -f /var/log/syslog

# Search for failed logins
sudo grep "Failed password" /var/log/auth.log

# Show sudo commands
sudo grep sudo /var/log/auth.log

# journalctl (systemd)
sudo journalctl
sudo journalctl -u nginx  # Specific service
sudo journalctl -f        # Follow
sudo journalctl --since "1 hour ago"
```

## Firewall (UFW)

```bash
# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose

# Allow port
sudo ufw allow 22
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Allow specific IP
sudo ufw allow from 192.168.1.100

# Allow subnet
sudo ufw allow from 192.168.1.0/24

# Deny port
sudo ufw deny 23

# Delete rule
sudo ufw delete allow 80

# Reset firewall
sudo ufw reset

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

## SSH Security

### Secure SSH Configuration
```bash
# Edit SSH config
sudo vim /etc/ssh/sshd_config

# Recommended settings:
Port 2222                    # Change default port
PermitRootLogin no           # Disable root login
PasswordAuthentication no    # Use keys only
PubkeyAuthentication yes     # Enable key auth
AllowUsers alice bob         # Whitelist users
MaxAuthTries 3               # Limit attempts

# Restart SSH
sudo systemctl restart sshd
```

### SSH Key Setup
```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Copy to server
ssh-copy-id user@server

# Or manually
cat ~/.ssh/id_ed25519.pub | ssh user@server "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Set correct permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/authorized_keys
```

## Security Auditing

### Find SUID Files
```bash
# Find all SUID binaries
sudo find / -perm -4000 -type f 2>/dev/null

# Find SGID files
sudo find / -perm -2000 -type f 2>/dev/null
```

### Check for Rootkits
```bash
# Install rkhunter
sudo apt install rkhunter

# Update and scan
sudo rkhunter --update
sudo rkhunter --check
```

### Check Open Ports
```bash
# Using netstat
sudo netstat -tulpn

# Using ss
sudo ss -tulpn

# Using nmap
sudo nmap localhost
```

## Automated Security Updates

```bash
# Install unattended-upgrades
sudo apt install unattended-upgrades

# Configure
sudo dpkg-reconfigure unattended-upgrades

# Edit configuration
sudo vim /etc/apt/apt.conf.d/50unattended-upgrades
```

## Fail2Ban - Intrusion Prevention

```bash
# Install
sudo apt install fail2ban

# Start service
sudo systemctl start fail2ban
sudo systemctl enable fail2ban

# Check status
sudo fail2ban-client status

# Check SSH jail
sudo fail2ban-client status sshd

# Unban IP
sudo fail2ban-client set sshd unbanip 192.168.1.100
```

### Basic Configuration
```bash
# Create local config
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo vim /etc/fail2ban/jail.local

# Example SSH protection:
[sshd]
enabled = true
port = 22
filter = sshd
logpath = /var/log/auth.log
maxretry = 3
bantime = 3600
```

## System Hardening Checklist

### 1. Keep System Updated
```bash
sudo apt update && sudo apt upgrade
```

### 2. Minimal Installed Software
```bash
# List installed packages
dpkg -l

# Remove unnecessary
sudo apt remove package-name
sudo apt autoremove
```

### 3. Disable Unused Services
```bash
# List services
systemctl list-units --type=service

# Disable service
sudo systemctl disable service-name
sudo systemctl stop service-name
```

### 4. Configure File Permissions
```bash
# Secure home directories
sudo chmod 750 /home/*

# Secure important files
sudo chmod 644 /etc/passwd
sudo chmod 600 /etc/shadow
sudo chmod 600 /boot/grub/grub.cfg
```

### 5. Enable AppArmor/SELinux
```bash
# AppArmor status (Ubuntu)
sudo apparmor_status

# SELinux status (RedHat)
sestatus
```

## Security Monitoring

### Check Last Logins
```bash
# Last successful logins
last

# Last failed logins
sudo lastb

# Current users
w
who
```

### Monitor System Calls
```bash
# Install auditd
sudo apt install auditd

# View audit logs
sudo ausearch -m LOGIN

#Check file access
sudo auditctl -w /etc/passwd -p wa -k passwd_changes
```

### System Integrity
```bash
# Install AIDE
sudo apt install aide

# Initialize database
sudo aideinit

# Check for changes
sudo aide --check
```

## Practical Security Scripts

### 1. Failed Login Monitor
```bash
#!/bin/bash
grep "Failed password" /var/log/auth.log | tail -20
```

### 2. Check Suspicious Users
```bash
#!/bin/bash
awk -F: '$3 >= 1000 {print $1}' /etc/passwd
```

### 3. Port Scan Detection
```bash
#!/bin/bash
sudo netstat -antp | grep SYN_RECV | wc -l
```

### 4. Disk Usage Alert
```bash
#!/bin/bash
THRESHOLD=80
USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ $USAGE -gt $THRESHOLD ]; then
    echo "Disk usage critical: ${USAGE}%"
fi
```

**Security is not a product, it's a process!**

---

## Congratulations! 🎉

You've completed the Linux Basics module! You now have the foundational skills needed for:
- System administration
- Security analysis
- Automation and scripting
- Network troubleshooting

**Next Steps:**
- Practice regularly in a virtual lab
- Set up your own Linux server
- Explore security tools like Kali Linux
- Move on to Networking Fundamentals module

Keep learning, keep securing! 🐧🔒
            """
        }
    ]
    
    # Create lessons 7-12
    for index, lesson_data in enumerate(lessons, start=7):
        lesson = Lesson(
            module_id=linux_module.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            order=index,
            duration_minutes=lesson_data["duration"],
            content_markdown=lesson_data["content"].strip(),
            is_published=True
        )
        db.add(lesson)
    
    db.commit()
    print(f"✅ Created lessons 7-12 for Linux Basics module")
    print(f"🎉 Linux Basics module is now complete with all 12 lessons!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_linux_lessons_7_to_12(db)
    finally:
        db.close()
