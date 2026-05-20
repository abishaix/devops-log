# Practice Log — Route 53 Records, Hosted Zones, and Routing Policies
**Date:** May 20, 2026
**Resources Created:** 3 EC2 instances, 1 ALB, 1 Target Group, 2 Health Checks, Route 53 records
**Regions:** ap-south-1 (Mumbai), us-east-1 (US East)

---

## What I Built

End-to-end Route 53 lab covering all 5 routing policies. Deployed web servers across two AWS regions, configured an Application Load Balancer, and tested Simple, Alias, Subdomain, CNAME, Weighted, Geolocation, Latency, and Failover routing — all on the live domain `abishaix.com`.

---

## 🏗️ Architecture Diagrams

*(Hand-drawn diagram — to be added)*

---

## Infrastructure Summary

| Resource | Name | Details |
|---|---|---|
| EC2 Server 1 | route53-web | t3.micro, ap-south-1, `3.6.38.190` |
| EC2 Server 2 | route53-web-2 | t3.micro, ap-south-1, `15.206.66.155` |
| EC2 Server 3 | route53-web-us | t3.micro, us-east-1, `44.204.219.97` |
| Target Group | route53-tg | HTTP:80, ap-south-1 |
| Load Balancer | route53-alb | ALB, internet-facing, ap-south-1 |
| Health Check 1 | primary-mumbai | HTTP `3.6.38.190:80/` |
| Health Check 2 | secondary-us | HTTP `44.204.219.97:80/` |
| Hosted Zone | abishaix.com | Public hosted zone |

---

## Step by Step

### Scenario 1 — Simple Routing (A record → EC2 IP)

Launched `route53-web`, installed Apache, created an A record pointing `abishaix.com` to `3.6.38.190`.

```bash
sudo yum install -y httpd
sudo systemctl start httpd
sudo systemctl enable httpd
echo "<h1>Route 53 Lab — Simple Routing</h1>" | sudo tee /var/www/html/index.html
```

Route 53 record:
- Type: A
- Value: `3.6.38.190`
- Policy: Simple

Result: `http://abishaix.com` → EC2 directly ✅

---

### Scenario 2 — Alias Record (domain → ALB)

Created Target Group `route53-tg` → registered `route53-web` → created ALB `route53-alb` → edited the A record to Alias pointing to ALB.

Route 53 record:
- Type: A (Alias ON)
- Route traffic to: Application Load Balancer → ap-south-1 → route53-alb
- Policy: Simple
- Evaluate target health: Yes

Result: `http://abishaix.com` → ALB → EC2 ✅

Key learning: Alias is preferred over raw IP for AWS endpoints — AWS manages the IP, no manual updates needed.

---

### Scenario 3 — Subdomain (api.abishaix.com)

Created a separate A record for the subdomain — no domain registration needed.

```bash
echo "<h1>api.abishaix.com — API Server</h1>" | sudo tee /var/www/html/index.html
```

Route 53 record:
- Name: `api`
- Type: A
- Value: `3.6.38.190`
- Policy: Simple

Result: `http://api.abishaix.com` → EC2 ✅

Key learning: Once root domain is registered, unlimited free subdomains can be created in Route 53.

---

### Scenario 4 — CNAME Record (dev.abishaix.com → abishaix.com)

Route 53 record:
- Name: `dev`
- Type: CNAME
- Value: `abishaix.com`
- Policy: Simple

Result: `dev.abishaix.com` → resolves to `abishaix.com` → EC2 ✅

Key learning: CNAME maps one domain to another. Cannot be used at root domain apex — use Alias there instead.

---

### Scenario 5 — Weighted Routing (70/30 split)

Launched second server `route53-web-2`. Set different page content on each server to identify which one responds.

Deleted simple A record → created two weighted records:

| Record | IP | Weight |
|---|---|---|
| server-1 | `3.6.38.190` | 70 |
| server-2 | `15.206.66.155` | 30 |

Result: `http://abishaix.com` → Server 1 majority, Server 2 occasionally ✅

Key learning: Higher weight = more traffic. Useful for A/B testing and gradual rollouts.

---

### Scenario 6 — Geolocation Routing (Turkey only)

Deleted simple api A record → created geolocation record:

- Name: `api`
- Type: A
- Value: `3.6.38.190`
- Policy: Geolocation
- Location: Turkey

Test 1: Accessed from Turkey → `api.abishaix.com` loaded ✅
Test 2: Changed record to Bulgaria → `api.abishaix.com` unreachable ✅ (blocked — not in Turkey)

Key learning: Geolocation uses IP-based satellite location data. No policy = global access by default.

---

### Scenario 7 — Failover Routing (Primary/Secondary + Health Checks)

Launched `route53-web-us` in us-east-1 with content "Secondary Server — US East (Failover)".

Created two health checks:
- `primary-mumbai` → monitors `3.6.38.190:80`
- `secondary-us` → monitors `44.204.219.97:80`

Created failover records:

