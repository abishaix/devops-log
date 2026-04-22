# Lab 2 — Custom VPC + EC2 Setup
**Date:** April 20, 2026
**Course:** DevOps Bootcamp
**Instructor:** Mr. Veerababu

---

## 🏗️ What I Built

A custom VPC from scratch with one public subnet and one private subnet inside a single Availability Zone, connected to the internet via an Internet Gateway and Route Table, with an EC2 instance running in the public subnet secured by a Security Group.

---

## 📋 Resources Created

| Resource | Value |
|---|---|
| VPC | CIDR: `10.0.0.0/16` |
| Subnet 1 | Public — `10.0.0.0/24`, AZ-1 |
| Subnet 2 | Private — `10.0.1.0/24`, AZ-1 |
| Internet Gateway | Attached to VPC |
| Route Table | `0.0.0.0/0 → IGW`, associated to Subnet 1 |
| Security Group | SSH port 22, source `0.0.0.0/0` |
| EC2 Instance | Amazon Linux 2, public subnet, public IP enabled |
| Key Pair | RSA, `.pem` format |
| AWS Region | *(fill in your region, e.g. us-east-1)* |

---

## 🗺️ Architecture

```
Developer (outside AWS)
    │ SSH via internet
    ▼
Internet Gateway
    │ attached to VPC
    ▼
Route Table (0.0.0.0/0 → IGW)
    │ associated with public subnet only
    ▼
┌────────────────────────────────────────────────┐
│  VPC — 10.0.0.0/16                             │
│                                                │
│  ┌─────────────────┐   ┌─────────────────────┐ │
│  │  Public Subnet  │   │   Private Subnet    │ │
│  │  10.0.0.0/24    │   │   10.0.1.0/24       │ │
│  │                 │   │                     │ │
│  │  EC2 Instance   │   │   EC2 Instance      │ │
│  │  Public + Priv  │   │   Private IP only   │ │
│  │  IP  [SG: 22]   │   │   [SG]  no route    │ │
│  └─────────────────┘   └─────────────────────┘ │
└────────────────────────────────────────────────┘

Developer ──SSH──▶ Public EC2     ✓
Developer ──────✕  Private EC2    (no IGW route)
```

---

## 🔢 Step by Step

### Step 1 — Select Region
- Go to AWS Console → top-right dropdown → select your region
- Always do this first — every resource you create is region-scoped

---

### Step 2 — Create VPC
1. VPC → Your VPCs → **Create VPC**
2. Select **VPC only** (not "VPC and more")
3. CIDR: `10.0.0.0/16`
4. Create VPC

---

### Step 3 — Create Subnets

> Use the VPC filter in the subnet console to see only your VPC — not the default ones.

**Subnet 1 — Public:**
1. Subnets → Create Subnet
2. Select your VPC
3. CIDR: `10.0.0.0/24`
4. Pick an AZ (e.g. `us-east-1a`)

**Subnet 2 — Private:**
1. Create another subnet in the same VPC
2. CIDR: `10.0.1.0/24`
3. Same AZ is fine for this lab

> **Why /24 and not /16?** Giving a subnet the full /16 would allocate all 65,536 VPC IPs to one subnet — nothing left for the second. A /24 gives 256 IPs each (251 usable; AWS reserves 5).

---

### Step 4 — Create Internet Gateway
1. Internet Gateways → **Create Internet Gateway**
2. After creation: **Actions → Attach to VPC** → select your VPC

> IGW attaches at the VPC level — not to a subnet, not to an EC2 instance. One IGW per VPC.

---

### Step 5 — Create Route Table and Add Route
1. Route Tables → **Create Route Table** → attach to your VPC
2. Select the RT → **Routes** tab → **Edit Routes** → **Add Route**
   - Destination: `0.0.0.0/0`
   - Target: your Internet Gateway
3. Save

---

### Step 6 — Associate Route Table with Public Subnet
1. Still in the Route Table → **Subnet Associations** tab
2. **Edit subnet associations** → select **Subnet 1 (public)**
3. Save

