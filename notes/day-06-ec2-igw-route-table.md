# Day 6 — EC2, Internet Gateway, Route Tables & Public Subnet
**Date:** April 14, 2026 (Friday)
**Course:** DevOps with Multicloud — Mr. Veerababu

---

## 📚 Concepts Covered
- CIDR continued — multi-series ranges
- EC2 components (AMI, instance type, EBS, networking, key pair)
- Private IP vs Public IP
- Internet Gateway (IGW)
- Route Table
- What actually makes a subnet public vs private
- Bastion host pattern
- EC2 Instance Connect (browser SSH)

---

## 🧠 Theory Notes

### CIDR — Multi-Series Ranges
When netmask goes below /24, the IP range **spills across multiple series**:

```
10.0.0.0/23 = 512 IPs
├── 10.0.0.0 → 10.0.0.255  (series 0)
└── 10.0.1.0 → 10.0.1.255  (series 1)

10.0.0.0/22 = 1024 IPs
├── 10.0.0.0 → 10.0.0.255  (series 0)
├── 10.0.1.0 → 10.0.1.255  (series 1)
├── 10.0.2.0 → 10.0.2.255  (series 2)
└── 10.0.3.0 → 10.0.3.255  (series 3)
```

> Best practice: use /16 for VPC, /24 for each subnet. Increment third octet per subnet. No overlap, easy to reason about.

---

### EC2 — Components When Creating a Server

| Component | AWS Name | What It Is |
|-----------|----------|-----------|
| Operating System | AMI (Amazon Machine Image) | OS + pre-installed software template |
| CPU + RAM | Instance Type | e.g. `t2.micro`, `t3.medium` |
| Hard Disk | EBS (Elastic Block Storage) | Persistent disk attached to instance |
| Network | VPC + Subnet + Security Group | Where the server lives, what can reach it |
| Login Auth | Key Pair | Public key on server / private key on laptop |

#### Key Pair — How It Works
- You generate a key pair during EC2 creation
- **Public key** → stored on the server
- **Private key (.pem)** → downloaded to your laptop
- Use private key to SSH in: `ssh -i key.pem ec2-user@<public-ip>`

> Never lose your `.pem` file. No recovery — you'd need to create a new instance.

---

### Private IP vs Public IP

| | Private IP | Public IP |
|--|-----------|-----------|
| Used for | Communication inside VPC | Communication from internet |
| Visible to | Only resources in VPC | Anyone on internet |
| Example | `10.0.0.193` | `13.233.149.241` |
| Analogy | Room number inside a building | Street address of the building |

---

### Internet Gateway (IGW)
- IGW = the door that gives your VPC internet access
- Must be **created and attached to VPC** manually
- Attaching IGW to VPC alone is **not enough** — traffic won't flow yet
- You also need a Route Table to direct traffic through it

---

### Route Table (RT)
- Route Table = traffic director between IGW and subnets
- Two key routes in every public subnet's RT:

| Destination | Target | Meaning |
|-------------|--------|---------|
| `10.0.0.0/16` | local | Traffic inside VPC stays inside VPC |
| `0.0.0.0/0` | IGW | Everything else → go to internet via IGW |

---

### Public vs Private Subnet
> There is **no checkbox** in AWS for public or private. The only difference is the Route Table.

| | Public Subnet | Private Subnet |
|--|--------------|----------------|
| IGW route? | ✅ `0.0.0.0/0 → IGW` | ❌ No IGW route |
| Internet access | Yes | No |
| Use case | Bastion hosts, load balancers | App servers, databases |

---

### Steps to Create a Public Subnet

```
1. Create VPC (CIDR: 10.0.0.0/16)
2. Create subnets inside VPC (default = private)
3. Create IGW → attach to VPC
4. Create Route Table inside VPC
5. Add route: 0.0.0.0/0 → IGW
6. Associate Route Table with public subnet
   → subnet is now public ✅
```

---

### Bastion Host Pattern

```
Developer (internet)
       ↓  SSH
  Public EC2 (bastion host)
       ↓  SSH
  Private EC2 (app server)
```

- Apps always live in **private subnets** — not directly exposed
- Public server = jump server — only purpose is to relay access
- Public and private can talk to each other because they're in the **same VPC** (local route)

---

## 🏗️ Architecture

```
Region
└── VPC (10.0.0.0/16)
    ├── Internet Gateway (practice-igw)
    │       │
    │   Route Table (practice-rt-public)
    │   0.0.0.0/0 → IGW
    │       │
    ├── subnet-public (10.0.0.0/24)  ← RT associated here
    │   └── EC2: practice-server (t2.micro, Amazon Linux 2023)
    │       Public IP:  13.233.149.241
    │       Private IP: 10.0.0.193
    │
    └── subnet-private (10.0.1.0/24)  ← no IGW route
```

