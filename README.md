# DevOps Log — abishaix

Personal learning log for DevOps Bootcamp 2026. Documenting class notes, hands-on AWS labs, and architecture diagrams as I work through AWS, DevOps tooling, and cloud infrastructure.

**GitHub:** [abishaix/devops-log](https://github.com/abishaix/devops-log)
**LinkedIn:** [linkedin.com/in/abishaix](https://linkedin.com/in/abishaix)

---

## Progress Tracker

| Day | Topic | Notes | Lab |
|-----|-------|-------|-----|
| 1 | DevOps intro, lifecycle, roles | ✅ | — |
| 2 | AWS regions, availability zones | ✅ | — |
| 3 | VPC, subnets, public vs private cloud | ✅ | — |
| 4 | Security groups, ports, firewall | ✅ | — |
| 5 | TCP/UDP, CIDR, subnet math | ✅ | ✅ lab-01 |
| 6 | EC2, internet gateway, route table | ✅ | ✅ lab-02 |
| 7 | Custom VPC networking | ✅ | — |
| 8 | Bastion host, NAT gateway | ✅ | — |
| 9 | NAT gateway deep dive | ✅ | — |
| 10 | App deployment, nginx | ✅ | — |
| 11 | Load balancer | ✅ | ✅ lab-03 |
| 12 | Load balancer deep dive | ✅ | ✅ lab-04 |
| 13 | Path-based routing | ✅ | ✅ lab-05, lab-06 |
| 14 | Auto scaling group | ✅ | — |
| 15 | — | — | — |
| 16 | NLB + ALB integration | ✅ | — |
| 17 | Multipath ALB, ENI | ✅ | — |
| 18 | OS problems, S3 intro | ✅ | — |
| 19 | S3 deep dive | ✅ | — |
| 20 | — | — | — |
| 21 | Nginx reverse proxy | ✅ | ✅ lab-07 |
| 22 | Three-tier architecture | ✅ | ✅ lab-08 |
| 23 | S3 replication, inventory | ✅ | — |
| 24 | IAM users, groups, policies | ✅ | ✅ lab-09 |
| 25 | IAM custom policies, CLI debugging | ✅ | — |
| 26 | IAM roles, STS | ✅ | — |
| 27 | IAM groups, switch role, Route 53 | ✅ | ✅ lab-10 |
| 27b | IAM Identity Center, SSO | ✅ | — |
| 28 | Route 53 records, policies | ✅ | ✅ lab-11 |
| 29 | Route 53 policies, private zones | ✅ | — |
| 30 | HTTPS, SSL/TLS, ACM | ✅ | — |
| 31 | RDS — relational database service | ✅ | ✅ lab-12 |
| 32 | RDS lab, deployment options | ✅ | ✅ lab-13 |
| 33 | RDS private, backups, snapshots | ✅ | ✅ lab-14 |
| 34 | EC2 pricing, Secrets Manager | ✅ | — |
| 35 | VPC peering | ✅ | ✅ lab-15 |
| 36 | VPC endpoint connections | ✅ | ✅ lab-16, lab-17 |
| 37 | Cloud automation, Boto3, Lambda | ✅ | ✅ lab-18 |
| 38 | Lambda deep dive, EventBridge | ✅ | — |

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
│   ├── day-19-s3-deep-dive.md
│   ├── day-21-nginx-reverse-proxy.md
│   ├── day-22-three-tier-architecture-pip.md
│   ├── day-23-s3-replication-inventory.md
│   ├── day-24-iam-users-groups-policies.md
│   ├── day-25-iam-custom-policies-cli-debugging.md
│   ├── day-26-iam-roles-sts.md
│   ├── day-27-iam-groups-switch-role-route53.md
│   ├── day-27b-iam-identity-center-sso.md
│   ├── day-28-route53-records-policies.md
│   ├── day-29-route53-policies-private-zones.md
│   ├── day-30-https-ssl-tls-acm.md
│   ├── day-31-rds-relational-database-service.md
│   ├── day-32-rds-lab-deployment-options.md
│   ├── day-33-rds-private-backups-snapshots.md
│   ├── day-34-ec2-pricing-secrets-manager.md
│   ├── day-35-vpc-peering.md
│   ├── day-36-vpc-endpoint-connections.md
│   ├── day-37-cloud-automation-boto3-lambda.md
│   └── day-38-lambda-eventbridge.md
├── practice-logs/
│   ├── lab-01-aws-vpc-ec2-setup.md
│   ├── lab-02-custom-vpc-ec2.md
│   ├── lab-03-alb-target-group-failover.md
│   ├── lab-04-asg-alb-private-vpc.md
│   ├── lab-05-nlb-alb-asg.md
│   ├── lab-06-path-based-routing-alb.md
│   ├── lab-07-nginx-reverse-proxy-flask.md
│   ├── lab-08-two-tier-nginx-flask.md
│   ├── lab-09-route53-iam-groups-ec2.md
│   ├── lab-10-identity-center-sso.md
│   ├── lab-11-route53-routing-policies.md
│   ├── lab-12-rds-setup.md
│   ├── lab-13-rds-replica.md
│   ├── lab-14-rds-private-bastion.md
│   ├── lab-15-vpc-peering.md
│   ├── lab-16-s3-nat-gateway.md
│   ├── lab-17-transit-gateway-same-region.md
│   └── lab-18-boto3-lambda-ec2.md
├── diagrams/
├── screenshots/
└── cheatsheets/
```

---

## Bootcamp Roadmap

```
AWS Core (Days 1–38) ← currently here
├── Networking — VPC, subnets, IGW, NAT, peering, endpoints ✅
├── Compute — EC2, ASG, ALB, NLB ✅
├── Storage — S3, EBS ✅
├── Database — RDS ✅
├── IAM + Security ✅
├── Route 53 ✅
├── Cloud Automation — Boto3, Lambda, EventBridge ← Day 37–38
└── Coming up — Lambda labs, ElastiCache, more automation

DevOps Tooling (Months 3–6)
├── Docker
├── Kubernetes
├── Terraform
├── GitHub Actions / GitLab CI/CD
└── Prometheus + Grafana
```
