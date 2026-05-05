# Lab 05 — NLB + ALB + ASG Integration
**Date:** May 5, 2026
**Region:** us-east-1
**VPC:** int01-vpc (`vpc-0732967ed82cb6ac2`)

---

## Resources Created

| Resource | Name | Details |
|---|---|---|
| VPC | int01-vpc | 10.0.0.0/16, 4 subnets across 2 AZs |
| NLB | NLB-01 | Internet-facing, Elastic IPs assigned, public subnets |
| NLB Target Group | TG-NLB01 | Protocol: TCP, target type: Application Load Balancer |
| ALB | ALB-01 | Internal, private subnets across us-east-1a + us-east-1b |
| ALB Target Group | TG-01 | Protocol: HTTP:80, target type: instance |
| Launch Template | LT-01 | ami-0b4a8843c1ef43fb4, v3 default, nginx user data |
| ASG | LT-01 | Min: 1, Max: 3, Desired: 3, target tracking 20% CPU |
| Bastion | bastion | t3.micro, us-east-1a, public subnet |
| App Server | app-server | t3.micro, us-east-1a, manually created |

---

## What I Built

NLB + ALB combination architecture. NLB sits in public subnets as the internet-facing entry point with static Elastic IPs for upstream whitelisting. ALB sits in private subnets as an internal load balancer. ASG manages EC2 instances bootstrapped via user data — nginx auto-starts on every new instance. Stress test confirmed ASG scaled out to 3 instances. Full flow validated via browser hitting NLB DNS endpoint.

---

## Architecture

```
Internet
    ↓
NLB-01 (public subnets, Elastic IPs)
    ↓ TCP
TG-NLB01 → ALB-01
    ↓ HTTP
TG-01
    ↓
EC2 Instances (private subnets, us-east-1b) ← managed by ASG
```

---

## Step by Step

1. Created ALB target group `TG-01` — HTTP:80, target type: instance
2. Created ALB `ALB-01` — internal, private subnets: int01-subnet-private1-us-east-1a + int01-subnet-private2-us-east-1b
3. Created NLB target group `TG-NLB01` — TCP:80, target type: Application Load Balancer, pointed to `ALB-01`
4. Created NLB `NLB-01` — internet-facing, public subnets, assigned Elastic IPs
5. Created launch template `LT-01` (v3) with user data:
```bash
#!/bin/bash
yum install nginx -y
systemctl start nginx
systemctl enable nginx
```
6. Created ASG `LT-01` — min 1, max 3, desired 1, attached to `TG-01`
7. Added target tracking scaling policy — CPU utilization target: 20%
8. Terminated old ASG instance (launched before user data was added), ASG replaced with bootstrapped instance
9. Verified TG-NLB01 showing ALB-01 as healthy target
10. Verified TG-01 showing 4/4 healthy targets (3 ASG instances + app-server)
11. SSH'd into ASG instance via bastion, ran stress test — ASG scaled out to desired 3
12. Validated full flow: browser hit NLB DNS → "Hello from EC2-1, Private Subnet | AZ: us-east-1a"

---

## Key Commands

```bash
# SSH hop via bastion
ssh -i abi.pem ec2-user@98.80.139.155        # bastion public IP
ssh -i abi.pem ec2-user@<asg-instance-ip>   # ASG instance private IP

# Verify nginx
systemctl status nginx

# Stress test (ASG scale-out trigger)
yum install stress -y
stress --cpu 8 --timeout 300
```

---

## Mistakes & Fixes

| Mistake | Root Cause | Fix |
|---|---|---|
| ASG not scaling | Scaling limits 1-1, no scaling policy | Set max to 3, created target tracking policy |
| New ASG instance unhealthy | nginx not running — instance launched before user data was added | Updated launch template with user data, terminated old instance |
| stress not found on ASG instance | User data only had nginx | Installed manually; updated launch template to include it |
| User data BASE64 error | Extra formatting in user data field | Pasted plain text without encoding |
| Stress test not triggering scale-out | Was running on app-server (not ASG-managed) | SSH'd into ASG instance via bastion instead |

---

## Screenshots

**VPC — int01-vpc, 10.0.0.0/16, resource map showing 4 subnets + IGW + NAT**
![VPC Overview](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.00.54PM.png)

**Subnets — 4 subnets across us-east-1a and us-east-1b (2 public, 2 private)**
![Subnets](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.01.09PM.png)

**Target Groups — TG-01 (HTTP, ALB-01) and TG-NLB01 (TCP, NLB-01, target: ALB)**
![Target Groups](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.08.27PM.png)

**TG-NLB01 — ALB-01 as registered target, health status: healthy**
![NLB Target Group](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.09.25PM.png)

**TG-01 — 4/4 healthy targets (3 ASG instances + app-server)**
![ALB Target Group](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.09.49PM.png)

**ASG — capacity overview, desired 3, scaling limits 1-3, at desired capacity**
![ASG Overview](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.10.06PM.png)

**ASG — automatic scaling, target tracking policy, 20% CPU utilization**
![ASG Scaling Policy](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.10.37PM.png)

**Launch Template LT-01 — v3 default, user data: nginx install + start + enable**
![Launch Template](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.11.27PM.png)

**Launch Template — advanced details showing user data script**
![Launch Template User Data](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.11.33PM.png)

**EC2 Instances — 3 ASG-managed m1.small instances + bastion + app-server, all running**
![EC2 Instances](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.11.57PM.png)

**Browser — NLB DNS endpoint serving "Hello from EC2-1, Private Subnet | AZ: us-east-1a"**
![Browser NLB Response](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/Screenshot%202026-05-05%20at%2010.12.11PM.png)

**Architecture Diagram — NLB + ALB + ASG**
![Architecture Diagram](https://github.com/abishaix/devops-log/raw/main/screenshots/nlb-alb-asg/NLB+ALB%20Integration.svg)

---

## Cleanup Order

1. ASG `LT-01` — terminates managed instances automatically
2. ALB `ALB-01`
3. NLB `NLB-01`
4. Target groups — `TG-01`, `TG-NLB01`
5. Elastic IPs — release both
6. EC2 instances — `app-server`, `bastion`
7. Launch template `LT-01`

---

## Next Steps

- Repeat this build from scratch without notes
- ENI deep dive — assigning static private IPs to EC2
- Complete remaining self-learning tasks: LB stickiness, scheduled ASG scaling, lifecycle policy
