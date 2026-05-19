# Practice Log — VPC + EC2 Setup with IGW and Route Table
**Date:** April 2026
**Resources Created:** VPC, 2 Subnets, IGW, Route Table, Security Group, EC2
**Region:** ap-south-1 (Mumbai)

---

## What I Built

A working public subnet with an EC2 instance accessible from the internet via EC2 Instance Connect. Full network stack built from scratch — VPC → Subnet → IGW → Route Table → Security Group → EC2.

```
VPC (10.0.0.0/16)
├── subnet-public  (10.0.0.0/24)  ← IGW connected
│   └── EC2: practice-server (t2.micro, Amazon Linux 2023)
│       Public IP:  13.233.149.241
│       Private IP: 10.0.0.193
└── subnet-private (10.0.1.0/24)  ← no internet
```

---

## Step by Step

**1. Create VPC**
- Name: `practice-vpc`
- CIDR: `10.0.0.0/16`

**2. Create Subnets**
- `subnet-public` → CIDR: `10.0.0.0/24` → AZ: ap-south-1a
- `subnet-private` → CIDR: `10.0.1.0/24` → AZ: ap-south-1a

**3. Create Internet Gateway**
- Name: `practice-igw`
- Action: Attach to `practice-vpc`

**4. Create Route Table**
- Name: `practice-rt-public`
- Add route: `0.0.0.0/0` → `practice-igw`
- Associate with: `subnet-public`

**5. Create Security Group**
- Name: `practice-sg`
- Inbound rules:
  - HTTP (80) → `0.0.0.0/0`
  - HTTPS (443) → `0.0.0.0/0`
  - SSH (22) → `0.0.0.0/0` ← practice only, not for production

**6. Launch EC2**
- Name: `practice-server`
- AMI: Amazon Linux 2023
- Instance type: `t2.micro` (free tier)
- Network: `practice-vpc` → `subnet-public`
- Security Group: `practice-sg`
- Key Pair: created and downloaded `.pem`

**7. Connect via EC2 Instance Connect**
- Go to EC2 → select instance → Connect → EC2 Instance Connect → Connect

---

## Terminal Output

| Command | Output | What It Means |
|---------|--------|---------------|
| `whoami` | `ec2-user` | Default user on Amazon Linux |
| `curl ifconfig.me` | `13.233.149.241` | Server's public IP — internet-facing |
| `ip addr` | `10.0.0.193/24` | Server's private IP — inside VPC subnet |

---

## Screenshots
- 📸 VPC created — `10.0.0.0/16`, state: Available
- 📸 Two subnets — `subnet-public` and `subnet-private`
- 📸 Security Group inbound rules — SSH, HTTP, HTTPS
- 📸 IGW created and attached to `practice-vpc` — state: Attached
- 📸 Route Table — Routes tab: `10.0.0.0/16 local` + `0.0.0.0/0 → IGW`
- 📸 Route Table — Subnet Associations: `subnet-public` associated
- 📸 EC2 instance — Running state with public IP assigned
- 📸 EC2 Instance Connect — terminal showing `whoami`, `curl ifconfig.me`, `ip addr`

---

## Troubleshooting

**Problem:** EC2 Instance Connect failed — `"Error establishing SSH connection"`

**Steps checked:**
1. ✅ Instance has public IP assigned
2. ✅ Route Table associated to `subnet-public`
3. ✅ `0.0.0.0/0 → IGW` route exists
4. ❌ SSH rule was restricted to `My IP (31.223.91.134/32)` — **this was the issue**

**Root cause:** EC2 Instance Connect doesn't use your personal IP. AWS uses its own IP range (`13.233.177.x`) to create the SSH tunnel in the browser. Restricting SSH to My IP blocked AWS's service.

**Fix:** Changed SSH source from `My IP` → `0.0.0.0/0`

**Lesson learned:**
- EC2 Instance Connect ≠ direct SSH from your laptop
- For practice → SSH open to `0.0.0.0/0` is fine
- For production → use bastion host or AWS Systems Manager Session Manager

---

## Cleanup — Deletion Order

| Step | Action |
|------|--------|
| 1 | Terminate EC2 `practice-server` → wait for **Terminated** state |
| 2 | Delete Security Group `practice-sg` |
| 3 | Detach IGW `practice-igw` from VPC → then delete it |
| 4 | Delete Route Table `practice-rt-public` |
| 5 | Delete subnets — `subnet-public` and `subnet-private` |
| 6 | Delete VPC `practice-vpc` |

✅ All resources deleted. No running instances. No unexpected charges.

> VPC always goes last. If you try to delete VPC before removing dependencies, AWS throws an error.

---

## Billing Protection
- Zero Spend Budget → alert at $0.01
- Monthly Budget → $5/month cap with email alert
- Free Tier alerts enabled

---

## Cost
~$0.00 — all resources within AWS Free Tier. t2.micro + short session.
