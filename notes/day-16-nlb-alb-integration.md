# Day 16 — Network Load Balancer & NLB+ALB Integration
**Date:** May 5, 2026
**Course:** DevOps Bootcamp

---

## 📚 Concepts Covered

- Network Load Balancer (NLB) — how it works and when to use it
- NLB vs ALB — key differences in protocol, routing, and IP control
- Elastic IPs with NLB — why static IPs matter for security
- ENI (Elastic Network Interface) — intro (deep dive tomorrow)
- NLB + ALB combination architecture — when and why
- Self-learning tasks assigned: LB stickiness, scheduled ASG scaling, ASG lifecycle policy

---

## 🧠 Theory Notes

### Network Load Balancer (NLB)

NLB operates at **Layer 4 (TCP)** — it doesn't inspect HTTP headers, it just routes raw TCP traffic as-is.

| Feature | NLB | ALB |
|---|---|---|
| Protocol | TCP | HTTP/HTTPS |
| Header inspection | ❌ No | ✅ Yes |
| Path-based routing | ❌ No | ✅ Yes |
| Throughput | High | Lower (due to header parsing) |
| Latency | Low | Higher |
| Elastic IP support | ✅ Yes | ❌ No |
| IP control | Static (your own EIP) | Dynamic (AWS-managed, can change) |

**Why NLB is faster:** No header verification. Takes the request, sends it straight to the target. No inspection overhead.

**Why ALB is smarter:** Reads the HTTP header, routes based on path (`/mobile`, `/electronics`, etc.). One ALB can serve multiple applications.

---

### Elastic IPs on NLB — Why It Matters

By default, AWS assigns IPs to load balancers and those IPs can change anytime. With NLB, you can attach your own **Elastic IPs (EIPs)** — static IPs that never change.

**Why this is important:**

```
On-prem / Partner system
    │
    ▼
Egress Firewall
    │ whitelist rules: allow 34.x.x.x, 52.x.x.x (your NLB EIPs)
    ▼
NLB (with fixed Elastic IPs)
    │
    ▼
Target Group / ALB
```

- Firewalls, partner APIs, and on-prem systems can only whitelist **IPs**, not DNS names
- If ALB or default NLB IPs change, those whitelists break and external systems lose access
- With EIPs on NLB, the IPs are permanently yours — whitelists stay valid forever
- DNS-based whitelisting is not supported in most firewall systems — IP only

**NLB with EIP = stable endpoint for firewall rules. No DNS dependency for clients.**

---

### ENI — Elastic Network Interface (Intro)

When you create an NLB across 2 Availability Zones, AWS creates **2 ENIs** — one per AZ. Each ENI carries the IP address for that AZ's NLB endpoint.

- Internal load balancer → private IP per ENI
- Internet-facing load balancer → public IP per ENI (if EIP attached, that's what shows)

Deep dive on ENI tomorrow.

---

### NLB + ALB Combination Architecture

**When to use this:** You need BOTH high throughput + consistent IPs (NLB) AND path-based routing (ALB) in the same stack.

**How it works:**

```
Internet
    │
    ▼
NLB (public subnets, Elastic IPs)
    │ TCP — no header check, high throughput
    ▼
NLB Target Group → points to ALB (not EC2 instances)
    │
    ▼
ALB (private subnets — internal, not internet-facing)
    │ HTTP — reads header, routes by path
    ▼
ALB Target Groups → EC2 instances (app servers)
```

**What each layer does:**

| Layer | Role | Subnet |
|---|---|---|
| NLB | Accepts public traffic, provides stable IPs, high throughput | Public |
| ALB | Path-based routing, header inspection | Private |
| EC2 | Serves the actual application | Private |

**Target groups needed:**
1. `TG-NLB` — protocol TCP, target type: ALB (not instance)
2. `TG-ALB` — protocol HTTP, target type: instance (your EC2s)

**When NOT to use this:** Don't add NLB unnecessarily. Only if you need:
- Fixed IPs for whitelisting upstream/downstream systems, OR
- Higher throughput than ALB alone provides

---

### Listeners on NLB

NLB uses **listeners** to control which ports it accepts traffic on. No path-based rules — just port forwarding to a target group.

```
Listener 80  → Target Group
Listener 81  → Same or different Target Group
Listener 82  → ❌ Not created → connection refused
```

If a port isn't in a listener, NLB drops it. No listener = no access. You can add multiple listeners pointing to the same TG if needed.

---

## 📊 Quick Reference — NLB vs ALB

| | NLB | ALB |
|---|---|---|
| OSI Layer | 4 (Transport) | 7 (Application) |
| Protocol | TCP/UDP | HTTP/HTTPS |
| Routing logic | Port only | Port + Path + Header |
| Static IP | ✅ Elastic IP supported | ❌ AWS-managed only |
| Path routing | ❌ | ✅ |
| High throughput | ✅ | ❌ (slower due to header parsing) |
| Use case | Partner integrations, on-prem firewall whitelisting, raw TCP | Web apps, microservices, path-based routing |

---

## 🏗️ Architecture Diagram

```
                    AWS VPC
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  Public Subnets                   Private Subnets        │
│  ┌─────────────────────┐         ┌──────────────────┐   │
│  │                     │         │                  │   │
│  │  NLB                │ ──────► │  ALB (internal)  │   │
│  │  (Elastic IPs)      │  TCP    │                  │   │
│  │  TG: ALB endpoint   │         │  TG: EC2 instances│  │
│  │                     │         │  /mobile → TG1   │   │
│  └─────────────────────┘         │  /electronics    │   │
│           ▲                      │     → TG2        │   │
│           │                      └──────────────────┘   │
└───────────│──────────────────────────────────────────────┘
            │
    Egress Firewall
    (whitelist NLB EIPs)
            │
    On-prem / Partner
```

---

## ✅ Self-Learning Tasks (Assigned Today)

1. **LB Stickiness** — what is it, how to configure it on ALB
2. **Scheduled-based Auto Scaling** — configure ASG to create servers at 10 AM, delete at 11 AM (time-based, static scaling)
3. **ASG Lifecycle Policy** — default warm-up is 300 seconds; how to extend it when your app takes longer than 5 min to start
4. **NLB + ALB Integration** — practice end-to-end: NLB in public subnets, ALB in private subnets, EC2 as final target

---

## ❓ Questions I Still Have

- ENI deep dive — tomorrow's topic: how to assign a specific private IP to a server
- Can you use the same EIP across multiple NLBs? (Probably not — EIP is 1:1)
- What happens to NLB EIPs when you delete the load balancer? (They go back to your account, not released)

---

## 🔗 GitHub

Commit to `devops-log`:
```
docs: add day 16 notes - NLB, ALB, NLB+ALB integration architecture
```

---

## ⏭️ Next Steps

- ENI (Elastic Network Interface) — deep dive
- Assigning static private IPs to EC2 instances
- Complete the 4 self-learning tasks above
