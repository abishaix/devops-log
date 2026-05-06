# Day 17 — Multi-Path ALB, Target Groups & ENI
**Date:** May 6, 2026

---

## 📚 Concepts Covered

- Single server, multiple application paths — how LB health checks work
- Target group per path — why one TG is not enough for multi-path routing
- LB can send traffic to paths without a TG, but health checks won't cover them
- ENI (Elastic Network Interface) — what it is, lifecycle, use cases
- How to preserve a private IP when replacing a corrupted server

---

## 🧠 Theory Notes

### Single Server, Multiple Paths — Health Check Problem

When you deploy multiple applications on one server at different paths:

```
/usr/share/nginx/html/index.html        ← default path (port 80)
/usr/share/nginx/html/path1/index.html  ← path1 (port 3000)
/usr/share/nginx/html/path2/index.html  ← path2 (port 5000)
```

If you create only **one target group** pointing to the default path:

| Question | Answer |
|---|---|
| Will LB perform health checks for default path? | ✅ Yes |
| Will LB perform health checks for path1? | ❌ No — not in TG |
| Will LB perform health checks for path2? | ❌ No — not in TG |
| Will LB send traffic to path1 if same server? | ✅ Yes — blindly |
| Is this safe? | ❌ No — no health checks = no safety net |

**Key rule:** LB performs health checks based only on what's defined in the TG. TG doesn't perform health checks — it gives the configuration *to* the LB. LB does the actual checking.

**If path1 app is broken but LB has no TG for it, LB will still send traffic there — end users get errors.**

---

### Solution — One TG Per Path

Create a separate TG for each path:

| TG | Port | Path |
|---|---|---|
| TG-1 | 80 | / (default) |
| TG-2 | 3000 | /path1 |
| TG-3 | 5000 | /path2 |

Same server can be registered in all three TGs — port and path are different so LB treats them as separate health check targets.

**ALB rules:**
- Default → TG-1 (port 80, `/`)
- `/path1` → TG-2 (port 3000, `/path1`)
- `/path2` → TG-3 (port 5000, `/path2`)

**One TG cannot have multiple ports or multiple paths.** One TG = one port + one path.

---

### ENI — Elastic Network Interface

When you launch an EC2 instance, AWS doesn't attach network properties directly to the server — it creates an **ENI** and attaches it to the server. The ENI holds:

- Private IP address
- Security group
- Subnet association

```
EC2 Instance
    └── ENI (attached)
            ├── Private IP
            ├── Security Group
            └── Subnet
```

Think of ENI as the NIC card in a physical server. In Azure, this is called a NIC card — same concept.

---

### ENI Rules

| Action | Possible? |
|---|---|
| Detach ENI while server is running | ❌ No |
| Delete ENI while server is running | ❌ No |
| ENI deleted when server is stopped | ❌ No — ENI stays until terminate |
| ENI deleted when server is terminated | ✅ Yes — by default |
| Attach another server's ENI while that server is running | ❌ No |
| Attach ENI from a terminated server to a new server | ✅ Yes |

---

### ENI Use Case — Preserving Private IP After Server Corruption

**Problem:** OS is corrupted. You want to replace the server but keep the same private IP (used by downstream/upstream systems).

**Default behavior:** When you terminate a server, its ENI is deleted → IP released back to the subnet CIDR pool → no guarantee you get the same IP again.

**Two solutions:**

**Option 1 — Remember the IP, terminate, recreate ENI:**
1. Note down the private IP
2. Terminate the server (IP released to CIDR pool)
3. Create a new ENI with that specific IP
4. Launch a new server and attach that ENI

**Option 2 — Disable ENI auto-delete before terminating:**
1. Go to ENI → Actions → Change termination behavior → **Disable**
2. Terminate the server
3. ENI remains available with same IP, same SG
4. Launch a new server → attach existing ENI in Advanced Network Configuration

**Important:** ENIs created automatically with a server have "delete on termination" **enabled** by default. ENIs created manually and attached externally do **not** auto-delete.

---

### ENI + Elastic IP = Fully Static Network

You can attach an Elastic IP to an ENI. When that ENI is attached to a server:
- Public IP = static (Elastic IP)
- Private IP = static (defined in ENI)

Even if you terminate and replace the server, attaching the same ENI gives the new server the exact same public + private IPs.

---

## 📊 Quick Reference

| Concept | Detail |
|---|---|
| One TG = one path + one port | Cannot define multiple paths or ports in a single TG |
| LB health checks | LB does the checking, TG provides the configuration |
| ENI auto-delete | Enabled by default for server-created ENIs, disabled for externally-created ENIs |
| ENI holds | Private IP, Security Group, Subnet |
| To keep same IP after replace | Disable ENI auto-delete before terminating server |
| Elastic IP on ENI | Makes both public and private IPs static |

---

## 🏗️ Architecture Diagrams

**Single TG — health checks only for default path:**
```
Client → LB → TG-1 (port 80, /) → EC2
                                    ├── / (HC ✅)
                                    ├── /path1 (HC ❌ — no TG)
                                    └── /path2 (HC ❌ — no TG)
```

**Multiple TGs — health checks for all paths:**
```
Client → LB → TG-1 (port 80,   /)      → EC2 :80   /
              TG-2 (port 3000, /path1)  → EC2 :3000 /path1
              TG-3 (port 5000, /path2)  → EC2 :5000 /path2
```

**ENI — preserve IP on server replacement:**
```
Server 1 (OS corrupted)
    └── ENI [IP: 10.0.x.x, SG: sg-xxx]
            ↓ disable auto-delete
            ↓ terminate server 1
            ↓ ENI still available
New Server 2
    └── attach same ENI → gets same IP + SG
```

---

## ✅ Tasks Assigned

1. Create a server, deploy 3 applications at different paths (`/`, `/path1`, `/path2`)
2. Create TG for default path only → configure LB → test:
   - Hit LB DNS → verify routes to default
   - Hit LB DNS/path1 → verify behavior without TG
3. List common OS problems when running multiple apps on one OS (prep for Docker/Kubernetes)

---

## ❓ Questions I Still Have

- When attaching an externally-created ENI to a server, can you still add a separate SG on top, or is the ENI SG the only one that applies?
- If you attach an Elastic IP to an ENI, and then delete that ENI, does the Elastic IP get released automatically?

---

## 🔗 GitHub

```
docs: add day 17 notes - multi-path ALB, target groups, ENI
```

---

## ⏭️ Next Steps

- Practice: single server, multi-path nginx setup with separate TGs
- Research Docker and Kubernetes context — common OS problems with multiple apps
