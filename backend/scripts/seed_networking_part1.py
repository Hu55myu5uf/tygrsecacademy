
import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Tier, Module, Lesson

def seed_networking_module(db: Session):
    """Seed Networking Fundamentals module for Tier 0"""
    print("Seeding Networking Fundamentals module...")
    
    # Get Tier 0
    tier0 = db.query(Tier).filter(Tier.tier_number == 0).first()
    if not tier0:
        print("ERROR: Tier 0 not found!")
        return
    
    # Check if module exists
    existing = db.query(Module).filter(
        Module.tier_id == tier0.id,
        Module.title == "Networking Fundamentals"
    ).first()
    
    if existing:
        print("Module already exists. Skipping.")
        return
    
    # Create module
    networking_module = Module(
        tier_id=tier0.id,
        title="Networking Fundamentals",
        description="Master networking concepts essential for cybersecurity. Learn protocols, IP addressing, routing, security fundamentals, and practical packet analysis.",
        order=2,
        estimated_hours=7,
        is_published=True
    )
    
    db.add(networking_module)
    db.commit()
    db.refresh(networking_module)
    
    # Create lessons 1-5
    lessons_part1 = [
        {
            "title": "Introduction to Networking",
            "description": "Understanding the OSI model, network protocols, and types of networks",
            "duration": 30,
            "content": """
# Introduction to Networking

## Learning Objectives
- Understand the OSI and TCP/IP models
- Learn about different network types (LAN, WAN, MAN)
- Recognize common network protocols and their purposes

## The OSI Model

The **Open Systems Interconnection (OSI)** model is a conceptual framework that standardizes network communication into 7 layers:

| Layer | Name | Function | Protocols/Examples |
|-------|------|----------|-------------------|
| 7 | Application | User interface, applications | HTTP, FTP, SMTP, DNS |
| 6 | Presentation | Data formatting, encryption | SSL/TLS, JPEG, ASCII |
| 5 | Session | Connection management | NetBIOS, RPC |
| 4 | Transport | End-to-end communication | TCP, UDP |
| 3 | Network | Routing, logical addressing | IP, ICMP, OSPF |
| 2 | Data Link | Physical addressing | Ethernet, MAC, ARP |
| 1 | Physical | Hardware, cables, signals | Cables, hubs, NICs |

### Mnemonic
**Please Do Not Throw Sausage Pizza Away**
(Physical, Data Link, Network, Transport, Session, Presentation, Application)

## TCP/IP Model

A simplified 4-layer model used in practice:

1. **Network Access** (Physical + Data Link)
2. **Internet** (Network)
3. **Transport** (Transport)
4. **Application** (Session + Presentation + Application)

## Network Types

### LAN (Local Area Network)
- **Coverage:** Single building or campus
- **Speed:** High (1-100 Gbps)
- **Example:** Office network, home network
- **Ownership:** Private

### WAN (Wide Area Network)
- **Coverage:** Cities, countries, continents
- **Speed:** Varies (2 Mbps - 100 Gbps)
- **Example:** Internet, corporate networks connecting offices
- **Ownership:** Often leased from ISPs

### MAN (Metropolitan Area Network)
- **Coverage:** City or metropolitan area
- **Speed:** High
- **Example:** City-wide Wi-Fi, cable TV networks

### PAN (Personal Area Network)
- **Coverage:** A few meters
- **Example:** Bluetooth devices, NFC

## Key Network Devices

### Hub
- Layer 1 device
- Broadcasts to all ports
- No intelligence
- **Security Issue:** Everyone sees all traffic

### Switch
- Layer 2 device
- Forwards based on MAC addresses
- Creates separate collision domains
- **More secure** than hubs

### Router
- Layer 3 device
- Forwards based on IP addresses
- Connects different networks
- Performs NAT, filtering

### Firewall
- Can operate at multiple layers
- Filters traffic based on rules
- Protects network from threats

## Common Protocols

### Application Layer
- **HTTP/HTTPS** - Web browsing
- **FTP/SFTP** - File transfer
- **SMTP/POP3/IMAP** - Email
- **DNS** - Domain name resolution
- **SSH** - Secure remote access
- **Telnet** - Insecure remote access (avoid!)

### Transport Layer
- **TCP** - Reliable, connection-oriented
- **UDP** - Fast, connectionless

### Network Layer
- **IP** - Internet Protocol (addressing)
- **ICMP** - Error messages, ping
- **ARP** - Maps IP to MAC address

## Client-Server vs Peer-to-Peer

### Client-Server
- Centralized server provides services
- Clients request resources
- **Example:** Web browsing, email servers
- **Pro:** Centralized control, security
- **Con:** Single point of failure

### Peer-to-Peer (P2P)
- All nodes are equal
- Share resources directly
- **Example:** BitTorrent, blockchain
- **Pro:** No central server needed
- **Con:** Harder to secure

## Network Topologies

### Star
- All devices connect to central hub/switch
- **Pro:** Easy to manage, failure isolation
- **Con:** Hub is single point of failure

### Bus
- All devices on single cable
- **Pro:** Simple, inexpensive
- **Con:** Cable break affects all

### Ring
- Devices in circular loop
- **Pro:** Equal access
- **Con:** Break disrupts network

### Mesh
- Every device connects to every other
- **Pro:** Redundancy, reliability
- **Con:** Expensive, complex

## Bandwidth vs Latency

### Bandwidth
- **Amount** of data transferred per second
- Measured in bps, Kbps, Mbps, Gbps
- **Analogy:** Width of a pipe

### Latency
- **Time** for data to travel from source to destination
- Measured in milliseconds (ms)
- **Analogy:** Length of a pipe

**High bandwidth + Low latency = Best performance**

## Security Implications

### Layer 1 (Physical)
- Cable tapping
- Unauthorized access to equipment

### Layer 2 (Data Link)
- MAC spoofing
- ARP poisoning
- VLAN hopping

### Layer 3 (Network)
- IP spoofing
- Routing attacks
- DoS/DDoS

### Layer 7 (Application)
- SQL injection
- XSS attacks
- Phishing

## Practical Examples

### Check Your Network Info (Linux/Mac)
```bash
# IP address
ip addr show
ifconfig

# Routing table
ip route
netstat -r

# DNS servers
cat /etc/resolv.conf
```

### Windows
```powershell
# IP configuration
ipconfig /all

# Routing table
route print

# DNS cache
ipconfig /displaydns
```

## Key Takeaways

1. **OSI Model** has 7 layers, each with specific functions
2. **TCP/IP Model** is the practical implementation (4 layers)
3. **Different network types** serve different purposes (LAN, WAN, MAN)
4. **Devices operate at different layers** (hub, switch, router)
5. **Protocols define rules** for communication at each layer
6. **Security threats exist at every layer** of the network

Understanding these fundamentals is crucial for network security analysis and defense!
            """
        },
        {
            "title": "IP Addressing & Subnetting",
            "description": "IPv4/IPv6 addressing, CIDR notation, and subnetting calculations",
            "duration": 45,
            "content": """
# IP Addressing & Subnetting

## Learning Objectives
- Understand IPv4 and IPv6 addressing
- Master CIDR notation and subnet masks
- Perform subnetting calculations
- Recognize private vs public IP addresses

## IPv4 Addressing

### Structure
- 32-bit address
- Written as 4 octets (dotted decimal)
- **Example:** 192.168.1.100

```
192     .  168     .  1       .  100
11000000.  10101000.  00000001.  01100100
```

### IP Address Classes (Legacy)

| Class | Range | Default Mask | Networks | Hosts |
|-------|-------|--------------|----------|-------|
| A | 1-126 | 255.0.0.0 (/8) | 126 | 16,777,214 |
| B | 128-191 | 255.255.0.0 (/16) | 16,384 | 65,534 |
| C | 192-223 | 255.255.255.0 (/24) | 2,097,152 | 254 |
| D | 224-239 | Multicast | - | - |
| E | 240-255 | Reserved | - | - |

**Note:** 127.x.x.x is reserved for loopback (localhost)

## Private IP Addresses (RFC 1918)

These are NOT routed on the internet:

- **Class A:** 10.0.0.0 - 10.255.255.255 (10.0.0.0/8)
- **Class B:** 172.16.0.0 - 172.31.255.255 (172.16.0.0/12)
- **Class C:** 192.168.0.0 - 192.168.255.255 (192.168.0.0/16)

## Subnet Masks

A subnet mask defines which portion is network vs host.

### Example
```
IP:      192.168.1.100
Mask:    255.255.255.0
Binary:  11111111.11111111.11111111.00000000

Network: 192.168.1.0
Host:    .100
```

### CIDR Notation

**Classless Inter-Domain Routing** - more flexible than classes

```
192.168.1.0/24
            ^^
            |
      Number of network bits
```

| CIDR | Subnet Mask | Usable Hosts |
|------|-------------|--------------|
| /32 | 255.255.255.255 | 1 (host) |
| /31 | 255.255.255.254 | 2 (point-to-point) |
| /30 | 255.255.255.252 | 2 |
| /29 | 255.255.255.248 | 6 |
| /28 | 255.255.255.240 | 14 |
| /27 | 255.255.255.224 | 30 |
| /26 | 255.255.255.192 | 62 |
| /25 | 255.255.255.128 | 126 |
| /24 | 255.255.255.0 | 254 |
| /16 | 255.255.0.0 | 65,534 |
| /8 | 255.0.0.0 | 16,777,214 |

## Subnetting Calculations

### Formula
- **Number of subnets:** 2^n (where n = borrowed bits)
- **Hosts per subnet:** 2^h - 2 (where h = host bits)

### Example 1: Divide 192.168.1.0/24 into 4 subnets

```
Original: /24 (255.255.255.0)
Need 4 subnets: 2^2 = 4
Borrow 2 bits: /24 + 2 = /26

New mask: 255.255.255.192 (/26)
Hosts per subnet: 2^6 - 2 = 62

Subnets:
1. 192.168.1.0/26   (0-63)     → .0 to .63
2. 192.168.1.64/26  (64-127)   → .64 to .127
3. 192.168.1.128/26 (128-191)  → .128 to .191
4. 192.168.1.192/26 (192-255)  → .192 to .255
```

### Example 2: Need 50 hosts per subnet

```
Hosts needed: 50
2^6 - 2 = 62 hosts ✓ (fits!)
Host bits: 6
Network bits: 32 - 6 = 26

Use /26 subnet mask
```

## Special IP Addresses

### Network Address
- All host bits are 0
- **Example:** 192.168.1.0/24 → 192.168.1.0

### Broadcast Address
- All host bits are 1
- **Example:** 192.168.1.0/24 → 192.168.1.255

### Loopback
- 127.0.0.1 (localhost)
- Used for testing

### APIPA (Automatic Private IP Addressing)
- 169.254.0.0/16
- Assigned when DHCP fails

## IPv6 Addressing

### Why IPv6?
- IPv4: ~4.3 billion addresses (exhausted!)
- IPv6: 340 undecillion addresses

### Structure
- 128-bit address
- Written as 8 groups of 4 hex digits
- **Example:** 2001:0db8:85a3:0000:0000:8a2e:0370:7334

### Shorthand Rules

1. **Leading zeros can be omitted**
   ```
   2001:0db8 → 2001:db8
   ```

2. **Consecutive groups of zeros can be replaced with ::**
   ```
   2001:0db8:0000:0000:0000:0000:0000:0001
   →
   2001:0db8::1
   ```

### IPv6 Address Types

- **Global Unicast:** 2000::/3 (routable internet addresses)
- **Link-Local:** fe80::/10 (local network only)
- **Loopback:** ::1 (equivalent to 127.0.0.1)
- **Multicast:** ff00::/8

## Practical Commands

### Check IP Address
```bash
# Linux/Mac
ip addr show
ifconfig

# Windows
ipconfig

# Get public IP
curl ifconfig.me
curl ipinfo.io/ip
```

### Calculate Subnets
```bash
# Install ipcalc
sudo apt install ipcalc

# Use it
ipcalc 192.168.1.0/24
ipcalc 192.168.1.0/26
```

### Online Tools
- ipcalc.app
- subnet-calculator.com
- subnetmask.info

## Security Implications

### IP Spoofing
- Attacker uses fake source IP
- Makes tracking difficult
- Used in DDoS attacks

### Network Reconnaissance
- Attackers scan IP ranges
- Identify live hosts
- Discover network structure

### Private IP Exposure
- Can reveal internal network structure
- NAT helps hide internal IPs

## Best Practices

1. **Use private IPs internally**
2. **Implement proper subnetting** for security segmentation
3. **Document your IP addressing scheme**
4. **Reserve IP ranges** for specific purposes (servers, printers, DHCP)
5. **Use IPv6** where possible (future-proof)

## Practice Problems

### Problem 1
How many usable hosts in 10.0.0.0/22?
```
32 - 22 = 10 host bits
2^10 - 2 = 1022 hosts
```

### Problem 2
What is the broadcast address for 172.16.50.0/28?
```
/28 = 255.255.255.240
Block size = 256 - 240 = 16
50 ÷ 16 = 3 remainder 2
Network: 172.16.50.48
Broadcast: 172.16.50.63
```

### Problem 3
Is 172.20.1.50 a private IP?
```
Yes! Falls in 172.16.0.0 - 172.31.255.255 range
```

## Key Takeaways

1. **IPv4 uses 32 bits**, IPv6 uses 128 bits
2. **Private IPs** aren't routed on internet
3. **CIDR notation** (/24) is more flexible than classes
4. **Subnetting allows network segmentation** for security
5. **Network and broadcast addresses** can't be assigned to hosts
6. Understanding IP addressing is **fundamental to network security**

Mastering IP addressing and subnetting is essential for network administration and security!
            """
        }
    ]
    
    # Create lessons
    for index, lesson_data in enumerate(lessons_part1, start=1):
        lesson = Lesson(
            module_id=networking_module.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            order=index,
            duration_minutes=lesson_data["duration"],
            content_markdown=lesson_data["content"].strip(),
            is_published=True
        )
        db.add(lesson)
    
    db.commit()
    print(f"✅ Created Networking module with lessons 1-2")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_networking_module(db)
    finally:
        db.close()
