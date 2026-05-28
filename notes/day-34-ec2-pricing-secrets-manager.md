# Day 34 — EC2 Pricing Models, Secrets Manager & VPC Endpoints Preview
**Date:** May 28, 2026

---

## 📚 Concepts Covered
- EC2 instance purchasing options: On-Demand, Reserved, Spot, Dedicated Host, Capacity Reservation
- Reserved instance: payment options, convertible vs standard, 1-year vs 3-year
- Spot instances: how they work, drawbacks, when to use with ASG
- Dedicated Host: bare metal hardware allocation, instance families, CPU planning
- AWS Secrets Manager: credential storage, automatic rotation, RDS integration
- Why you must never hardcode DB credentials in application code
- Getting secrets from Secret Manager in backend code
- RDS + Secret Manager architecture challenge: private RDS, Secret Manager outside VPC
- Preview: VPC Endpoints, VPC Peering, Transit Gateway, VPN — upcoming classes
- Performance Insights: query-level CPU/memory analysis
- RDS snapshots: export to S3, difference from automated backups

---

## 🧠 Theory Notes

### EC2 Purchasing Options Overview

```
On-Demand
  └── Default. Create anytime, pay per use. No commitment.

Reserved Instance
  └── Commit 1 or 3 years upfront. Up to 72% discount.

Spot Instance
  └── Use unused datacenter capacity. Up to 90% discount.
      Can be interrupted anytime by AWS.

Dedicated Host
  └── Reserve physical bare-metal hardware. Most expensive.
      No other tenants share your hardware.

Capacity Reservation
  └── Reserve instance capacity in a specific AZ.
      No billing discount — just guarantees the slot is available.
```

---

### On-Demand Instances

Default behavior — no commitment, no reservation. Create and delete whenever needed.

Best for:
- Development and testing
- Short-lived or unpredictable workloads
- Applications where you don't yet know runtime duration

Cost: highest per-hour rate, but no upfront commitment.

---

### Reserved Instances

You commit to a specific instance type and region for 1 or 3 years. AWS gives a discount in return.

**Types:**
| Type | What it means |
|---|---|
| Standard | Fixed instance type, no changes allowed. Higher discount. |
| Convertible | Can change instance type during the term. Slightly lower discount. |

**Payment options:**
| Option | How it works |
|---|---|
| All Upfront | Pay full amount now. Maximum discount. |
| Partial Upfront | Pay part now, rest monthly. |
| No Upfront | Pay monthly. Least discount, but no initial cost. |

**Term options:** 1 year or 3 years only — no other slots.

Example: t3.micro for 3 years, all upfront = ~$103. vs on-demand = ~$300+ for same period. Effective saving ~72%.

**Drawback:** Whether you use it or not, you pay. Like reserving a car for a week — you owe the fee regardless.

**Best for:** Production servers, databases, applications running 24/7 with a known lifecycle.

```
My app runs continuously for 2+ years → Reserved
My app runs for 2 months → On-Demand
My app runs for testing only → On-Demand
```

---

### Spot Instances

AWS collects unused capacity (leftover hardware space) from data centers and offers it at deep discount — up to 90% cheaper than On-Demand.

**How it works:**
```
Datacenter hardware
  └── Some capacity always unused at any given time
        └── AWS packages this as "spot capacity"
              └── Available on request, no guarantee
                    └── Price fluctuates based on availability
```

**Drawbacks:**
- Cannot change instance type after launch (hardware is pre-allocated leftover)
- AWS can delete your spot instance anytime — if another workload needs the hardware, your instance gets reclaimed
- No long-term guarantee of availability
- Not suitable as a single standalone instance

**Why you must pair Spot with ASG:**

```
Single spot instance
  └── Gets terminated by AWS
        └── Application is down ❌

Spot instances inside Auto Scaling Group (10 instances)
  └── One instance gets terminated
        └── Remaining 9 still serving traffic ✅
              └── ASG tries to replace the terminated one
                    └── If spot available → new instance launches
                          └── If not → tries again later
```

Set ASG target CPU at 50% (not 70%) to leave headroom — if one instance disappears, the rest can absorb traffic before replacement arrives.

**Best for:** Batch jobs, CI/CD pipeline runners, fault-tolerant distributed workloads, temporary processing tasks where interruptions are acceptable.

