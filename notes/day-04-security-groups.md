# Day 4 — Security Groups, Ports & Firewall Rules
**Date:** April 10, 2026
**Course:** DevOps with Multicloud — Mr. Veerababu

---

## 📚 Concepts Covered
- What is a Security Group (firewall in AWS)
- Inbound vs Outbound rules
- Ports — what they are and why they matter
- Default SG behavior
- SSH and RDP access

---

## 🧠 Theory Notes

### Security Group (SG)
- SG = **firewall** in AWS
- Works at the **server (EC2 instance) level**
- Allows only authorized requests, blocks everything else
- Every EC2 instance must have a Security Group

### Rules — What You Define in a SG

Each rule contains:

| Field | Meaning |
|-------|---------|
| **Source** | Where the request is coming from (IP address) |
| **Protocol** | How data travels (TCP, UDP, HTTP, HTTPS, SSH…) |
| **Port** | Which logical endpoint on the server to allow |
| **Destination** | Where traffic is going |

### Inbound vs Outbound

| | Inbound | Outbound |
|--|---------|----------|
| Direction | Traffic **towards** the server | Traffic **away from** the server |
| Default | **DENY ALL** | **ALLOW ALL** |
| Why | Entry is critical to control | Exit is less risky |

> By default: everything trying to reach your server is blocked. You explicitly open what you need.

### Ports — Why They Matter

A server has one IP but can run **multiple applications** — each on a different port.

```
Server IP: 174.1.2.3
├── Port 3000 → Flipkart app
├── Port 5000 → IRCTC app
└── Port 6000 → Amazon app
```

- Total port range: **0 to 65,535**
- You can't assign the same port to two apps on the same server

### Common Ports to Know

| Port | Protocol | Use |
|------|----------|-----|
| **22** | SSH | Login to Linux server |
| **3389** | RDP | Login to Windows server |
| **80** | HTTP | Web traffic (unencrypted) |
| **443** | HTTPS | Web traffic (encrypted) |

### SG Rule Examples

| Rule | What It Does |
|------|-------------|
| `0.0.0.0/0` on port 80 | Allow HTTP from anyone |
| `63.2.34.5/32` on port 22 | Allow SSH from one specific IP only |
| `0.0.0.0/0` on all ports | Open everything (never do this in prod) |

> `/32` = a single specific IP address. Append this when you only want one machine to access.

### Security Best Practice
- Port 22 (SSH) should **never** be open to all (`0.0.0.0/0`)
- Only whitelist your specific IP for SSH access
- Developers get port 22 access only — not every port

---

## 💻 Commands (Preview)
```bash
# Start nginx web server (runs on port 80 by default)
systemctl start nginx

# Check which ports are listening
ss -tuln
```

---

## 📊 HTTP vs HTTPS

| | HTTP | HTTPS |
|--|------|-------|
| Port | 80 | 443 |
| Data | Plain text — visible to anyone | Encrypted |
| Use | Dev/testing | Production always |

---

## ❓ Questions to Follow Up
- What's the difference between a Security Group and a NACL (Network ACL)?
- Can you attach multiple security groups to one EC2?
- What happens when you have conflicting rules?

---

## ⏭️ Next Steps
- Day 5: TCP/UDP protocols, CIDR, VPC sizing, subnets