---

## ✅ What I Built — Day 6

| Resource | Name | Config |
|----------|------|--------|
| VPC | `practice-vpc` | `10.0.0.0/16` |
| Subnet public | `subnet-public` | `10.0.0.0/24`, AZ1 |
| Subnet private | `subnet-private` | `10.0.1.0/24`, AZ1 |
| Internet Gateway | `practice-igw` | Attached to `practice-vpc` |
| Route Table | `practice-rt-public` | `0.0.0.0/0 → IGW`, associated to `subnet-public` |
| Security Group | `practice-sg` | HTTP(80), HTTPS(443) open / SSH(22) open |
| EC2 | `practice-server` | `t2.micro`, Amazon Linux 2023, `subnet-public` |

---

## 💻 Terminal Output — Confirmed Working

Connected via EC2 Instance Connect (browser SSH):

| Command | Output | What It Means |
|---------|--------|---------------|
| `whoami` | `ec2-user` | Default user on Amazon Linux |
| `curl ifconfig.me` | `13.233.149.241` | Server's public IP — internet-facing |
| `ip addr` | `10.0.0.193/24` | Server's private IP — inside VPC subnet |

---

## ❌ Mistakes & Fixes

### EC2 Instance Connect Failed
**Error:** `"Failed to connect to your instance. Error establishing SSH connection"`

**Troubleshooting steps:**
1. ✅ Instance has public IP? → Yes
2. ✅ Route Table associated to subnet-public? → Yes
3. ✅ `0.0.0.0/0 → IGW` route exists? → Yes
4. ❌ Security Group SSH rule → **Found the issue**

**Root cause:**
SSH was set to `My IP (31.223.91.134/32)` — but EC2 Instance Connect doesn't use your personal IP. AWS uses **its own IP range** (`13.233.177.x`) to create the SSH tunnel in the browser. My IP rule blocked AWS's service IP.

**Fix:** Changed SSH source from `My IP` → `0.0.0.0/0`

**Result:** Connected successfully ✅

---

### Key Lesson — EC2 Instance Connect vs Direct SSH

| | EC2 Instance Connect | Direct SSH from laptop |
|--|---------------------|----------------------|
| Who connects | AWS's service IP range | Your personal IP |
| SG rule needed | `0.0.0.0/0` on port 22 | Your IP `/32` on port 22 |
| For practice | ✅ Use this | Fine for personal projects |
| For production | ❌ Don't open SSH to all | Use bastion host or AWS SSM |

---

## 💰 Billing Protection Setup
- Zero Spend Budget → alert when spending exceeds $0.01
- Monthly Budget → $5/month cap with email alert
- Free Tier alerts enabled in billing preferences

> Set this up on Day 1 of any AWS account. Prevents surprise bills.

---

## 📸 Screenshots
- 📸 IGW created and attached to `practice-vpc` — state: Attached
- 📸 Route Table — Routes tab: `10.0.0.0/16 local` + `0.0.0.0/0 → IGW`
- 📸 Route Table — Subnet Associations tab: `subnet-public` associated
- 📸 Security Group inbound rules — HTTP, HTTPS, SSH
- 📸 EC2 instance — Running state with public IP assigned
- 📸 EC2 Instance Connect — terminal showing `whoami`, `curl ifconfig.me`, `ip addr` output
- 📸 Billing — Zero Spend and Monthly budget created

---

## 🗑️ Cleanup — Deletion Order

> Always delete in this order — dependencies first, VPC last.

| Step | Action |
|------|--------|
| 1 | Terminate EC2 `practice-server` → wait for **Terminated** state |
| 2 | Delete Security Group `practice-sg` |
| 3 | **Detach** IGW `practice-igw` from VPC → then delete it |
| 4 | Delete Route Table `practice-rt-public` |
| 5 | Delete subnets — `subnet-public` and `subnet-private` |
| 6 | Delete VPC `practice-vpc` |

> ✅ All resources deleted. No running instances. No leftover charges.

> If you delete VPC before detaching IGW or deleting subnets → AWS throws an error. VPC always goes last.

---

## ❓ Questions I Still Have
- How does traffic reach a private subnet from outside? → It doesn't. That's the point.
- Can two instances in the same subnet ping each other?
- What is NAT Gateway — how do private subnets get internet for software updates?
- When do you use AWS SSM Session Manager instead of bastion host?

---

## ⏭️ Next Steps
- Push Day 5 + Day 6 notes and practice logs to GitHub
- Next practice: add a second EC2 in private subnet, SSH from public to private
