
import sys
import os
from sqlalchemy.orm import Session

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def seed_linux_lessons_5_to_12(db: Session):
    """Seed remaining lessons 5-12 for Linux Basics module"""
    print("Seeding Linux Basics lessons 5-12...")
    
    # Get Linux Basics module
    linux_module = db.query(Module).filter(Module.title == "Linux Basics").first()
    
    if not linux_module:
        print("ERROR: Linux Basics module not found. Run seed_linux_basics.py first!")
        return
    
    # Check if lessons already exist
    existing_count = db.query(Lesson).filter(Lesson.module_id == linux_module.id).count()
    if existing_count >= 12:
        print(f"All 12 lessons already exist ({existing_count} found). Skipping.")
        return
    
    # Lessons 5-12
    lessons = [
        {
            "title": "File Operations",
            "description": "Creating, moving, copying, and deleting files and directories",
            "duration": 40,
            "content": """
# File Operations

Master the essential file manipulation commands that you'll use every day in Linux.

## Creating Files

### touch - Create Empty Files
```bash
# Create a single file
touch file.txt

# Create multiple files
touch file1.txt file2.txt file3.txt

# Create file with timestamp
touch -t 202312251200 oldfile.txt

# Update existing file timestamp
touch existing.txt
```

### echo - Create File with Content
```bash
# Create file with text
echo "Hello World" > greeting.txt

# Append to file
echo "New line" >> greeting.txt

# Create empty file
echo -n > empty.txt
```

### cat - Concatenate and Create
```bash
# Create file interactively (Ctrl+D to save)
cat > newfile.txt
Type your content here...
[Ctrl+D]

# Combine files
cat file1.txt file2.txt > combined.txt
```

## Creating Directories

```bash
# Create single directory
mkdir projects

# Create multiple directories
mkdir dir1 dir2 dir3

# Create nested directories
mkdir -p workspace/projects/WebApp/src

# Create with permissions
mkdir -m 755 public_folder
```

## Copying Files and Directories

### cp - Copy Command
```bash
# Copy file
cp source.txt destination.txt

# Copy to directory
cp file.txt /home/user/Documents/

# Copy multiple files
cp file1.txt file2.txt /destination/

# Copy directory (recursive)
cp -r folder/ /backup/folder/

# Copy with progress (verbose)
cp -v source.txt dest.txt

# Preserve permissions and timestamps
cp -p important.txt backup.txt

# Interactive (ask before overwrite)
cp -i file.txt existing.txt
```

## Moving and Renaming

### mv - Move Command
```bash
# Rename file
mv oldname.txt newname.txt

# Move file to directory
mv file.txt /home/user/Documents/

# Move multiple files
mv *.txt /destination/

# Move directory
mv old_folder/ new_folder/

# Interactive mode
mv -i source.txt destination.txt

# Never overwrite
mv -n file.txt existing.txt

# Backup before overwrite
mv -b file.txt existing.txt
```

##Deleting Files and Directories

### rm - Remove Command
```bash
# Delete file
rm file.txt

# Delete multiple files
rm file1.txt file2.txt

# Delete with confirmation
rm -i important.txt

# Force delete (no confirmation)
rm -f file.txt

# Delete directory and contents
rm -r folder/

# Force delete directory
rm -rf folder/

# Verbose mode
rm -v file.txt

# Delete all .txt files
rm *.txt
```

### rmdir - Remove Empty Directories
```bash
# Remove empty directory
rmdir empty_folder/

# Remove nested empty directories
rmdir -p path/to/empty/dirs/
```

## Wildcards and Patterns

```bash
# * matches any characters
rm *.txt           # All .txt files
cp *.jpg /photos/  # All .jpg files

# ? matches single character
rm file?.txt       # file1.txt, file2.txt, fileA.txt

# [] matches range
rm file[1-5].txt   # file1.txt through file5.txt
rm file[abc].txt   # filea.txt, fileb.txt, filec.txt

# {} braces expansion
mkdir {Jan,Feb,Mar,Apr}_{2023,2024}
```

## Pro Tips and Best Practices

### 1. Always Use -i for Important Operations
```bash
# Safer deletions
alias rm='rm -i'
alias mv='mv -i'
alias cp='cp -i'
```

### 2. Be Careful with rm -rf
```bash
# DANGEROUS - Never run as root!
# rm -rf /  # DON'T DO THIS!

# Safe practice: check first
ls -la folder/
rm -rf folder/
```

### 3. Use --help and man
```bash
cp --help
man rm
```

## Common Tasks

### Backup Directory
```bash
# Copy with timestamp
cp -r important_folder/ important_folder_$(date +%Y%m%d)/

# Or use tar (better for backups)
tar -czf backup_$(date +%Y%m%d).tar.gz folder/
```

### Bulk Rename
```bash
# Using mmv (if installed)
sudo apt install mmv
mmv "*.txt" "#1.md"

# Using rename
rename 's/\.txt$/.md/' *.txt

# Manual loop
for file in *.txt; do
    mv "$file" "${file%.txt}.md"
done
```

### Find and Delete
```bash
# Delete all .log files older than 7 days
find /var/log -name "*.log" -mtime +7 -delete

# Delete empty directories
find . -type d -empty -delete
```

## Practice Exercises

Try these operations:
```bash
# 1. Create project structure
mkdir -p myproject/{src,tests,docs}
cd myproject
touch src/main.py src/utils.py
touch tests/test_main.py
touch docs/README.md

# 2. Copy and reorganize
cp src/main.py src/main_backup.py
mv src/utils.py src/helpers.py

# 3. Cleanup
rm src/main_backup.py
```

Master these commands and file manipulation becomes second nature!
            """
        },
        {
            "title": "File Permissions",
            "description": "Understanding ownership, chmod, chown, and security permissions",
            "duration": 45,
            "content": """
# File Permissions

Understanding Linux permissions is critical for security. This lesson covers ownership, permissions, and how to modify them.

## Understanding Permissions

### The Permission Model

Every file/directory in Linux has:
1. **Owner** - The user who owns it
2. **Group** - A group of users
3. **Others** - Everyone else

Each has three permission types:
- **r** (read) - View file contents
- **w** (write) - Modify file
- **x** (execute) - Run as program

### Reading ls -l Output

```bash
$ ls -l file.txt
-rw-r--r-- 1 john developers 1024 Dec 20 10:00 file.txt
│││││││││  │ │    │         │    │
│││││││││  │ │    │         │    └─ Filename
│││││││││  │ │    │         └─ Size
│││││││││  │ │    └─ Group
│││││││││  │ └─ Owner
│││││││││  └─ Link count
││││││││└─ Others: r-- (read only)
│││││└─ Group: r-- (read only)
││└─ Owner: rw- (read, write)
└─ File type: - (regular file)
```

### File Types

| Symbol | Type |
|--------|------|
| `-` | Regular file |
| `d` | Directory |
| `l` | Symbolic link |
| `c` | Character device |
| `b` | Block device |
| `s` | Socket |
| `p` | Named pipe |

## Permission Numbers (Octal)

| Permission | Binary | Octal |
|------------|--------|-------|
| --- | 000 | 0 |
| --x | 001 | 1 |
| -w- | 010 | 2 |
| -wx | 011 | 3 |
| r-- | 100 | 4 |
| r-x | 101 | 5 |
| rw- | 110 | 6 |
| rwx | 111 | 7 |

### chmod - Change Permissions

#### Symbolic Mode
```bash
# Add execute for owner
chmod u+x script.sh

# Remove write for group
chmod g-w file.txt

# Set read-only for others
chmod o=r file.txt

# Add execute for everyone
chmod a+x program

# Multiple changes
chmod u+x,g-w,o-r file.txt
```

#### Numeric Mode
```bash
# rwxr-xr-x (755) - Common for scripts
chmod 755 script.sh

# rw-r--r-- (644) - Common for files
chmod 644 document.txt

# rw------- (600) - Private file
chmod 600 private.key

# rwxrwxrwx (777) - Full access (DANGEROUS!)
chmod 777 file.txt  # Don't do this unless necessary!

# Recursive
chmod -R 755 directory/
```

## Ownership Commands

### chown - Change Owner
```bash
# Change owner
sudo chown john file.txt

# Change owner and group
sudo chown john:developers file.txt

# Recursive
sudo chown -R john:developers project/

# Change only group
sudo chown :developers file.txt
```

### chgrp - Change Group
```bash
# Change group
sudo chgrp developers file.txt

# Recursive
sudo chgrp -R developers project/
```

## Special Permissions

### SetUID (SUID) - 4000
Allows file to run as owner
```bash
# Set SUID
chmod 4755 program
chmod u+s program

# Check
ls -l program
-rwsr-xr-x  # Notice 's' instead of 'x'
```

### SetGID (SGID) - 2000
On directories: new files inherit group
```bash
# Set SGID on directory
chmod 2775 shared_folder/
chmod g+s shared_folder/

# Check
ls -ld shared_folder/
drwxrwsr-x  # Notice 's' in group
```

### Sticky Bit - 1000
On directories: only owner can delete files
```bash
# Set sticky bit
chmod 1777 /tmp
chmod +t shared_temp/

# Check
ls -ld /tmp
drwxrwxrwt  # Notice 't' at end
```

## umask - Default Permissions

```bash
# Check current umask
umask
# Output: 0022

# Set umask
umask 0027

# Calculate default permissions:
# Files: 666 - umask = 666 - 022 = 644
# Dirs:  777 - umask = 777 - 022 = 755
```

## Access Control Lists (ACLs)

For fine-grained permissions:

```bash
# Install ACL tools
sudo apt install acl

# View ACLs
getfacl file.txt

# Set ACL for specific user
setfacl -m u:alice:rw file.txt

# Set ACL for specific group
setfacl -m g:admins:rwx folder/

# Remove ACL
setfacl -x u:alice file.txt

# Remove all ACLs
setfacl -b file.txt
```

## Common Permission Scenarios

### Web Server Files
```bash
# Directories
chmod 755 /var/www/html/
# Files
chmod 644 /var/www/html/*.html
```

### SSH Keys
```bash
# Private key (must be 600!)
chmod 600 ~/.ssh/id_rsa

# Public key
chmod 644 ~/.ssh/id_rsa.pub

# SSH directory
chmod 700 ~/.ssh/
```

### Scripts
```bash
# Make executable
chmod +x script.sh

# Run it
./script.sh
```

### Shared Folder
```bash
# Create shared folder
sudo mkdir /shared
sudo chmod 2775 /shared
sudo chown :team /shared

# Now members of 'team' group can share files
```

## Security Best Practices

1. **Principle of Least Privilege**
   - Give minimum permissions needed
   - Don't use 777 unless absolutely necessary

2. **Protect Sensitive Files**
   ```bash
   chmod 600 ~/.ssh/id_rsa
   chmod 600 ~/.gnupg/*
   chmod 600 ~/.password-store/*
   ```

3. **Regular Audits**
   ```bash
   # Find world-writable files
   find / -perm -002 -type f 2>/dev/null
   
   # Find SUID files
   find / -perm -4000 2>/dev/null
   ```

4. Using sudo Properly**
   ```bash
   # Don't do this
   sudo chmod -R 777 /

   # Do this
   sudo chmod 755 /specific/path
   ```

## Troubleshooting

```bash
# Permission denied when running script?
chmod +x script.sh

# Can't modify file?
ls -l file.txt  # Check permissions
# sudo chown yourusername file.txt

# Can't delete file in directory?
ls -ld directory/  # Check directory permissions
```

## Practice Exercises

```bash
# 1. Create and secure a private file
touch secret.txt
chmod 600 secret.txt
ls -l secret.txt

# 2. Create executable script
echo '#!/bin/bash' > hello.sh
echo 'echo "Hello World"' >> hello.sh
chmod +x hello.sh
./hello.sh

# 3. Create shared project folder
sudo mkdir /projects
sudo chmod 2775 /projects
sudo chgrp developers /projects
```

Understanding permissions is fundamental to Linux security!
            """
        }
    ]
    
    # Add lessons 5-6 for now
    for index, lesson_data in enumerate(lessons, start=5):
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
    print(f"Created lessons 5-{4+len(lessons)} for Linux Basics module")
    print("Linux lessons 5-6 seeded successfully!")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_linux_lessons_5_to_12(db)
    finally:
        db.close()