**ASCII Flow — Spot + ASG Pattern:**
```
Load Balancer
      │
      ├──► Spot Instance 1  ◄── may be deleted anytime
      ├──► Spot Instance 2  ◄── may be deleted anytime
      ├──► Spot Instance 3  ← still running
      └──► Spot Instance 4  ← still running

If instances 1 & 2 are reclaimed:
  ASG detects count below desired → requests new spot capacity
  If available → new instances launch
  Traffic handled by 3 & 4 in the meantime
```

---

### Dedicated Host

Reserve actual physical bare-metal hardware. AWS allocates a specific server to you exclusively — no other customer's instances share that hardware.

**Use case:** Compliance requirements, licensing constraints (some software licenses are per-socket/core), need for physical isolation.

**Cost:** Most expensive option.

**How CPU planning works:**
```
C5 instance family → 96 physical CPUs allocated to you

Instance type    CPUs each    Max instances from 96 CPUs
m5.xlarge        4 CPUs       24 instances
m5.2xlarge       8 CPUs       12 instances
m5.4xlarge       16 CPUs      6 instances
c5.metal         96 CPUs      1 instance (bare metal)
```

You decide how to carve up the hardware. Unused CPUs sit idle — that's fine, the hardware is yours.

**Cost comparison:**
```
Spot          → cheapest (~90% discount vs On-Demand)
Reserved      → moderate (~72% discount)
On-Demand     → standard price
Dedicated Host → most expensive
```

---

### AWS Secrets Manager

A fully managed AWS service for storing, rotating, and retrieving secrets — database credentials, API keys, passwords.

**Why not hardcode credentials:**
```python
# BAD — hardcoded credentials
conn = mysql.connect(
    host="database-1.xxxxx.rds.amazonaws.com",
    user="admin",
    password="MyPassword123"   # ← hardcoded
)
```

Problems:
- Anyone with repo access can see the password
- Password rotation breaks the app
- Security audits flag hardcoded credentials immediately

**Secrets Manager approach:**
```python
# GOOD — credentials fetched from Secrets Manager at runtime
import boto3
import json

client = boto3.client('secretsmanager')
secret = client.get_secret_value(SecretId='rds!db-xxxxxxxx')
creds = json.loads(secret['SecretString'])

conn = mysql.connect(
    host=creds['host'],
    user=creds['username'],
    password=creds['password']
)
```

App fetches credentials from Secrets Manager at startup. When password rotates, app picks up the new one automatically — no code change needed.

---

### Secrets Manager — Automatic Rotation

```
Default rotation: every 7 days
Configurable: daily, weekly, monthly (e.g. every 30 days)

Day 1:  password = "xK9$mPq2"
Day 7:  password rotates → "rT4@nWv8"  ← Secrets Manager updates automatically
Day 14: password rotates → "bY7#jLx1"
...
```

Backend app never knows the actual password — it just asks Secrets Manager "what's the current password?" every time it connects. No hardcoded value to become stale.

If you hardcode the password, after first rotation your app starts failing with authentication errors.

---

### RDS + Secrets Manager Integration

When creating or modifying RDS, you can set credential management to:
- **Self-managed** — you set and manage the password
- **Managed by AWS Secrets Manager** — RDS generates a strong password and stores it in Secrets Manager with rotation enabled

To view credentials: Secrets Manager → select secret → Retrieve secret value → shows username + password.

---

### Architecture Challenge: Private RDS + Secret Manager

Secrets Manager is a global AWS service — it lives **outside your VPC**.

```
VPC
  └── Private Subnet
        └── RDS Instance (private, no internet)
              │
              └── needs to reach → Secrets Manager (outside VPC)
                                    ← no route available
                                    ← public access disabled
                                    ← no IGW in private subnet
```

**Problem:** Private RDS has no internet path to reach Secrets Manager.

**Solution (preview — next class):** VPC Endpoint for Secrets Manager.

```
VPC
  └── Private Subnet
        └── RDS / Backend Server
              │
              └──► VPC Endpoint (Secrets Manager)
                        │
                        └──► Secrets Manager (AWS network — no internet)
```

VPC Endpoints create a private connection from inside your VPC to AWS services without going through the internet. Traffic stays on the AWS backbone.

---

### ASCII Flow — Backend → Secrets Manager → RDS (Full Path)

