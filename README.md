# devops-log

Personal documentation of a live DevOps bootcamp — notes, practice labs, architecture diagrams, and screenshots from hands-on AWS work.

> **Currently:** Deep in AWS IAM, Route 53, and Identity Center. Domain live at [abishaix.com](http://abishaix.com).

---

## 📊 Progress Tracker

| Day | Topic | Notes | Lab |
|-----|-------|:-----:|:---:|
| 1 | DevOps intro, lifecycle, roles | ✅ | — |
| 2 | AWS Regions & Availability Zones | ✅ | — |
| 3 | VPC, Subnets, Public vs Private Cloud | ✅ | — |
| 4 | Security Groups, Ports, Firewall | ✅ | — |
| 5 | TCP/UDP, CIDR, Subnet Math | ✅ | ✅ |
| 6 | EC2, IGW, Route Table, SSH | ✅ | ✅ |
| 7 | Custom VPC Networking | ✅ | — |
| 8 | Bastion Host, NAT Gateway | ✅ | — |
| 9 | NAT Gateway Deep Dive | ✅ | — |
| 10 | App Deployment with Nginx | ✅ | — |
| 11 | Load Balancer | ✅ | — |
| 12 | Load Balancer Deep Dive | ✅ | — |
| 13 | Path-Based Routing | ✅ | — |
| 14 | Auto Scaling Group | ✅ | — |
| 15 | — skipped — | — | — |
| 16 | NLB + ALB Integration | ✅ | — |
| 17 | Multipath ALB, ENI | ✅ | — |
| 18 | OS Problems, S3 Intro | ✅ | — |
| 19 | S3 Deep Dive | ✅ | — |
| 20 | — skipped — | — | — |
| 21 | Nginx Reverse Proxy, Frontend/Backend | ✅ | ✅ |
| 22 | Three-Tier Architecture, Python, pip | ✅ | ✅ |
| 23 | S3 Replication, Inventory | ✅ | — |
| 24 | IAM Users, Groups, Policies | ✅ | — |
| 25 | IAM Custom Policies, CLI Debugging | ✅ | — |
| 26 | IAM Roles, STS, Temporary Credentials | ✅ | — |
| 27 | IAM Groups, Switch Role, Route 53 Intro | ✅ | ✅ |
| 27b | IAM Identity Center, AWS SSO, Organizations | ✅ | ✅ |

**25 of 27 days documented.** Days 15 and 20 were skipped.

---

## 🔬 Practice Labs

| Lab | Topic | Screenshots |
|-----|-------|:-----------:|
| [lab-01](practice-logs/lab-01-aws-vpc-ec2-setup.md) | VPC + EC2 Setup | — |
| [lab-02](practice-logs/lab-02-custom-vpc-ec2.md) | Custom VPC + EC2 | — |
| [lab-03](practice-logs/lab-03-alb-target-group-failover.md) | ALB + Target Group + Failover | ✅ |
| [lab-04](practice-logs/lab-04-asg-alb-private-vpc.md) | ASG + ALB + Private VPC | ✅ |
| [lab-05](practice-logs/lab-05-nlb-alb-asg.md) | NLB + ALB + ASG | ✅ |
| [lab-06](practice-logs/lab-06-path-based-routing-alb.md) | Path-Based Routing + ALB | ✅ |
| [lab-07](practice-logs/lab-07-nginx-reverse-proxy-flask.md) | Nginx Reverse Proxy + Flask | ✅ |
| [lab-08](practice-logs/lab-08-nginx-reverse-proxy-flask.md) | Nginx Reverse Proxy + Flask (Two-Tier) | ✅ |
| [lab-09](practice-logs/lab-09-route53-iam-groups-ec2.md) | IAM Groups + EC2 + Route 53 + abishaix.com | ✅ |
| [lab-10](practice-logs/lab-10-identity-center-sso.md) | IAM Identity Center + AWS SSO + Organizations | ✅ |

---

## 🗂️ Repo Structure

```
devops-log/
├── README.md
├── notes/              # Daily class notes (Days 1-27)
├── practice-logs/      # Hands-on lab writeups (lab-01 to lab-10)
├── diagrams/           # SVG architecture diagrams
├── screenshots/        # Lab screenshots organized by lab number
│   ├── lab-03/
│   ├── lab-04/
│   ├── lab-05/
│   ├── lab-07/
│   ├── lab-08/
│   ├── lab-09/
│   └── lab-10/
└── cheatsheets/        # AWS CLI, CIDR reference, Linux commands
```

---

## 🛠️ Stack Covered So Far

`AWS` `VPC` `EC2` `S3` `IAM` `Route 53` `ALB` `NLB` `ASG` `NAT Gateway` `Nginx` `Flask` `Linux` `Bash` `Git`

---

## 🔗 Links

- GitHub: [abishaix](https://github.com/abishaix)
- LinkedIn: [abishaix](https://linkedin.com/in/abishaix)
- Site: [abishaix.com](http://abishaix.com)
