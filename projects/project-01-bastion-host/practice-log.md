# Practice Log — Project #1: Secure EC2 Access via Bastion Host

**Date:** April 23, 2026  
**Region:** ap-south-1 (Mumbai)  
**Duration:** ~1.5 hours  

---

## Resources Created

| Resource | ID |
|----------|----|
| VPC | vpc-0266d2ab75e9615e4 |
| Public Subnet | subnet-0d3bad6a263732401 |
| Private Subnet | subnet-0d92c5938d538a263 |
| Bastion EC2 | i-006424c198d9639b4 |
| Private EC2 | i-0e099ed69d1538ad2 |

---

## What I Built

Custom VPC with two subnets (public + private), Internet Gateway, NAT Gateway, and two EC2 instances. SSH access chain: laptop → Bastion → Private EC2. NAT confirmed working via `ping google.com` from private EC2.

---

## Step by Step

**1.** Created VPC using "VPC and more" wizard — CIDR `10.0.0.0/16`, 1 public subnet, 1 private subnet, NAT Gateway enabled.

**2.** Launched Bastion EC2 in public subnet — t3.micro, Amazon Linux 2023, `mykey.pem`.

**3.** Launched Private EC2 in private subnet — same AMI and key, no public IP.

**4.** Attempted SSH into Bastion — failed (no public IP on instance).

**5.** Enabled auto-assign public IPv4 on public subnet → re-launched Bastion → got public IP `13.233.168.56`.

**6.** Attempted SSH again — failed (connection timeout).

**7.** Checked Security Group — inbound was set to "All traffic" on the wrong SG. Updated to SSH port 22, source `0.0.0.0/0` for testing, then locked to my IP.

**8.** SSH into Bastion from laptop — success.
```bash
ssh -i "mykey.pem" ec2-user@13.233.168.56
```

**9.** Copied `mykey.pem` to Bastion, attempted SSH to private EC2 — failed with key permission error.
```
Permissions 0644 for 'mykey.pem' are too open.
```

**10.** Fixed permissions:
```bash
chmod 400 mykey.pem
```

**11.** Retried SSH — still failed. Error: `Permission denied (publickey)`.

**12.** Realized username typo — was using `ece-user` instead of `ec2-user`. Used AWS Console copy-paste command — success.
```bash
ssh -i "mykey.pem" ec2-user@10.0.140.167
```

**13.** Verified from private EC2:
```bash
ping google.com   # NAT working ✅
hostname          # ip-10-0-140-167.ap-south-1.compute.internal ✅
whoami            # ec2-user ✅
```

---

## Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| No public IP on Bastion | Auto-assign public IP disabled on subnet | Enabled in subnet settings |
| SSH connection timeout | Security Group had no inbound rule | Added SSH :22 inbound rule |
| `Permissions 0644 for mykey.pem are too open` | Key file too permissive | `chmod 400 mykey.pem` |
| `Permission denied (publickey)` after chmod | Username typo `ece-user` | Corrected to `ec2-user` |

---

## Cost

| Resource | Cost |
|----------|------|
| NAT Gateway | ~$0.045/hr while running |
| EC2 (t3.micro x2) | Free tier |
| Elastic IP | Free while attached to running NAT GW |
| **Total session** | **~$0.05–0.10** |

---

## Cleanup (completed)

- [x] Terminated both EC2 instances
- [x] Deleted NAT Gateway
- [x] Released Elastic IP
- [x] Deleted VPC (removes subnets, route tables, IGW)