```
Request
    │
    ▼
Backend Server (private subnet)
    │
    ├──1. GET secret ──────────────► VPC Endpoint ──► Secrets Manager
    │       ◄─── username + password ─────────────────────────────────
    │
    ├──2. Connect to RDS using fetched credentials
    │         │
    │         ▼
    │      RDS (private subnet)
    │         └── authenticate → authorized ✅
    │
    └──3. Run query → return data
```

---

### Upcoming Networking Concepts (Preview)

| Concept | What it solves |
|---|---|
| VPC Endpoint | Connect VPC privately to AWS services (S3, Secrets Manager, etc.) without internet |
| VPC Peering | Connect two VPCs in the same or different accounts so they can communicate privately |
| Transit Gateway | Hub-and-spoke: connect multiple VPCs and on-prem networks through a single gateway |
| VPN | Secure encrypted tunnel over internet from on-prem/office to AWS VPC |

These are all required for the full three-tier project with private RDS, backend in a separate VPC, and cross-account access.

---

### Performance Insights

Available on Aurora; limited on standard RDS free tier. Lets you see which SQL queries are consuming the most CPU/memory.

**Use case:** Database is hitting high CPU. Performance Insights shows the last N queries ranked by resource consumption. Lets you identify a bad query — e.g. a `SELECT * FROM orders` with no filter running against millions of rows.

Fix pattern:
```sql
-- BAD: processes all rows
SELECT * FROM orders;

-- GOOD: filter applied, only processes matching partition
SELECT * FROM orders WHERE order_date = '2026-05-28';
```

---

### RDS Snapshot vs Automated Backup (Reinforced)

| | Automated Backup | Manual Snapshot |
|---|---|---|
| Who triggers | AWS (scheduled daily) | You (manually) |
| Retention | Rolling 35 days max | Kept until deleted |
| Contains | Last 35 days of data | Point-in-time data at snapshot moment |
| Export to S3 | No (stays in RDS) | Yes — can export to S3 bucket |
| Use case | Daily protection, point-in-time restore | Before risky changes, region migration |

Snapshot restore = new RDS instance with all data (database + tables + records) already in it.

---

## 📊 Quick Reference Tables

### EC2 Purchasing Options Summary

| Type | Discount | Commitment | Can be interrupted? | Best for |
|---|---|---|---|---|
| On-Demand | None | None | No | Testing, short-lived, unknown duration |
| Reserved | ~72% | 1 or 3 years | No | Production, 24/7, known lifecycle |
| Spot | ~90% | None | Yes — anytime | Batch, CI/CD, fault-tolerant workloads |
| Dedicated Host | None (cost ++) | Optional | No | Compliance, licensing, physical isolation |
| Capacity Reservation | None | None | No | Guarantee AZ slot without cost commitment |

### Reserved Instance Payment Options

| Payment | Upfront cost | Monthly cost | Total discount |
|---|---|---|---|
| All Upfront | Full amount now | None | Maximum |
| Partial Upfront | Part now | Remainder monthly | Moderate |
| No Upfront | None | Full monthly | Minimum |

---

## 🏗️ Architecture / Diagram

![Day 34 — Secrets Manager + VPC Architecture](../diagrams/day-34-secrets-manager-vpc.svg)

---

## ✅ What I Practiced
- Modified RDS to switch from self-managed to Secrets Manager credentials
- Navigated to Secrets Manager → viewed auto-generated secret
- Observed rotation settings (7-day default)
- Reviewed spot instance fleet creation UI — instance family, CPU/RAM range, cost per hour
- Reviewed reserved instance purchase UI — term, payment option, effective rate
- Reviewed dedicated host allocation UI — instance family, CPU allocation

---

## ❓ Questions I Still Have
- How does VPC Endpoint for Secrets Manager work in practice — what does the endpoint configuration look like?
- VPC Peering vs Transit Gateway — when does Transit Gateway make more sense?
- If Secret Manager rotates password, does RDS automatically accept the new one or do we need to update anything on the RDS side?
- Can you use Spot instances for RDS? (Answer: No — but worth confirming)

---

## ⏭️ Next Steps
- VPC Endpoints — private connectivity to AWS services
- VPC Peering — cross-VPC connectivity
- Transit Gateway — multi-VPC hub
- VPN — on-prem to AWS secure connection
- Then: backend application connecting to private RDS through all of the above
