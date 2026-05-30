# Practice Log — S3 Access: NAT Gateway vs VPC Endpoint
**Date:** May 30, 2026
**Resources Created:** VPC, public/private subnets, bastion, private EC2, NAT Gateway, IAM role, S3 bucket
**Region:** us-west-2 (Oregon)

---

## What I Built

Two-part lab proving the difference between reaching S3 via NAT (internet path) vs VPC Gateway Endpoint (private path). Both use the same VPC and private EC2 — only the routing changes.

| Resource | Detail |
|---|---|
| VPC | `10.0.0.0/24` (mod1-vpc) |
| Public subnet | bastion lives here |
| Private subnet | ec2-private lives here (`10.0.140.142`) |
| Bastion | public IP `35.93.224.251` |
| NAT Gateway | `nat-1aa87c29fffdde9a9`, EIP `54.190.220.171` (regional) |
| IAM Role | EC2 service role with S3FullAccess |
| S3 Bucket | `s3-nat-access-bucket` |

---

## Part 1 — S3 Access via NAT Gateway

### What this proves
Private EC2 with no public IP reaches S3 through NAT → IGW → public internet. Traffic leaves the AWS network. Confirmed by matching `curl ifconfig.me` output to the NAT Gateway's Elastic IP.

### 🏗️ Architecture Diagram
![lab-16 NAT to S3 architecture](../diagrams/lab-16-s3-nat-gateway.svg)

**Hand-drawn:**
![hand-drawn NAT to S3 architecture](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/nat-s3-architecture.png)

### How it works

```
ec2-private (10.0.140.142, no public IP)
    │
    ▼
private subnet route table
    0.0.0.0/0 → NAT Gateway
    │
    ▼
NAT Gateway (54.190.220.171)
    │
    ▼
IGW → public internet → https://s3.us-west-2.amazonaws.com
    │
    ▼
S3 bucket (s3-nat-access-bucket) ✓
```

### Step by Step

**1. Connect to private server via bastion**

Connect to bastion via EC2 Instance Connect, then hop to the private server:

```bash
ssh -i vpc-peer.pem ec2-user@10.0.140.142
```

**2. Test S3 access without IAM role**

```bash
aws s3 ls
```

Result: `Unable to locate credentials` — the NAT route existed but the server had no identity. Connection layer works; auth layer missing.

**3. Attach IAM role to the private EC2**

EC2 → select ec2-private → Actions → Security → Modify IAM role → attach role with S3FullAccess → Update.

STS issues temporary credentials in the background automatically. No `aws configure` needed.

**4. Test S3 access with IAM role attached**

```bash
aws s3 ls
```

Result: `2026-05-30 08:51:09 s3-nat-access-bucket` ✓

**5. Prove traffic goes through NAT**

```bash
curl ifconfig.me
```

Result: `54.190.220.171` — matches the NAT Gateway's Elastic IP exactly. The private server has no public IP; NAT is masquerading as `54.190.220.171` for all outbound internet traffic.

**6. Capture the public S3 endpoint in use**

```bash
aws s3 ls --debug 2>&1 | grep -i "endpoint provider result"
```

Result: `Endpoint provider result: https://s3.us-west-2.amazonaws.com` — the public endpoint. After switching to the gateway endpoint in Part 2, this URL will change to an internal one.

Also visible in debug output: `X-Amz-Security-Token` — the STS temporary credential from the IAM role, rotating automatically, never stored on disk.

### Key lesson — connection vs authentication

```
First aws s3 ls:   NAT route existed  +  no IAM role  →  credentials error
Second aws s3 ls:  NAT route existed  +  IAM role      →  works ✓

Connection (how request gets to S3) = route table → NAT → IGW
Auth (who you are)                  = IAM role → STS temporary credentials
Both required. Either alone is not enough.
```

### Why IAM role, not `aws configure`

```
aws configure  → long-lived keys stored on disk
                 if server compromised → keys stolen → permanent access ✗

IAM role       → STS temporary credentials, rotate every 1-12 hours
                 if server compromised → credentials expire automatically ✓
```

### Screenshots

![bastion SSH then s3 ls](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/bastion-ssh-then-s3-ls.png)
*Connecting via bastion to private server, then running aws s3 ls.*

![curl ifconfig NAT IP](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/curl-ifconfig-nat-ip-1.png)
*curl ifconfig.me returning 54.190.220.171 — matches NAT Gateway EIP.*

![NAT gateway details](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/nat-gateway-details-1.png)
*NAT Gateway showing EIP 54.190.220.171 — confirms IP match.*

![VPC resource map](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/mod1-vpc-resource-map.png)
*mod1-vpc resource map showing subnets and NAT.*

![private route table NAT route](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/private-rtb-nat-route.png)
*Private subnet route table — 0.0.0.0/0 → NAT Gateway.*

![IAM role EC2 S3 access](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/iam-role-ec2-s3-access.png)
*IAM role with S3FullAccess attached to ec2-private.*

![S3 ls success with IAM](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-16/s3-ls-success-with-iam.png)
*aws s3 ls returning s3-nat-access-bucket after IAM role attached.*

---

## Part 2 — S3 Access via VPC Gateway Endpoint

*To be completed after gateway endpoint and interface endpoint practicals.*

---

## Cleanup

*(To be completed after Part 2 — delete in dependency order)*

## Cost

NAT Gateway: ~$0.045/hour + $0.045/GB data processed. Terminate promptly after lab. S3 bucket: free tier. EC2 instances: free tier (t2.micro).
