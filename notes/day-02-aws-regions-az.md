# Day 2 — AWS Global Infrastructure: Regions & Availability Zones
**Date:** April 8, 2026
**Course:** DevOps with Multicloud — Mr. Veerababu

---

## 📚 Concepts Covered
- AWS global infrastructure hierarchy
- Regions and Availability Zones
- Where DevOps engineers operate vs. what AWS manages
- EC2 introduction

---

## 🧠 Theory Notes

### AWS Infrastructure Hierarchy

```
Global Layer (AWS manages this — not your concern)
└── Continent
    └── Region  ← Your responsibility starts here
        └── Availability Zone (AZ)  ← And here
            └── EC2 Instance (your server)
```

> You don't create regions. You don't create AZs. AWS already built those. Your job is to **select** where to deploy.

### Regions
- A **region** is a geographic location — not a country, a geolocation
- One country can have multiple regions (India has 2: Mumbai + Hyderabad)
- AWS has **33+ regions** worldwide
- When you create any resource → first step is always **select region**

### Availability Zones (AZ)
- AZ = **data center** (one or more physical buildings)
- Each region contains **multiple AZs** (usually 3)
- AWS has **108+ AZs** globally
- AZs within a region are physically separate but connected with low latency

```
Region (e.g. ap-south-1 Mumbai)
├── AZ1 (ap-south-1a)
├── AZ2 (ap-south-1b)
└── AZ3 (ap-south-1c)
```

### Your Job When Creating a Server

1. Select **Region**
2. Select **Availability Zone**
3. AWS handles the rest (physical hardware, power, cooling, networking at data center level)

---

## 📊 Quick Reference

| Term | What It Is | Who Manages It |
|------|-----------|----------------|
| Global Layer | Worldwide backbone | AWS |
| Continent | Geographic grouping | AWS |
| Region | Geolocation (e.g. Mumbai) | AWS creates, **you select** |
| Availability Zone | Data center cluster | AWS creates, **you select** |
| EC2 Instance | Your server | **You** |

---

## 💻 Key Terms Introduced
- **EC2** = Elastic Cloud Compute = Server = Instance (all same thing)
- **Region** = group of Availability Zones
- **AZ** = data center(s)

---

## ❓ Questions to Follow Up
- What happens if one AZ goes down — does my app stay up?
- How do I choose which region to deploy in?
- What's the latency difference between AZs in the same region?

---

## ⏭️ Next Steps
- Day 3: VPC — Virtual Private Cloud, Subnets, Public vs Private Cloud
