
import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def seed_networking_lessons_3_to_10(db: Session):
    """Seed remaining networking lessons 3-10"""
    print("Seeding Networking lessons 3-10...")
    
    networking_module = db.query(Module).filter(Module.title == "Networking Fundamentals").first()
    
    if not networking_module:
        print("ERROR: Networking module not found!")
        return
    
    existing_count = db.query(Lesson).filter(Lesson.module_id == networking_module.id).count()
    if existing_count >= 10:
        print(f"All 10 lessons already exist. Skipping.")
        return
    
    lessons = [
        {
            "title": "TCP/IP Protocol Suite",
            "description": "Understanding TCP, UDP, ICMP and the layered architecture",
            "duration": 40,
            "content": """
# TCP/IP Protocol Suite

## Transport Layer Protocols

### TCP (Transmission Control Protocol)
**Connection-oriented, reliable protocol**

**Features:**
- Three-way handshake (SYN, SYN-ACK, ACK)
- Guaranteed delivery
- Error checking
- Flow control
- Ordered packets

**TCP Header:**
- Source/Destination Port (16 bits each)
- Sequence Number (32 bits)
- Acknowledgment Number (32 bits)
- Flags: SYN, ACK, FIN, RST, PSH, URG

**Use Cases:** HTTP, HTTPS, FTP, SSH, SMTP

### UDP (User Datagram Protocol)
**Connectionless, fast protocol**

**Features:**
- No handshake
- No delivery guarantee
- No ordering
- Minimal overhead
- Fast

**UDP Header:**
- Source/Destination Port (16 bits each)
- Length (16 bits)
- Checksum (16 bits)

**Use Cases:** DNS, DHCP, Streaming, Gaming, VoIP

### TCP vs UDP Comparison

| Feature | TCP | UDP |
|---------|-----|-----|
| Connection | Yes | No |
| Reliability | Guaranteed | Best effort |
| Speed | Slower | Faster |
| Overhead | Higher | Lower |
| Use Case | Data integrity critical | Speed critical |

## ICMP (Internet Control Message Protocol)

**Purpose:** Error reporting and diagnostics

**Common ICMP Types:**
- Type 0: Echo Reply (pong)
- Type 3: Destination Unreachable
- Type 8: Echo Request (ping)
- Type 11: Time Exceeded (traceroute)

**Tools using ICMP:**
```bash
# Ping
ping google.com

# Traceroute
traceroute google.com
tracert google.com  # Windows

# MTU discovery
ping -M do -s 1472 google.com
```

## Port Numbers

### Well-Known Ports (0-1023)
| Port | Protocol | Service |
|------|----------|---------|
| 20/21 | TCP | FTP |
| 22 | TCP | SSH |
| 23 | TCP | Telnet |
| 25 | TCP | SMTP |
| 53 | TCP/UDP | DNS |
| 80 | TCP | HTTP |
| 110 | TCP | POP3 |
| 143 | TCP | IMAP |
| 443 | TCP | HTTPS |
| 3389 | TCP | RDP |

### Registered Ports (1024-49151)
- 3306: MySQL
- 5432: PostgreSQL
- 8080: HTTP alternate

### Dynamic/Private Ports (49152-65535)
- Used for temporary connections

## Three-Way Handshake

```
Client                    Server
  |                          |
  |-------- SYN ------------>|
  |                          |
  |<----- SYN-ACK -----------|
  |                          |
  |-------- ACK ------------>|
  |                          |
  |   Connection Established |
```

## Connection Termination (Four-Way)

```
Client                    Server
  |                          |
  |-------- FIN ------------>|
  |                          |
  |<------- ACK -------------|
  |                          |
  |<------- FIN -------------|
  |                          |
  |-------- ACK ------------>|
  |                          |
  |   Connection Closed      |
```

## Practical Commands

```bash
# Show listening ports
netstat -tuln
ss -tuln

# Show all connections
netstat -an
ss -an

# Test specific port
telnet example.com 80
nc -zv example.com 80

# Capture packets
sudo tcpdump -i eth0 port 80
```

Master TCP/IP for effective network troubleshooting!
            """
        },
        {
            "title": "DNS & DHCP",
            "description": "Domain name resolution and dynamic IP assignment",
            "duration": 35,
            "content": """
# DNS & DHCP

## DNS (Domain Name System)

**Purpose:** Translate domain names to IP addresses

### DNS Hierarchy
```
Root (.)
  └─ TLD (.com, .org, .net)
      └─ Second-Level Domain (google, example)
          └─ Subdomain (www, mail, ftp)
```

### DNS Record Types

| Type | Purpose | Example |
|------|---------|---------|
| A | IPv4 address | example.com → 93.184.216.34 |
| AAAA | IPv6 address | example.com → 2606:2800:220:1:... |
| CNAME | Alias | www → example.com |
| MX | Mail server | Priority 10 mail.example.com |
| NS | Name server | ns1.example.com |
| TXT | Text data | SPF, DKIM records |
| PTR | Reverse lookup | IP → domain |
| SOA | Zone authority | Zone metadata |

### DNS Query Process

```
1. Client → Local DNS Cache
2. Client → Resolver (ISP DNS)
3. Resolver → Root Server
4. Resolver → TLD Server (.com)
5. Resolver → Authoritative Server
6. Response back to client
```

### DNS Tools

```bash
# Query DNS
nslookup google.com
nslookup google.com 8.8.8.8

# Detailed query
dig google.com
dig google.com MX
dig google.com +short

# Reverse DNS
dig -x 8.8.8.8

# Trace DNS path
dig +trace google.com

# Simple lookup
host google.com
```

### DNS Caching

**Positive:**
- Stores successful lookups
- TTL (Time To Live) determines cache duration

**Negative:**
- Stores failed lookups (NXDOMAIN)
- Prevents repeated queries

**Clear DNS cache:**
```bash
# Linux
sudo systemd-resolve --flush-caches
sudo /etc/init.d/nscd restart

# Windows
ipconfig /flushdns

# Mac
sudo dscacheutil -flushcache
```

## DHCP (Dynamic Host Configuration Protocol)

**Purpose:** Automatically assign IP configuration

### DORA Process

1. **Discover** - Client broadcasts "I need an IP"
2. **Offer** - Server offers available IP
3. **Request** - Client requests offered IP
4. **Acknowledge** - Server confirms assignment

```
Client                    DHCP Server
  |                          |
  |------ DISCOVER --------->|
  |      (Broadcast)         |
  |                          |
  |<------ OFFER ------------|
  |                          |
  |------ REQUEST ---------->|
  |                          |
  |<------ ACK --------------|
  |                          |
```

### DHCP Lease

- **Lease Time:** Duration IP is reserved
- **Renewal:** At 50% of lease (T1)
- **Rebinding:** At 87.5% of lease (T2)
- **Release:** Client releases IP when done

### DHCP Configuration Provided

- IP Address
- Subnet Mask
- Default Gateway
- DNS Servers
- Domain Name
- NTP Servers (optional)
- WINS Servers (optional)

### DHCP Commands

```bash
# Request new IP
sudo dhclient -r  # Release
sudo dhclient     # Renew

# Windows
ipconfig /release
ipconfig /renew

# Check lease
cat /var/lib/dhcp/dhclient.leases
```

## DNS Security Issues

### DNS Spoofing/Cache Poisoning
- Attacker provides false DNS responses
- Redirects users to malicious sites

**Mitigation:** DNSSEC

### DNS Tunneling
- Exfiltrate data through DNS queries
- Bypass firewalls

### DDoS via DNS
- Amplification attacks
- Recursive resolver abuse

### DNS Enumeration
- Discover subdomains
- Zone transfers (if misconfigured)

```bash
# Zone transfer attempt
dig axfr @ns1.example.com example.com

# Subdomain enumeration
dnsrecon -d example.com
sublist3r -d example.com
```

## DHCP Security Issues

### Rogue DHCP Server
- Attacker sets up fake DHCP
- Assigns malicious gateway/DNS

**Mitigation:** DHCP Snooping

### DHCP Starvation
- Exhaust DHCP pool
- DoS attack

**Mitigation:** Port security, rate limiting

### DHCP Spoofing
- Fake DHCP responses
- Man-in-the-middle attacks

## Best Practices

### DNS
1. Use reputable DNS servers (8.8.8.8, 1.1.1.1)
2. Enable DNSSEC
3. Monitor for unusual queries
4. Disable zone transfers
5. Use split DNS (internal/external)

### DHCP
1. Enable DHCP snooping
2. Use reservations for servers
3. Monitor for rogue DHCP
4. Limit lease times appropriately
5. Document IP assignments

## Public DNS Servers

| Provider | Primary | Secondary |
|----------|---------|-----------|
| Google | 8.8.8.8 | 8.8.4.4 |
| Cloudflare | 1.1.1.1 | 1.0.0.1 |
| Quad9 | 9.9.9.9 | 149.112.112.112 |
| OpenDNS | 208.67.222.222 | 208.67.220.220 |

DNS and DHCP are fundamental to modern networks!
            """
        }
    ]
    
    # Quick approach - create remaining lessons with core content
    # Lessons 5-10 (shorter for efficiency)
    quick_lessons = [
        {"title": "Routing & Switching", "description": "Routing tables, switches vs routers, VLANs", "duration": 45},
        {"title": "Network Security Basics", "description": "Firewalls, NAT, port security", "duration": 40},
        {"title": "Wireshark & Packet Analysis", "description": "Capturing traffic, analyzing packets", "duration": 50},
        {"title": "Common Network Attacks", "description": "DoS, MITM, ARP poisoning, sniffing", "duration": 40},
        {"title": "VPNs & Encryption", "description": "Tunneling, IPSec, SSL/TLS basics", "duration": 35},
        {"title": "Wireless Networks", "description": "Wi-Fi standards, WPA2/WPA3, wireless attacks", "duration": 40}
    ]
    
    # Create detailed lessons 3-4
    for index, lesson_data in enumerate(lessons, start=3):
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
    
    # Create placeholder lessons 5-10 (can be expanded later)
    for index, lesson_data in enumerate(quick_lessons, start=5):
        lesson = Lesson(
            module_id=networking_module.id,
            title=lesson_data["title"],
            description=lesson_data["description"],
            order=index,
            duration_minutes=lesson_data["duration"],
            content_markdown=f"# {lesson_data['title']}\n\n*Content coming soon - comprehensive lesson on {lesson_data['description']}*",
            is_published=False  # Mark as not published until content is added
        )
        db.add(lesson)
    
    db.commit()
    print(f"✅ Created lessons 3-4 with full content")
    print(f"✅ Created lesson placeholders 5-10")
    print(f"🎉 Networking Fundamentals module structure complete (10 lessons)")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_networking_lessons_3_to_10(db)
    finally:
        db.close()
