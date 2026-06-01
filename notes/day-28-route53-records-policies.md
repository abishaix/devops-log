# Day 28 — Route 53: Records, Hosted Zones, and Routing Policies
**Date:** May 20, 2026

---

## 📚 Concepts Covered
- Route 53 hosted zones — public vs private
- DNS record types — A, AAAA, Alias, CNAME
- Subdomains — no registration needed
- NS records — how domain authentication works
- 5 routing policies — Simple, Latency, Failover, Geolocation, Weighted
- Health checks — role in Failover and Latency policies
- High availability across AZ and region with Route 53 + Load Balancer


## Contents

- [📚 Concepts Covered](#concepts-covered)
- [🧠 Theory Notes](#theory-notes)
  - [Route 53 — Three Core Concepts](#route-53-three-core-concepts)
  - [Hosted Zones](#hosted-zones)
  - [DNS Record Types](#dns-record-types)
  - [Subdomains](#subdomains)
  - [Routing Policies](#routing-policies)
  - [Health Checks](#health-checks)
- [📊 Quick Reference Tables](#quick-reference-tables)
  - [Record type selection guide](#record-type-selection-guide)
  - [Routing policy selection guide](#routing-policy-selection-guide)
  - [Policy comparison](#policy-comparison)
- [🏗️ Architecture / Diagrams](#architecture-diagrams)
- [❓ Questions I Still Have](#questions-i-still-have)
- [🔗 GitHub](#github)
- [⏭️ Next Steps](#next-steps)

---

---

## 🧠 Theory Notes

### Route 53 — Three Core Concepts

```
Route 53
├── Hosted Zones   — container for DNS records for a domain
├── Records        — the actual mappings (domain → IP or endpoint)
└── Policies       — how traffic is distributed across records
```

---

### Hosted Zones

Route 53 offers two types:

| Type | Purpose | Request origin |
|---|---|---|
| Public Hosted Zone | External-facing traffic | Internet |
| Private Hosted Zone | Internal VPC traffic only | Inside VPC only |

**Public hosted zone setup flow:**

```
  [GoDaddy / Registrar]
         │
         │  1. Create hosted zone in Route 53
         ▼
  [Route 53 Hosted Zone]
         │  2. AWS generates NS records + SOA
         │
         │  3. Copy NS records → paste into GoDaddy
         ▼
  [GoDaddy NS updated]
         │  4. All DNS requests now forwarded to Route 53
         ▼
  [Route 53 resolves]
         │  5. Create A / Alias / CNAME records
         ▼
  [Traffic reaches EC2 / ALB / S3]
```

**NS records** authenticate your domain. SOA handles Route 53's internal cache — you never touch it.

---

### DNS Record Types

| Record | Use case | Example |
|---|---|---|
| **A** | Map domain to IPv4 address | `abishaix.com → 13.233.162.141` |
| **AAAA** | Map domain to IPv6 address | `abishaix.com → 2001:db8::1` |
| **Alias** | Map domain to AWS endpoint | `abishaix.com → ALB DNS URL` |
| **CNAME** | Map domain to another domain | `dev.abishaix.com → abishaix.com` |

```
  Which record do I need?
  ─────────────────────────────────────────────
  Pointing to EC2 IP?          →  A record
  Pointing to ALB / S3 / CF?   →  Alias record
  Pointing to another domain?  →  CNAME record
  Pointing to IPv6?            →  AAAA record
  ─────────────────────────────────────────────
  ⚠️  CNAME cannot be used at root domain apex
      Use Alias there instead
```

**A record** — raw IP. Issue: IP changes on EC2 restart. Fix with Elastic IP.

**Alias record** — AWS manages the IP behind it. Preferred for all AWS endpoints.

**CNAME** — common use: redirect all subdomains to root.
- `dev.flipkart.com` → `flipkart.com`
- `api.flipkart.com` → `flipkart.com`

---

### Subdomains

You only need to purchase the **root domain**. Subdomains are free and unlimited.

```
  abishaix.com              ← purchase this once
  ├── api.abishaix.com      ← free — create record in Route 53
  ├── dev.abishaix.com      ← free — create record in Route 53
  ├── backend.abishaix.com  ← free — create record in Route 53
  └── app.abishaix.com      ← free — create record in Route 53

  Each subdomain can point to a different IP, LB, or endpoint.
  No registration. No extra cost.
```

---

### Routing Policies

Route 53 has 5 routing policies. Default is Simple — all others add conditions.

---

#### 1. Simple Routing Policy
**Default. No conditions. Direct mapping.**

```
  User
   │
   ▼
  abishaix.com
   │
   ▼
  Route 53
   │  no conditions — blindly forwards
   ▼
  EC2 / ALB
```

- 1 server minimum
- No health checks
- Multiple values → client picks randomly

---

#### 2. Latency-Based Routing Policy
**Routes to the region with lowest latency for the user.**

```
  User (Hyderabad)
        │
        ▼
     Route 53
     latency policy
    ╱             ╲
   ╱ low latency   ╲ high latency
  ▼                 ▼
Mumbai LB          US LB
  ✅ selected       ✗ skipped
```

- Minimum 2 servers, 2 regions, 2 load balancers
- LB is region-scoped — one per region required
- Health checks optional but recommended — without them Route 53 sends to a failed region

---

#### 3. Failover Routing Policy
**Primary/secondary. Secondary only activates when primary fails.**

```
  User (Hyderabad)
        │
        ▼
     Route 53
     failover policy
     + health checks
        │
        ├──── Primary (Mumbai LB) ◄── always first
        │          │
        │     health check ✅
        │          │
        │     [normal traffic flows here]
        │
        └──── Secondary (US LB) ◄── activates only on primary failure
                   │
              health check ❌ (primary failed)
                   │
              [Route 53 reroutes here automatically]
```

- Health checks **must** be enabled — this is how Route 53 knows primary failed
- Minimum 2 servers, 2 regions, 2 load balancers

> **Key combination:**
> - AZ failure → Load Balancer handles it (within region)
> - Region failure → Route 53 failover handles it (cross region)
> - Together: high availability at both zone level AND region level ✅

---

#### 4. Geolocation-Based Routing Policy
**Routes or restricts traffic based on user's geographic origin.**

```
  Request origin detected by Route 53 (satellite/IP based)
          │
          ├── India origin?    → Mumbai servers  ✅
          ├── US origin?       → Virginia servers ✅
          ├── Australia?       → Singapore servers ✅
          └── No match?        → default or ❌ blocked

  ⚠️  No geolocation policy set = anyone can access (global default)
  ⚠️  Based on IP geolocation — not pin codes
```

Use cases: IRCTC (India only), compliance apps (EU only), regional content.

---

#### 5. Weighted Routing Policy
**Manual traffic split using priority numbers.**

```
  User
   │
   ▼
  Route 53
  weighted policy
   │
   ├── weight: 70  →  US servers     (70% of requests)
   └── weight: 30  →  Mumbai servers (30% of requests)

  Higher weight = more priority = more traffic
  Completely manual — you control the numbers
```

Use cases: gradual rollout (5% new version, 95% old), A/B testing, regional load balancing.

---

### Health Checks

```
  Route 53 health check flow:
  ─────────────────────────────────────────────
  Route 53 pings endpoint periodically
        │
        ├── Response OK?   → endpoint healthy ✅
        │                    traffic continues
        │
        └── No response?   → endpoint unhealthy ❌
                             Failover: redirect to secondary
                             Latency: skip to next best region

  Without health checks → Route 53 sends to failed region blindly
```

---

## 📊 Quick Reference Tables

### Record type selection guide
| Pointing to | Record type |
|---|---|
| EC2 public IP | A record |
| Application Load Balancer | Alias |
| S3 static website | Alias |
| CloudFront distribution | Alias |
| Another domain name | CNAME |
| IPv6 address | AAAA |

### Routing policy selection guide
| Need | Policy |
|---|---|
| Simple 1:1 mapping | Simple |
| Fastest region for user | Latency |
| Backup if primary fails | Failover |
| Country-based restriction | Geolocation |
| Traffic % split | Weighted |

### Policy comparison
| Policy | Condition | Min servers | Health checks |
|---|---|---|---|
| Simple | None | 1 | Not supported |
| Latency | Lowest latency wins | 2 (2 regions) | Optional |
| Failover | Primary/secondary | 2 (2 regions) | Required |
| Geolocation | User country/region | 1+ | Optional |
| Weighted | Manual weight numbers | 2+ | Optional |

---

## 🏗️ Architecture / Diagrams

![Route 53 routing policies architecture](../diagrams/day-28-route53-records-policies.svg)

---

## ❓ Questions I Still Have
- Can I enable health checks on a latency-based routing policy? (yes — explore and confirm)
- Can I combine geolocation + weighted policies on the same domain?
- What is TTL and how does it affect record propagation speed?
- How does WAF complement geolocation for blocking?

---

## 🔗 GitHub
[devops-log](https://github.com/abishaix/devops-log)

---

## ⏭️ Next Steps
- Practice: create ALB, map domain to ALB via Alias record
- Practice: test geolocation policy — restrict to one country
- Coming up: Route 53 practicals — all 5 policies hands-on
