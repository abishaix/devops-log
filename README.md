# DevOps Log — Abishai Muthyala

Personal DevOps learning log documenting AWS, Linux, networking, and infrastructure concepts from bootcamp and hands-on labs.

---

## Progress Tracker

| Day | Topic | Notes | Practice |
|-----|-------|-------|----------|
| 1 | DevOps intro, lifecycle, roles | ✅ | ⬜ |
| 2 | AWS regions, availability zones | ✅ | ⬜ |
| 3 | VPC, subnets, public vs private cloud | ✅ | ⬜ |
| 4 | Security groups, ports, firewall | ✅ | ⬜ |
| 5 | TCP/UDP, CIDR, subnet math | ✅ | ✅ |
| 6 | EC2, IGW, route table, SSH | ✅ | ✅ |
| 7 | Custom VPC networking | ✅ | ✅ |
| 8 | Bastion host, NAT gateway | ✅ | ✅ |
| 9 | NAT gateway deep dive | ✅ | ✅ |
| 10 | App deployment, Nginx | ✅ | ✅ |
| 11 | Load balancer intro | ✅ | ✅ |
| 12 | Load balancer deep dive | ✅ | ✅ |
| 13 | ALB path-based routing, microservices | ✅ | ✅ |
| 14 | Auto Scaling Group | ✅ | ✅ |
| 15 | — | ⬜ | ⬜ |
| 16 | NLB, ALB, NLB+ALB integration | ✅ | ✅ |
| 17 | Multi-path ALB, target groups, ENI | ✅ | ⬜ |
| 18 | OS problems, S3 intro | ✅ | ⬜ |
| 19 | S3 deep dive | ✅ | ⬜ |
| 20 | — | ⬜ | ⬜ |
| 21 | Nginx reverse proxy | ✅ | ✅ |
| 22 | Three-tier architecture, Python backend, pip | ✅ | ✅ |
| 23 | S3 replication, inventory | ✅ | ⬜ |
| 24 | IAM users, groups, policies | ✅ | ✅ |
| 25 | IAM custom policies, CLI, debugging | ✅ | ✅ |
| 26 | IAM roles, STS, temporary credentials | ✅ | ✅ |
| 27 | IAM groups, switch role, Route 53 | ✅ | ✅ |
| 27 (Part 2) | IAM Identity Center, SSO, AWS Organizations | ✅ | ✅ |
| 28 | Route 53 records, hosted zones, routing policies | ✅ | ✅ |
| 29 | Route 53 failover, health checks, TTL, private hosted zones | ✅ | ✅ |
| 30 | HTTPS, SSL/TLS, ACM | ✅ | ⬜ |
| 31 | AWS RDS — relational database service | ✅ | ⬜ |
| 32 | RDS lab: deployment options, read replicas, Aurora | ✅ | ✅ |

---

## Repo Structure

```
devops-log/
├── README.md
├── notes/
│   ├── day-01-devops-intro.md
│   ├── day-02-aws-regions-az.md
│   ├── day-03-vpc-subnets.md
│   ├── day-04-security-groups.md
│   ├── day-05-networking-vpc-cidr.md
│   ├── day-06-ec2-igw-route-table.md
│   ├── day-07-custom-vpc-networking.md
│   ├── day-08-bastion-host-nat-gateway.md
│   ├── day-09-nat-gateway-deep-dive.md
│   ├── day-10-app-deployment-nginx.md
│   ├── day-11-load-balancer.md
│   ├── day-12-load-balancer-deep-dive.md
│   ├── day-13-path-based-routing.md
│   ├── day-14-auto-scaling-group.md
│   ├── day-16-nlb-alb-integration.md
│   ├── day-17-multipath-alb-eni.md
│   ├── day-18-os-problems-s3-intro.md
│   ├── day-19-s3-deepdive.md
│   ├── day-21-nginx-reverse-proxy.md
│   ├── day-22-three-tier-architecture-pip.md
│   ├── day-23-s3-replication-inventory.md
│   ├── day-24-iam-users-groups-policies.md
│   ├── day-25-iam-custom-policies-cli-debugging.md
│   ├── day-26-iam-roles-sts.md
│   ├── day-27-iam-groups-switch-role-route53.md
│   ├── day-27-part2-iam-identity-center-sso.md
│   ├── day-28-route53-records-policies.md
│   ├── day-29-route53-policies-private-zones.md
│   ├── day-30-https-ssl-tls-acm.md
│   ├── day-31-rds-relational-database-service.md
│   └── day-32-rds-lab-deployment-options.md
├── practice-logs/
│   ├── lab-01-aws-vpc-ec2-setup.md
│   ├── lab-02-custom-vpc-ec2.md
│   ├── lab-03-alb-target-group-failover.md
│   ├── lab-04-asg-alb-private-vpc.md
│   ├── lab-05-nlb-alb-asg.md
│   ├── lab-06-path-based-routing-alb.md
│   ├── lab-07-nginx-reverse-proxy-flask.md
│   ├── lab-08-nginx-reverse-proxy-flask.md
│   ├── lab-09-route53-iam-groups-ec2.md
│   ├── lab-10-identity-center-sso.md
│   └── lab-11-route53-routing-policies.md
├── diagrams/
│   ├── day-32-rds-deployment-options.svg
└── screenshots/
```

---

## Tech Stack

![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
