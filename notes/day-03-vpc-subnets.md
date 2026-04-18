# Day 3 — VPC, Subnets & Cloud Types
**Date:** April 9, 2026
**Course:** DevOps with Multicloud — Mr. Veerababu

---

## 📚 Concepts Covered
- What is a VPC
- Subnets and how they relate to AZs
- Public vs Private Cloud
- Full picture: Region → AZ → VPC → Subnet

---

## 🧠 Theory Notes

### VPC — Virtual Private Cloud
- VPC = a **private network layer** you create inside the public cloud
- Think of it as renting space in AWS's apartment building and building your own private apartment inside it
- VPC operates at the **Region level** → select region, then create VPC
- VPC is the **main network** — everything else lives inside it

> Before you create any server → you need a VPC.

### Subnets
- Subnets = **divisions of your VPC**
- A subnet is a smaller network carved out of the VPC
- Subnets operate at the **Availability Zone level** (one subnet = one AZ)
- Multiple subnets can exist in one VPC, spread across different AZs

### Public Cloud vs Private Cloud

| | Public Cloud | Private Cloud |
|--|-------------|---------------|
| **What** | Shared infrastructure (AWS, Azure, GCP) | Dedicated to one org only |
| **Access** | Over the internet | Internal network or hosted |
| **You own** | Nothing — you rent | The hardware or the hosted env |
| **Example** | AWS EC2 instance | Company's internal data center |
| **Cost** | Pay as you go | High upfront cost |

> VPC inside AWS = **private cloud inside public cloud**. You get isolation without owning hardware.

---

## 📊 How Everything Fits Together

```
Region (e.g. eu-west-1 Europe)
│
├── VPC (your private network — spans the whole region)
│
├── AZ1 (Data Center A)
│   ├── Public Subnet   ← open to internet
│   └── Private Subnet  ← internal only
│
└── AZ2 (Data Center B)
    ├── Public Subnet
    └── Private Subnet
```

### The Analogy

| Cloud Concept | Real Life |
|--------------|-----------|
| Region | City |
| Availability Zone | Building in that city |
| VPC | Your private property |
| Subnet | Rooms in your house |
| Public Subnet | Front door — open to the world |
| Private Subnet | Locked room — internal only |

---

## ❓ Questions to Follow Up
- How many VPCs can you create per region?
- What's the CIDR range for a VPC? (comes in Day 5)
- Can one subnet span multiple AZs?

---

## ⏭️ Next Steps
- Day 4: Security Groups, Ports, Firewall rules
