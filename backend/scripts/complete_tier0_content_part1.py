import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def update_lesson_content(db: Session, module_title: str, lesson_order: int, content: str):
    """Update a specific lesson's content"""
    module = db.query(Module).filter(Module.title == module_title).first()
    if not module:
        print(f"Module '{module_title}' not found!")
        return False
    
    lesson = db.query(Lesson).filter(
        Lesson.module_id == module.id,
        Lesson.order == lesson_order
    ).first()
    
    if not lesson:
        print(f"Lesson {lesson_order} in '{module_title}' not found!")
        return False
    
    lesson.content_markdown = content.strip()
    lesson.is_published = True
    db.commit()
    return True

def complete_networking_module(db: Session):
    """Complete remaining Networking lessons 5-10"""
    print("Completing Networking Fundamentals module...")
    
    lessons_content = {
        5: {
            "content": """
# Routing & Switching

## Understanding Routing

**Routing** is the process of selecting paths in a network to send data packets.

### Router Functions
1. **Path Selection** - Choose best route
2. **Packet Forwarding** - Send data to next hop
3. **Network Segmentation** - Connect different networks

### Routing Table

```bash
# View routing table
ip route show
route -n
netstat -rn

# Example output:
Destination     Gateway         Genmask         Interface
0.0.0.0         192.168.1.1     0.0.0.0         eth0
192.168.1.0     0.0.0.0         255.255.255.0   eth0
```

### Types of Routes
- **Directly Connected** - Networks directly attached
- **Static Routes** - Manually configured
- **Dynamic Routes** - Learned via routing protocols

### Routing Protocols

**Distance Vector (RIP)**
- Uses hop count as metric
- Shares entire routing table
- Simple but slow convergence

**Link State (OSPF)**
- Knows entire network topology
- Faster convergence
- More CPU intensive

**Path Vector (BGP)**
- Used for internet routing
- Policy-based routing
- Handles routing between ISPs

## Switching Fundamentals

**Switch** - Layer 2 device that forwards frames based on MAC addresses

### How Switches Work

1. **Learning** - Records MAC addresses from source
2. **Flooding** - Sends to all ports if destination unknown
3. **Forwarding** - Sends to specific port when learned
4. **Filtering** - Blocks frames when source/dest on same port

### MAC Address Table

```bash
# View MAC table (on managed switch)
show mac address-table

Port    MAC Address       VLAN
----    -------------     ----
1       aa:bb:cc:11:22:33 1
2       dd:ee:ff:44:55:66 1
```

### Switch vs Hub

| Feature | Hub | Switch |
|---------|-----|--------|
| Layer | 1 (Physical) | 2 (Data Link) |
| Intelligence | None | MAC learning |
| Collision Domain | Shared | Per port |
| Performance | Slow | Fast |
| Security | Low | Better |

## VLANs (Virtual LANs)

**Purpose**: Logically segment networks without physical separation

### Benefits
- **Security** - Isolate traffic
- **Performance** - Reduce broadcast domains
- **Flexibility** - Group users logically

### VLAN Configuration

```bash
# Create VLAN
vlan 10
name Engineering

vlan 20
name Sales

# Assign port to VLAN
interface FastEthernet0/1
switchport mode access
switchport access vlan 10
```

### VLAN Types

**Access VLAN** - Single VLAN per port
**Voice VLAN** - Separate VLAN for VoIP phones
**Native VLAN** - Default VLAN for untagged traffic
**Management VLAN** - For switch management

### Inter-VLAN Routing

Devices in different VLANs need a router to communicate:

```
VLAN 10 (Finance) ←→ Router ←→ VLAN 20 (HR)
```

## Spanning Tree Protocol (STP)

**Problem**: Network loops cause broadcast storms

**Solution**: STP creates loop-free topology

### STP Terminology
- **Root Bridge** - Central reference point
- **Root Port** - Best path to root
- **Designated Port** - Forwards frames
- **Blocked Port** - Prevents loops

### Port States
1. Blocking (blocks traffic)
2. Listening (no data, learns topology)
3. Learning (learns MAC, no forwarding)
4. Forwarding (normal operation)
5. Disabled (admin down)

## Link Aggregation (EtherChannel)

**Purpose**: Combine multiple physical links into one logical link

### Benefits
- **Bandwidth** - Multiply throughput
- **Redundancy** - Automatic failover
- **Load Balancing** - Distribute traffic

```bash
# Configure EtherChannel
interface range FastEthernet0/1-2
channel-group 1 mode active
```

## Router Configuration Basics

```bash
# Enter config mode
Router> enable
Router# configure terminal

# Set hostname
Router(config)# hostname R1

# Configure interface
R1(config)# interface gigabitethernet0/0
R1(config-if)# ip address 192.168.1.1 255.255.255.0
R1(config-if)# no shutdown

# Add static route
R1(config)# ip route 10.0.0.0 255.255.255.0 192.168.1.254

# Save config
R1# copy running-config startup-config
```

## Practical Scenarios

### Home Network
```
Internet → Modem → Router/Switch → Devices
```
- Router provides NAT, DHCP, firewall
- Built-in switch for wired devices
- Wireless AP for WiFi

### Enterprise Network
```
Internet → Border Router → Core Switch → Distribution Switches → Access Switches → Devices
```
- Hierarchical design
- Redundant paths
- VLANs for segmentation

## Key Takeaways

- Routers work at Layer 3 (IP addresses)
- Switches work at Layer 2 (MAC addresses)
- VLANs provide logical network segmentation
- STP prevents network loops
- Understanding routing/switching is fundamental to networking

Master these concepts for network design and troubleshooting!
"""
        },
        6: {
            "content": """
# Network Security Basics

## Firewall Fundamentals

**Firewall** - Security system that monitors and controls network traffic based on rules

### Types of Firewalls

**Packet Filtering**
- Inspects packet headers
- Permit/deny based on IP, port, protocol
- Fast but basic security

**Stateful Inspection**
- Tracks connection state
- Understands context
- Better security than packet filtering

**Application Layer (Proxy)**
- Inspects application data
- Can decrypt and inspect content
- More secure but slower

**Next-Generation Firewall (NGFW)**
- Deep packet inspection
- Intrusion prevention
- Application awareness
- Threat intelligence

### Firewall Rules

```bash
# UFW (Ubuntu Firewall)
sudo ufw allow 22/tcp          # Allow SSH
sudo ufw allow 80/tcp          # Allow HTTP
sudo ufw allow 443/tcp         # Allow HTTPS
sudo ufw deny 23/tcp           # Deny Telnet
sudo ufw enable

# iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 80 -j ACCEPT
sudo iptables -A INPUT -j DROP  # Default deny
```

### Rule Order Matters!
- Rules processed top-to-bottom
- First match wins
- Always end with explicit deny

## Network Address Translation (NAT)

**Purpose**: Allow multiple devices to share single public IP

### Types of NAT

**Static NAT** - One-to-one mapping
```
Private: 192.168.1.10 ↔ Public: 203.0.113.5
```

**Dynamic NAT** - Pool of public IPs
```
Private IPs → Pool of Public IPs
```

**PAT (Port Address Translation)**
```
192.168.1.10:50000 → 203.0.113.5:50000
192.168.1.11:50001 → 203.0.113.5:50001
192.168.1.12:50002 → 203.0.113.5:50002
```

### Benefits
- **IP Conservation** - Fewer public IPs needed
- **Security** - Hides internal network
- **Flexibility** - Easy to change internal addressing

### Drawbacks
- Breaks end-to-end connectivity
- Complicates some protocols (FTP, SIP)
- Can impact performance

## Port Security

**Problem**: Unauthorized devices connecting to network

**Solution**: Restrict which devices can connect to each port

### MAC Address Filtering

```bash
# Cisco switch
interface FastEthernet0/1
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address aaaa.bbbb.cccc
switchport port-security violation shutdown
```

### Violation Actions
- **Protect** - Drop packets, no alert
- **Restrict** - Drop packets, log alert
- **Shutdown** - Disable port (most secure)

### 802.1X (Network Access Control)

Requires authentication before network access:

```
Device → Switch → RADIUS Server → Authentication
```

## Access Control Lists (ACLs)

**Purpose**: Filter traffic based on criteria

### Standard ACLs
```bash
# Cisco
access-list 10 deny 192.168.1.100
access-list 10 permit 192.168.1.0 0.0.0.255

interface GigabitEthernet0/0
ip access-group 10 in
```

### Extended ACLs
```bash
access-list 100 deny tcp any any eq telnet
access-list 100 permit tcp 192.168.1.0 0.0.0.255 any eq 443
access-list 100 deny ip any any
```

## Network Segmentation

**Defense in Depth**: Multiple layers of security

### Demilitarized Zone (DMZ)

```
Internet
   ↓
Firewall
   ↓
 DMZ (Web Server, Mail Server)
   ↓
Firewall
   ↓
Internal Network
```

### Screened Subnet

```
Internet → Firewall → DMZ → Firewall → Internal
```

Benefits:
- Isolates public-facing servers
- Protects internal network
- Contains breaches

## Intrusion Detection/Prevention

### IDS vs IPS

**IDS (Intrusion Detection System)**
- Monitors traffic
- Alerts on suspicious activity
- Passive (doesn't block)

**IPS (Intrusion Prevention System)**
- Monitors AND blocks threats
- Active protection
- Can cause false positives

### Detection Methods

**Signature-Based**
- Matches known attack patterns
- Fast and accurate for known threats
- Can't detect zero-days

**Anomaly-Based**
- Learns normal behavior
- Detects deviations
- Can catch zero-days
- Higher false positives

## VPN (Virtual Private Network)

**Purpose**: Secure tunnel over untrusted network

### Types

**Site-to-Site VPN**
```
Office A ←→ Internet ←→ Office B
```

**Remote Access VPN**
```
Employee laptop ←→ Internet ←→ Corporate Network
```

### VPN Protocols

**IPSec**
- Industry standard
- Strong encryption
- Complex setup

**SSL/TLS (OpenVPN)**
- Uses TLS protocol
- Works over HTTPS (port 443)
- Firewall friendly

**WireGuard**
- Modern, fast
- Simple configuration
- Strong cryptography

## Common Attacks & Defenses

### ARP Spoofing
**Attack**: Fake ARP responses redirect traffic
**Defense**: Dynamic ARP Inspection (DAI)

### VLAN Hopping
**Attack**: Access unauthorized VLANs
**Defense**: Disable auto-negotiation, secure trunk ports

### MAC Flooding
**Attack**: Overflow switch MAC table
**Defense**: Port security, limit MAC addresses per port

### DoS/DDoS
**Attack**: Overwhelm resources
**Defense**: Rate limiting, traffic filtering, DDoS mitigation services

## Best Practices

### Network Design
1. **Principle of Least Privilege** - Minimal necessary access
2. **Defense in Depth** - Multiple security layers
3. **Network Segmentation** - Isolate critical assets
4. **Zero Trust** - Never trust, always verify

### Configuration
1. **Change default passwords**
2. **Disable unused services**
3. **Keep firmware updated**
4. **Use strong encryption**
5. **Enable logging**

### Monitoring
1. **Log everything**
2. **Monitor for anomalies**
3. **Regular security audits**
4. **Penetration testing**

## Security Checklist

```bash
# Firewall
☑ Default deny policy
☑ Only necessary ports open
☑ Rules reviewed regularly

# Switching
☑ Port security enabled
☑ VLAN segmentation
☑ STP security (BPDU guard)

# Routing
☑ ACLs configured
☑ Disable unused interfaces
☑ Secure routing protocols

# Monitoring
☑ IDS/IPS deployed
☑ Logs collected centrally
☑ Alerts configured
```

## Key Takeaways

- Firewalls are first line of defense
- NAT provides security through obscurity
- Port security prevents unauthorized access
- Network segmentation limits blast radius
- Defense in depth is essential
- Always monitor and log

Security is not a one-time setup - it's an ongoing process!
"""
        }
    }
    
    for order, data in lessons_content.items():
        if update_lesson_content(db, "Networking Fundamentals", order, data["content"]):
            print(f"  ✅ Updated lesson {order}")
        else:
            print(f"  ❌ Failed to update lesson {order}")
    
    print("✅ Networking Fundamentals lessons 5-6 completed")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        complete_networking_module(db)
    finally:
        db.close()