> This is the step that makes Subnet 1 public. Subnet 2 has no association — so it stays private. A subnet with no route to an IGW cannot reach the internet regardless of anything else.

---

### Step 7 — Create Security Group
1. Security Groups → **Create Security Group** → select your VPC
2. Inbound rules → Add:
   - Type: SSH | Port: 22 | Source: `0.0.0.0/0`
3. Leave outbound default (allow all)

> SG decides whether a connection is allowed. It does **not** validate the key pair — that happens on the EC2 server itself.

---

### Step 8 — Launch EC2 Instance
1. EC2 → **Launch Instance** → Amazon Linux 2 AMI
2. Instance type: `t2.micro` (free tier)
3. Create new key pair: RSA, `.pem` → download and save
4. Network settings → Edit:
   - VPC: your custom VPC
   - Subnet: Subnet 1 (public)
   - Auto-assign public IP: **Enable**
   - Security group: your SG
5. Launch

---

### Step 9 — Connect via SSH

```bash
# Linux/Mac
ssh -i /path/to/mykey.pem ec2-user@<public-ip>

# Windows
ssh -i "C:\Users\YourName\Documents\mykey.pem" ec2-user@<public-ip>

# Verify you're in
whoami       # expected: ec2-user
hostname     # shows EC2 internal hostname
```

---

## 🔬 Break-It Tasks

These are the most important part of the lab. Each one shows you exactly what controls connectivity.

### Task A — Remove IGW from Route Table
1. Route Table → Routes → **Edit Routes**
2. Delete the `0.0.0.0/0 → IGW` entry (don't delete the IGW itself)
3. Try to SSH

**Expected:** Connection timeout. Packet leaves your machine, enters the VPC, but there's no route to send it out. Traffic drops.

**What it proves:** The route entry in the RT — not the IGW attachment itself — is what controls traffic flow.

4. Re-add the route after testing.

---

### Task B — Remove Subnet from Route Table Association
1. Route Table → Subnet Associations → **Edit**
2. Deselect Subnet 1
3. Try to SSH

**Expected:** Connection timeout again. The RT still has the `0.0.0.0/0 → IGW` route — but Subnet 1 is no longer using that RT. It falls back to the VPC main route table (no IGW route there).

**What it proves:** Both must be true — the RT must have the route AND it must be associated with the subnet.

4. Re-associate after testing.

---

## ❌ Errors Encountered

| Error | Cause | Fix |
|---|---|---|
| `Network error: connection timed out` | Packet never reached the server — routing or SG issue | Check: IGW attached, RT has `0.0.0.0/0 → IGW`, RT associated to subnet, EC2 has public IP |
| `Permission denied (publickey)` | Wrong key or wrong username | Check: correct `.pem` file, username is `ec2-user` not root/ubuntu |
| `WARNING: UNPROTECTED PRIVATE KEY FILE!` | `.pem` permissions too open (Linux/Mac) | Run `chmod 400 mykey.pem` then retry |

*(Add your own errors here as you hit them)*

---

## 🧹 Cleanup Checklist

Delete in this order — dependencies go bottom to top:

- [ ] 1. Terminate EC2 instance (wait for it to fully stop)
- [ ] 2. Delete Security Group
- [ ] 3. Disassociate subnets from Route Table, then delete Route Table
- [ ] 4. Detach Internet Gateway from VPC, then delete IGW
- [ ] 5. Delete Subnets
- [ ] 6. Delete VPC
- [ ] 7. Delete Key Pair (EC2 console → Key Pairs)

---

## 💰 Approximate Cost

| Resource | Cost |
|---|---|
| EC2 t2.micro | Free tier (750 hrs/month) |
| VPC, Subnets, SG, RT | Free |
| Internet Gateway | Free (data transfer costs apply at scale) |
| Key Pair | Free |

**Total for this lab: $0** (within free tier)

---

## ⏭️ Next Practice

- Rebuild from scratch with no notes — just the architecture diagram
- Launch an EC2 in the private subnet — confirm it gets no public IP
- Enable public IP on a private subnet EC2 — confirm SSH still fails (no IGW route)