| Record | IP | Type | Health Check |
|---|---|---|---|
| primary-mumbai | `3.6.38.190` | Primary | primary-mumbai |
| secondary-us | `44.204.219.97` | Secondary | secondary-us |

**Normal state test:** Route 53 Test Record → returned `3.6.38.190` (primary) ✅

**Simulated failure:** Inverted `primary-mumbai` health check → Route 53 Test Record → returned `44.204.219.97` (secondary) ✅

Key learning:
- Disable ≠ Unhealthy. Use **Invert** to simulate failure
- Health checks must be enabled for failover to work
- **Route 53 failover + Load Balancer = high availability at both zone AND region level**

---

### Scenario 8 — Latency Routing (Mumbai vs US East)

Created two latency records:

| Record | IP | Region |
|---|---|---|
| latency-mumbai | `3.6.38.190` | ap-south-1 |
| latency-us | `44.204.219.97` | us-east-1 |

Tested via Route 53 Test Record tool with different resolver IPs. US East resolver → returned US East IP. Mumbai resolver → returned Mumbai IP.

Key learning: Latency routing uses AWS's internal latency database between AWS regions — not geographic distance. Load balancer is region-scoped — one LB per region required for latency routing.

---

## Screenshots

EC2 instance running:
![EC2 summary](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/ec2-route53-web-summary.png)

Simple routing working:
![Simple routing](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/simple-routing-page.png)

ALB details:
![ALB details](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/alb-route53-details.png)

Alias record editing:
![Alias record](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/r53-edit-record-alias-alb.png)

ALB direct hit confirming server works:
![ALB direct](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/alb-dns-direct-hit.png)

Subdomain working:
![Subdomain](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/api-subdomain-page.png)

Weighted records in Route 53:
![Weighted records](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/r53-weighted-records-list.png)

Server 1 (70%):
![Server 1](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/weighted-server1-70.png)

Server 2 (30%):
![Server 2](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/weighted-server2-30.png)

Geolocation test record:
![Geolocation](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/r53-test-record-geolocation.png)

Failover records created:
![Failover records](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/r53-failover-records-created.png)

Health checks status:
![Health checks](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/r53-health-checks-mumbai-unhealthy.png)

Failover secondary server:
![Failover secondary](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/failover-secondary-page.png)

Latency records:
![Latency records](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-11/r53-latency-records-created.png)

---

## Troubleshooting

**Issue 1: A record already exists error**
- Cause: Tried to create a new record instead of editing the existing one
- Fix: Select existing record → Edit record (not Create)

**Issue 2: abishaix.com not loading after ALB setup**
- Cause: ALB security group had no inbound rule for port 80
- Fix: Added HTTP port 80 from `0.0.0.0/0` to ALB security group

**Issue 3: DNS_PROBE_FINISHED_NXDOMAIN**
- Cause: Frequent record type changes (simple → weighted → latency → failover) confused DNS resolvers
- Fix: Wait for TTL (60 seconds) to expire and retry in incognito

**Issue 4: Failover returning secondary even when primary healthy**
- Cause: Still had latency records instead of failover records — delete confirmation wasn't done
- Fix: Verified records list, deleted latency records, recreated failover records properly

**Issue 5: Disabling health check didn't trigger failover**
- Cause: Disabling a health check keeps it in healthy state — Route 53 treats disabled = healthy
- Fix: Used Invert instead of Disable to simulate unhealthy state

**Issue 6: dev.abishaix.com not loading**
- Cause: CNAME points to abishaix.com which itself wasn't resolving (missing A record)
- Fix: Recreated the root A record first, then CNAME resolved correctly

---

## Cleanup Order

1. Delete all Route 53 records except NS and SOA
2. Delete health checks (`primary-mumbai`, `secondary-us`)
3. Delete ALB `route53-alb`
4. Delete Target Group `route53-tg`
5. Terminate EC2 instances: `route53-web`, `route53-web-2` (ap-south-1)
6. Switch to us-east-1 → terminate `route53-web-us`
7. Delete security groups created for this lab

---

## Key Learnings

- Simple routing = default, no conditions, direct mapping
- Alias record = preferred for all AWS endpoints (ALB, S3, CloudFront)
- Subdomains are free — only root domain needs to be purchased
- CNAME = domain to domain mapping, cannot be used at apex
- Weighted = manual traffic split, useful for gradual rollouts and A/B testing
- Geolocation = country/region-based access control, IP location-based
- Failover = primary/secondary with health checks, **Invert ≠ Disable** for simulating failure
- Latency = routes to lowest-latency region per AWS's internal latency database
- **Route 53 failover + ALB = high availability at both AZ level and region level**
- LB is region-scoped — latency and failover policies each need one LB per region

---

## Cost

| Resource | Cost |
|---|---|
| EC2 t3.micro × 3 | Free tier |
| ALB | ~$0.02/hour — deleted same day |
| Route 53 health checks | $0.50/month each — deleted same day |
| Route 53 hosted zone | $0.50/month — kept for future labs |
| Data transfer | Minimal |
