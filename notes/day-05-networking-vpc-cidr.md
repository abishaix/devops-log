# Day 5 — Networking Basics, VPC & CIDR
**Date:** April 11, 2026
**Course:** DevOps with Multicloud — Mr. Veerababu

---

## 📚 Concepts Covered
- What a client needs to connect to a server
- TCP vs UDP protocols
- VPC — Virtual Private Cloud
- CIDR — how to calculate IP ranges and usable IPs
- Private IP address series
- Subnet sizing and design
- AWS reserved IPs per subnet
- VPC limits per region

---

## 🧠 Theory Notes

### Client → Server Connection
For any client to connect to a server, 4 things are required:

| Required | What It Is |
|----------|-----------|
| **Internet** | Basic connectivity |
| **IP** | Address of the server |
| **Protocol** | Rules for communication (HTTP, HTTPS, SSH…) |
| **Connection** | TCP or UDP — how the data actually moves |

### TCP vs UDP

| | TCP | UDP |
|--|-----|-----|
| Connection | Establishes connection first | No connection — just sends |
| Data Loss | None — verifies every packet | Possible — no verification |
| Use Case | HTTP/HTTPS, SSH | Video streaming, DNS, gaming |
| Analogy | Registered mail — signature required | Dropping flyers — no confirmation |

#### How TCP Works
1. Client sends **connection request** → Server
2. Server **accepts** → handshake complete
3. HTTP/HTTPS data flows inside that established connection

> TCP does the handshake first → once connected → HTTP/HTTPS transfers data inside that tunnel.

---

### VPC — Virtual Private Cloud
- VPC = logical network layer you create inside the cloud
- **Before creating any server → create VPC first**
- Inside VPC → create subnets → inside subnets → create EC2s
- VPC operates at **region level**
- Max **5 VPCs per region** (soft limit — can request increase from AWS)

### Private IP Series (always use for VPC)

| Series | Use |
|--------|-----|
| `10.x.x.x` | Private networks |
| `172.x.x.x` | Private networks |
| `192.x.x.x` | Private networks |

> Everything else = public IPs. Never use public series for VPC CIDR.

---

### CIDR — Classless Inter-Domain Routing
CIDR defines the **size** of a network — how many IPs it contains.

**Format:** `10.0.0.0/24`
- `10.0.0.0` = base network address
- `/24` = netmask — determines total IPs

#### CIDR Math
```
Formula: 2^(32 - netmask) = total IPs
Usable IPs = total IPs - 5  (AWS reserves 5 per subnet)
```

| CIDR | Math | Total IPs | Usable IPs |
|------|------|-----------|------------|
| `/16` | 2^16 | 65,536 | 65,531 |
| `/24` | 2^8 | 256 | **251** |
| `/23` | 2^9 | 512 | 507 |
| `/26` | 2^6 | 64 | 59 |
| `/28` | 2^4 | 16 | 11 |

#### Power of 2 Reference
| Exponent | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|----------|---|---|---|---|---|---|---|---|---|---|---|
| Value | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 |

---

### AWS Reserved IPs — Every Subnet Loses 5

| IP | Reserved For |
|----|-------------|
| `.0` | Network address |
| `.1` | VPC router |
| `.2` | DNS server |
| `.3` | Future use (AWS) |
| `.255` | Broadcast address |

> /24 = 256 total → **251 usable**. Always subtract 5 from your calculation.

---

### Subnet Sizing

| Split | Subnets | IPs Each |
|-------|---------|----------|
| 2 × /25 | `.0–.127` and `.128–.255` | 128 |
| 4 × /26 | 4 subnets | 64 |
| 8 × /27 | 8 subnets | 32 |

#### Subnet CIDR Rule
Subnet CIDR must always be **within** the VPC CIDR:

| VPC CIDR | Valid | Invalid |
|----------|-------|---------|
| `10.0.0.0/24` | `10.0.0.0/26` ✅ | `10.0.0.0/23` ❌ larger than VPC |
| `10.0.0.0/24` | `10.0.0.0/24` ✅ | `11.0.0.0/24` ❌ different series |

> Subnets in the same VPC talk to each other automatically via the **local route** — no extra config needed.

---

## 📊 Best Practice VPC Design

```
VPC:      10.0.0.0/16   (65,536 IPs — room to grow)
Subnet1:  10.0.0.0/24   (AZ1 public)   ← series 0
Subnet2:  10.0.1.0/24   (AZ1 private)  ← series 1
Subnet3:  10.0.2.0/24   (AZ2 public)   ← series 2
Subnet4:  10.0.3.0/24   (AZ2 private)  ← series 3
```

> Increment the third octet by 1 for each subnet — clean, no overlap.

---

## ✅ What I Practiced

- Created VPC: `10.0.0.0/16`
- Created `subnet-public`: `10.0.0.0/24` → 251 usable IPs
- Created `subnet-private`: `10.0.1.0/24` → 251 usable IPs
- Created Security Group:
  - HTTP (80) → `0.0.0.0/0`
  - HTTPS (443) → `0.0.0.0/0`
  - SSH (22) → my IP only

---

## 📸 Screenshots
- 📸 VPC created — `10.0.0.0/16`, state: Available
- 📸 Two subnets — `subnet-public` and `subnet-private`
- 📸 Security Group inbound rules — SSH, HTTP, HTTPS

---

## ❓ Questions I Still Have
- Why 5 VPCs per region limit? → AWS soft limit, requestable
- When do you use /23 or /22 vs /24 in production?
- How does multi-AZ subnet design improve availability?

---

## 🔗 Tool
Subnet CIDR Calculator: https://www.davidc.net/sites/default/subnets/subnets.html

---

## ⏭️ Next Steps
- Day 6: EC2, IGW, Route Table, SSH, EC2 Instance Connect
