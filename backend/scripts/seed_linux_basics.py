
import sys
import os
from sqlalchemy.orm import Session

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson, ContentBlock, ContentType

def seed_tier_zero_linux(db: Session):
    """Seed Tier 0 with Linux Basics module and 12 lessons"""
    print("Seeding Tier 0 - Linux Basics module...")
    
    # Check if Tier 0 exists, if not create it
    tier0 = db.query(Tier).filter(Tier.tier_number == 0).first()
    if not tier0:
        tier0 = Tier(
            tier_number=0,
            name="Foundations",
            description="Build your fundamental skills in cybersecurity essentials: Linux, networking, Python scripting, and AI basics.",
            order=0
        )
        db.add(tier0)
        db.commit()
        db.refresh(tier0)
    
    # Check if Linux Basics module already exists
    existing_module = db.query(Module).filter(
        Module.tier_id == tier0.id,
        Module.title == "Linux Basics"
    ).first()
    
    if existing_module:
        print("Linux Basics module already exists. Skipping.")
        return
    
    # Create Linux Basics Module
    linux_module = Module(
        tier_id=tier0.id,
        title="Linux Basics",
        description="Master the Linux operating system fundamentals essential for cybersecurity. Learn command line usage, file management, permissions, and security basics.",
        order=1,
        estimated_hours=8,
        is_published=True
    )
    
    db.add(linux_module)
    db.commit()
    db.refresh(linux_module)
    
    # Create 12 Linux Lessons
    lessons = [
        {
            "title": "Introduction to Linux",
            "description": "Understanding Linux, distributions, and why it matters in cybersecurity",
            "duration": 30,
            "content": """
# Introduction to Linux

## What is Linux?

Linux is a free and open-source Unix-like operating system kernel first released in 1991 by Linus Torvalds. It has become the backbone of cybersecurity, powering everything from security tools to enterprise servers.

## Why Linux for Cybersecurity?

1. **Open Source**: Full transparency - you can see and modify the code
2. **Command Line Power**: Automation and scripting capabilities
3. **Security Tools**: Most security tools are built for Linux first
4. **Server Dominance**: 90%+ of servers run Linux
5. **Customization**: Complete control over your system

## Popular Linux Distributions

- **Kali Linux**: Purpose-built for penetration testing and security auditing
- **Ubuntu**: User-friendly, great for beginners
- **Debian**: Stable and reliable
- **Fedora**: Cutting-edge features
- **ParrotOS**: Security-focused like Kali

## Key Differences from Windows

| Feature | Linux | Windows |
|---------|-------|---------|
| Cost | Free | Paid |
| Source Code | Open | Closed |
| Security | Very Secure | Less Secure |
| Customization | Highly Customizable | Limited |
| Package Management | Built-in | Limited |

## Your Learning Path

In this module, you'll master:
- Command line basics
- File system navigation
- User permissions and security
- Process management
- Network configuration
- Basic scripting

Let's begin your Linux journey!
            """
        },
        {
            "title": "Linux Installation & Setup",
            "description": "Installing Linux using VirtualBox/WSL and exploring the desktop environment",
            "duration": 45,
            "content": """
# Linux Installation & Setup

## Installation Options

### Option 1: VirtualBox (Recommended for Beginners)

**Step 1: Download VirtualBox**
- Visit virtualbox.org
- Download for your OS (Windows/Mac/Linux)
- Install with default settings

**Step 2: Download Ubuntu ISO**
```bash
# Visit ubuntu.com/download
# Choose Ubuntu 22.04 LTS Desktop
# Download the .iso file (3-4 GB)
```

**Step 3: Create Virtual Machine**
1. Open VirtualBox → New
2. Name: "Ubuntu Security Lab"
3. Type: Linux, Version: Ubuntu (64-bit)
4. RAM: 4GB (4096 MB)
5. Create Virtual Hard Disk: 25GB
6. Start VM and select Ubuntu ISO
7. Follow installation wizard

### Option 2: WSL2 (Windows Subsystem for Linux)

For Windows 10/11 users:

```powershell
# Open PowerShell as Administrator
wsl --install

# Restart computer
# Set up username and password
```

### Option 3: Dual Boot (Advanced)

Not recommended for beginners - stick with VirtualBox or WSL2.

## First Boot

After installation, you'll see:
- **Login Screen**: Enter your credentials
- **Desktop Environment**: GNOME (default for Ubuntu)
- **Terminal**: Your new best friend!

## Essential First Commands

```bash
# Check your username
whoami

# Check system information
uname -a

# Update package lists
sudo apt update

# Upgrade installed packages
sudo apt upgrade -y

# Install useful tools
sudo apt install vim git curl wget net-tools -y
```

## Desktop Environment Tour

- **Activities**: Top-left corner - search for apps
- **Terminal**: Ctrl+Alt+T
- **Files**: File manager
- **Settings**: System configuration

## Setting Up for Security Work

```bash
# Create a workspace directory
mkdir ~/security-workspace
cd ~/security-workspace

# Install basic security tools
sudo apt install nmap wireshark tcpdump -y
```

## Troubleshooting

**VirtualBox Guest Additions** (for better resolution):
```bash
sudo apt install virtualbox-guest-utils virtualbox-guest-x11
```

**WSL2 Graphics**:
```bash
# Install Windows Terminal from Microsoft Store
# Much better than default command prompt
```

## Next Steps

Now that Linux is installed, you're ready to dive into the terminal!
            """
        },
        {
            "title": "Terminal Basics",
            "description": "Understanding the terminal, bash shell, and basic commands",
            "duration": 40,
            "content": """
# Terminal Basics

## Understanding the Terminal

The terminal (or command line) is where the real power of Linux lives. While graphical interfaces are nice, the terminal allows you to:
- Work faster
- Automate tasks
- Access all system features
- Run security tools

## Opening the Terminal

- **Ubuntu**: Press `Ctrl + Alt + T`
- **Any Linux**: Search for "Terminal" in applications

## The Shell Prompt

When you open a terminal, you'll see something like:
```bash
username@hostname:~$
```

Breaking it down:
- `username`: Your account name
- `hostname`: Computer name
- `~`: Current directory (~ means home)
- `$`: Regular user (# means root user)

## Essential Commands

###pwd - Print Working Directory
```bash
pwd
# Output: /home/username
# Shows where you currently are
```

### ls - List Files
```bash
# Basic listing
ls

# Detailed listing
ls -l

# Show hidden files
ls -a

# Human-readable file sizes
ls -lh

# Combine options
ls -lah
```

### cd - Change Directory
```bash
# Go to home directory
cd ~
cd

# Go to specific directory
cd /etc

# Go up one level
cd ..

# Go up two levels
cd ../..

# Go to previous directory
cd -
```

### clear - Clear Screen
```bash
clear
# Or press Ctrl+L
```

## Command Structure

```bash
command [options] [arguments]

# Example:
ls -la /home
# command: ls
# option: -la
# argument: /home
```

## Getting Help

```bash
# Manual pages
man ls
# Press 'q' to quit

# Quick help
ls --help

# Search manual
man -k search_term
```

## Command History

```bash
# View command history
history

# Re-run last command
!!

# Re-run command #5 from history
!5

# Search history
# Press Ctrl+R, then type to search
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Ctrl+C | Kill current command |
| Ctrl+D | Logout/Exit |
| Ctrl+L | Clear screen |
| Ctrl+A | Go to line start |
| Ctrl+E | Go to line end |
| Ctrl+U | Delete to line start |
| Ctrl+K | Delete to line end |
| Ctrl+R | Search history |
| Tab | Auto-complete |
| ↑/↓ | Previous/Next command |

## Tab Completion (Your Best Friend)

```bash
# Type partial name and press Tab
cd /h[Tab]      # Completes to /home/
ls Doc[Tab]     # Completes to Documents if it exists
```

## Practice Exercises

Try these commands:
1. `pwd` - Where are you?
2. `ls` - What files are here?
3. `cd /` - Go to root directory
4. `ls` - What's in root?
5. `cd ~` - Go back home
6. `history` - See your commands

## Common Mistakes

❌ `ls-l` (no space)
✅ `ls -l`

❌ `cd/ home` (space after cd)
✅ `cd /etc`

❌ Case-insensitive (Linux IS case-sensitive)
✅ `cd Documents` not `cd documents`

Master these basics and you're ready to navigate the Linux file system!
            """
        },
        {
            "title": "File System Navigation",
            "description": "Linux directory structure, absolute vs relative paths, and efficient navigation",
            "duration": 35,
            "content": """
# File System Navigation

## Linux Directory Structure

Linux uses a hierarchical file system starting from root (`/`):

```
/                    (Root directory)
├── home/           (User home directories)
│   └── username/   (Your files)
├── etc/            (Configuration files)
├── var/            (Variable data, logs)
├── tmp/            (Temporary files)
├── usr/            (User programs)
├── bin/            (Essential binaries)
├── sbin/           (System binaries)
├── dev/            (Device files)
├── proc/           (Process information)
└── root/           (Root user home)
```

## Important Directories

| Directory | Purpose | Example |
|-----------|---------|---------|
| `/home` | User home folders | `/home/john` |
| `/etc` | System configuration | `/etc/passwd` |
| `/var/log` | System logs | `/var/log/auth.log` |
| `/tmp` | Temporary files | Cleared on reboot |
| `/usr/bin` | User programs | `/usr/bin/python3` |
| `/opt` | Third-party software | `/opt/tools` |

## Absolute vs Relative Paths

### Absolute Paths
Start with `/` - complete path from root
```bash
cd /home/username/Documents
cd /etc/apache2
ls /var/log/syslog
```

### Relative Paths
Relative to current directory
```bash
# If you're in /home/username
cd Documents          # Goes to /home/username/Documents
cd ../other user     # Goes to /home/otheruser
```

## Special Path Symbols

| Symbol | Meaning |
|--------|---------|
| `/` | Root directory |
| `~` | Home directory |
| `.` | Current directory |
| `..` | Parent directory |
| `-` | Previous directory |

## Navigation Examples

```bash
# Start in home directory
cd ~
pwd
# Output: /home/username

# Go to Documents
cd Documents
pwd
# Output: /home/username/Documents

# Go up one level
cd ..
pwd
# Output: /home/username

# Go to root
cd /
ls

# Go to /var/log
cd /var/log
ls

# Return to home
cd ~

# Go to previous directory
cd -
```

## Listing Directory Contents

```bash
# List current directory
ls

# List specific directory
ls /etc

# List with details
ls -l

# List all (including hidden)
ls -a

# List recursively
ls -R

# List with human-readable sizes
ls -lh

# Sort by time
ls -lt

# Reverse order
ls -lr
```

## Understanding ls -l Output

```bash
$ ls -l
-rw-r--r-- 1 user group 4096 Dec 20 10:30 file.txt
│││││││││  │ │    │     │    │          │
│││││││││  │ │    │     │    │          └─ Filename
│││││││││  │ │    │     │    └─ Date modified
│││││││││  │ │    │     └─ Size (bytes)
│││││││││  │ │    └─ Group
│││││││││  │ └─ Owner
│││││││││  └─ Links
││││││││└─ Others permissions (r--)
│││││└─ Group permissions (r--)
││└─ Owner permissions (rw-)
└─ File type (- = file, d = directory, l = link)
```

## tree Command

```bash
# Install tree
sudo apt install tree

# View directory tree
tree

# Limit depth
tree -L 2

# Show hidden files
tree -a
```

## Finding Files

```bash
# Find command
find /home -name "*.txt"

# Locate (faster, needs updating)
sudo updatedb
locate filename

# Which (find executables)
which python3
```

## Practice Navigation

```bash
# Navigate to /etc
cd /etc

# List configuration files
ls

# Go to /var/log
cd /var/log

# List log files
ls -lh

# Go back to home
cd ~

# Create directory structure
mkdir -p workspace/projects/linux-learning

# Navigate to it
cd workspace/projects/linux-learning

# Verify location
pwd
```

## Pro Tips

1. **Use Tab completion** - Type partial name and press Tab
2. **Use cd -** - Quick toggle between two directories
3. **Use pushd/popd** - Directory stack navigation
4. **Use Ctrl+R** - Search command history

```bash
# pushd/popd example
pushd /var/log  # Save current dir and go to /var/log
# ... work in /var/log ...
popd            # Return to saved directory
```

Now you can navigate Linux like a pro!
            """
        }
    ]
    
    # Create lessons 1-4
    for index, lesson_data in enumerate(lessons, start=1):
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
    print(f"Created {len(lessons)} lessons for Linux Basics module")
    print("Linux Basics module seeded successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_tier_zero_linux(db)
    finally:
        db.close()
