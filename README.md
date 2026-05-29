# DevOps Log — Abishai Muthyala

Personal DevOps learning log documenting AWS, Linux, networking, and infrastructure concepts from bootcamp and hands-on labs.

---

## Progress Tracker

| Day | Topic | Notes | Practice |
|-----|-------|-------|----------|
| 1 | DevOps intro, lifecycle, roles | [✅](notes/day-01-devops-intro.md) | ⬜ |
| 2 | AWS regions, availability zones | [✅](notes/day-02-aws-regions-az.md) | ⬜ |
| 3 | VPC, subnets, public vs private cloud | [✅](notes/day-03-vpc-subnets.md) | ⬜ |
| 4 | Security groups, ports, firewall | [✅](notes/day-04-security-groups.md) | ⬜ |
| 5 | TCP/UDP, CIDR, subnet math | [✅](notes/day-05-networking-vpc-cidr.md) | [✅](practice-logs/lab-01-aws-vpc-ec2-setup.md) |
| 6 | EC2, IGW, route table, SSH | [✅](notes/day-06-ec2-igw-route-table.md) | [✅](practice-logs/lab-02-custom-vpc-ec2.md) |
| 7 | Custom VPC networking | [✅](notes/day-07-custom-vpc-networking.md) | [✅](practice-logs/lab-03-alb-target-group-failover.md) |
| 8 | Bastion host, NAT gateway | [✅](notes/day-08-bastion-host-nat-gateway.md) | [✅](practice-logs/lab-04-asg-alb-private-vpc.md) |
| 9 | NAT gateway deep dive | [✅](notes/day-09-nat-gateway-deep-dive.md) | [✅](practice-logs/lab-05-nlb-alb-asg.md) |
| 10 | App deployment, Nginx | [✅](notes/day-10-app-deployment-nginx.md) | [✅](practice-logs/lab-06-path-based-routing-alb.md) |
| 11 | Load balancer intro | [✅](notes/day-11-load-balancer.md) | [✅](practice-logs/lab-07-nginx-reverse-proxy-flask.md) |
| 12 | Load balancer deep dive | [✅](notes/day-12-load-balancer-deep-dive.md) | [✅](practice-logs/lab-08-two-tier-nginx-flask.md) |
| 13 | ALB path-based routing, microservices | [✅](notes/day-13-path-based-routing.md) | ⬜ |
| 14 | Auto Scaling Group | [✅](notes/day-14-auto-scaling-group.md) | ⬜ |
| 15 | — | ⬜ | ⬜ |
| 16 | NLB, ALB, NLB+ALB integration | [✅](notes/day-16-nlb-alb-integration.md) | ⬜ |
| 17 | Multi-path ALB, target groups, ENI | [✅](notes/day-17-multipath-alb-eni.md) | ⬜ |
| 18 | OS problems, S3 intro | [✅](notes/day-18-os-problems-s3-intro.md) | ⬜ |
| 19 | S3 deep dive | [✅](notes/day-19-s3-deep-dive.md) | ⬜ |
| 20 | — | ⬜ | ⬜ |
| 21 | Nginx reverse proxy | [✅](notes/day-21-nginx-reverse-proxy.md) | [✅](practice-logs/lab-07-nginx-reverse-proxy-flask.md) |
| 22 | Three-tier architecture, Python backend, pip | [✅](notes/day-22-three-tier-architecture-pip.md) | [✅](practice-logs/lab-08-two-tier-nginx-flask.md) |
| 23 | S3 replication, inventory | [✅](notes/day-23-s3-replication-inventory.md) | ⬜ |
| 24 | IAM users, groups, policies | [✅](notes/day-24-iam-users-groups-policies.md) | [✅](practice-logs/lab-09-route53-iam-groups-ec2.md) |
| 25 | IAM custom policies, CLI, debugging | [✅](notes/day-25-iam-custom-policies-cli-debugging.md) | [✅](practice-logs/lab-09-route53-iam-groups-ec2.md) |
| 26 | IAM roles, STS, temporary credentials | [✅](notes/day-26-iam-roles-sts.md) | [✅](practice-logs/lab-09-route53-iam-groups-ec2.md) |
| 27 | IAM groups, switch role, Route 53 | [✅](notes/day-27-iam-groups-switch-role-route53.md) | [✅](practice-logs/lab-09-route53-iam-groups-ec2.md) |
| 27b | IAM Identity Center, SSO, AWS Organizations | [✅](notes/day-27b-iam-identity-center-sso.md) | [✅](practice-logs/lab-10-identity-center-sso.md) |
| 28 | Route 53 records, hosted zones, routing policies | [✅](notes/day-28-route53-records-policies.md) | [✅](practice-logs/lab-11-route53-routing-policies.md) |
| 29 | Route 53 failover, health checks, TTL, private hosted zones | [✅](notes/day-29-route53-policies-private-zones.md) | [✅](practice-logs/lab-11-route53-routing-policies.md) |
| 30 | HTTPS, SSL/TLS, ACM | [✅](notes/day-30-https-ssl-tls-acm.md) | ⬜ |
| 31 | AWS RDS — relational database service | [✅](notes/day-31-rds-relational-database-service.md) | [✅](practice-logs/lab-12-rds-setup.md) |
| 32 | RDS lab, deployment options | [✅](notes/day-32-rds-lab-deployment-options.md) | [✅](practice-logs/lab-13-rds-replica.md) |
| 33 | RDS private, backups, snapshots | [✅](notes/day-33-rds-private-backups-snapshots.md) | [✅](practice-logs/lab-14-rds-private-bastion.md) |
| 34 | EC2 pricing, Secrets Manager | [✅](notes/day-34-ec2-pricing-secrets-manager.md) | ⬜ |
| 35 | VPC peering | [✅](notes/day-35-vpc-peering.md) | [✅](practice-logs/lab-15-vpc-peering.md) |

---

## Repo Structure

```
devops-log/
├── README.md
├── notes/
│   ├── day-01 through day-35 (Days 15 and 20 not held)
├── practice-logs/
│   ├── lab-01 through lab-15
├── diagrams/
└── screenshots/
```

---

## Tech Stack

![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=flat&logo=linux&logoColor=black)
![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white)
