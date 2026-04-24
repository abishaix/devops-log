# Practice Log — Project #2: Portfolio Website on EC2 with Nginx

**Date:** April 24, 2026  
**Region:** ap-south-1 (Mumbai)  
**Duration:** ~1 hour  

---

## Resources Created

| Resource | Details |
|----------|---------|
| VPC | 10.0.0.0/16 — manual build, no wizard |
| Public Subnet | ap-south-1a |
| Internet Gateway | Attached to VPC |
| Route Table | 0.0.0.0/0 → IGW, explicitly associated to subnet |
| Security Group | SSH :22 + HTTP :80 |
| EC2 | t3.micro · Amazon Linux 2023 · Nginx |

---

## What I Built

Single EC2 instance running Nginx serving a static HTML portfolio page. Fully custom VPC built resource by resource without the wizard.

---

## Step by Step

1. Created VPC `10.0.0.0/16` — VPC only, no wizard
2. Created public subnet inside the VPC
3. Created Internet Gateway → attached to VPC
4. Created route table → added `0.0.0.0/0 → IGW` route
5. Associated route table to public subnet explicitly
6. Created Security Group — SSH :22 + HTTP :80
7. Launched EC2 in public subnet with custom SG
8. SSH into EC2, installed Nginx, started and enabled service
9. Replaced default Nginx page with portfolio HTML
10. Verified at `http://<public-ip>` — site live ✅

---

## Errors & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| Subnet not showing in EC2 launch wizard | Subnet created in wrong VPC (default VPC) | Deleted and recreated subnet inside custom VPC |
| "Instance is not in public subnet" | Route table not associated with subnet | Route Tables → Subnet associations → explicitly associated |
| SG not appearing as option in EC2 launch | SG created in wrong VPC | Recreated SG inside correct VPC |

---

## Nginx Commands Used

```bash
sudo yum update -y
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx

# deploy portfolio page
sudo nano /usr/share/nginx/html/index.html
```

---

## Verified Output

Site live at `http://13.220.148.24` — portfolio page loading with full layout, navigation, and content.

---

## Cost

| Resource | Cost |
|----------|------|
| EC2 t3.micro | Free tier |
| Data transfer | Negligible |
| **Total** | **~$0.00** |

---

## Cleanup

- [ ] Terminate EC2
- [ ] Delete custom SG, route table, IGW, subnet, VPC
