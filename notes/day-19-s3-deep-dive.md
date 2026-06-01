# Day 19 — S3 Deep Dive: Versioning, Pre-signed URLs, Static Website Hosting
**Date:** May 8, 2026

---

## 📚 Concepts Covered

- S3 bucket naming rules and why globally unique
- Pre-signed URLs — temporary access without making bucket public
- S3 Select — querying data directly from S3 objects
- S3 Versioning — tracking file changes, rollback
- S3 Static Website Hosting — deploying front-end projects
- S3 vs EC2 for hosting — when to use each
- CloudFront — proxy for private S3 buckets (intro)
- S3 high availability — data stored across minimum 3 AZs by default


## Contents

- [📚 Concepts Covered](#concepts-covered)
- [🧠 Theory Notes](#theory-notes)
  - [Bucket Naming — Why Globally Unique](#bucket-naming-why-globally-unique)
  - [Pre-signed URL](#pre-signed-url)
  - [S3 Select — Query Data in S3](#s3-select-query-data-in-s3)
  - [S3 Versioning — Deep Dive](#s3-versioning-deep-dive)
  - [S3 Static Website Hosting](#s3-static-website-hosting)
  - [S3 vs EC2 for Hosting](#s3-vs-ec2-for-hosting)
  - [S3 High Availability](#s3-high-availability)
  - [CloudFront — S3 Proxy (Intro)](#cloudfront-s3-proxy-intro)
- [🏗️ Architecture Diagram](#architecture-diagram)
- [✅ Tasks From Today](#tasks-from-today)
- [❓ Questions I Still Have](#questions-i-still-have)
- [🔗 GitHub](#github)
- [⏭️ Next Steps](#next-steps)

---

---

## 🧠 Theory Notes

### Bucket Naming — Why Globally Unique

S3 buckets have no IP address. The bucket name IS the address:

```
https://<bucket-name>.s3.amazonaws.com/folder/object
```

If two buckets had the same name, requests would route to the wrong one. Bucket names are permanent — renaming is not possible, just like you can't change a server's IP while it's live without breaking connections.

---

### Pre-signed URL

Gives temporary access to a private S3 object without making the bucket public.

| Property | Detail |
|---|---|
| Access type | Temporary |
| Max duration | 12 hours |
| Bucket status | Can remain private |
| Use case | Share a file with a colleague for limited time |

```
S3 bucket (private)
    │
    └── object (private)
            │
            ▼
        pre-signed URL
        (valid for X minutes/hours, max 12hr)
            │
            ▼
        anyone with the URL can access
        → after expiry: Access Denied
```

**vs Object URL:** Object URL is permanent but requires bucket and object to be public. Pre-signed URL is temporary, works on private buckets.

---

### S3 Select — Query Data in S3

Allows running SQL-like queries directly on data stored in S3 (CSV, JSON, Parquet). Useful for checking if data was updated without downloading the full file.

```sql
SELECT * FROM s3object LIMIT 5
```

For complex queries, use **Athena** — a dedicated analytics tool that integrates with S3 and supports full SQL.

---

### S3 Versioning — Deep Dive

When enabled, S3 keeps every version of every uploaded object.

```
Upload app.py v1 → stored as version 1
Make changes, upload app.py again → stored as version 2
v2 has a bug → restore v1 instantly
```

**Two advantages:**
1. Track every change to a file
2. Recover accidentally deleted objects

**Delete behavior with versioning enabled:**
- Delete main object → a "delete marker" is created, file still exists in versions
- Delete the delete marker → file is restored to main level
- Permanently delete → must delete from both main level AND versioning level

**When to use versioning:**
- Application code, artifacts, Terraform state files ✅
- Bulk data, backups, media files ❌ — doubles storage cost

---

### S3 Static Website Hosting

S3 can host static front-end projects directly — no EC2, no nginx, no VPC needed.

**What is static content:**
- HTML, CSS, JavaScript, images, videos — content that doesn't change per user
- Login pages, landing pages, portfolio sites

**What is NOT static (needs EC2 + backend):**
- Login logic (POST API to database)
- Dynamic data (GET from database per user)
- Any server-side processing

**How to enable:**
1. Upload all project files (index.html, style.css, images/)
2. Properties → Static website hosting → Enable
3. Set index document: `index.html`
4. Make bucket public (for learning) — in production use CloudFront instead

---

### S3 vs EC2 for Hosting

| | S3 Static Website | EC2 |
|---|---|---|
| Server management | No server needed | Need server |
| Cost | Very low | Higher |
| Scaling | Automatic | Manual/ASG |
| Maintenance | None | OS patches |
| High availability | Built-in (3+ AZs) | Need setup |
| Load balancer | Not needed | Often needed |
| Auto scaling | Automatic | Configure ASG |
| Storage | Unlimited | Limited disk |
| Performance | Fast with CloudFront | Depends on EC2 |
| Security patching | AWS manages | You manage |
| Use case | Static front-end only | Dynamic apps, APIs, backend |

**Rule:** If content is static → use S3. If content is dynamic (APIs, database) → use EC2.

---

### S3 High Availability

S3 works at region level but AWS automatically stores data across **minimum 3 AZs** within that region. You don't control which AZ — AWS handles it.

```
S3 bucket (ap-south-1)
    │
    ├── AZ: ap-south-1a → copy of app.py
    ├── AZ: ap-south-1b → copy of app.py
    └── AZ: ap-south-1c → copy of app.py
```

Even if 1 or 2 AZs fail, your data is still accessible. No need to configure multi-AZ like EC2.

---

### CloudFront — S3 Proxy (Intro)

In production, S3 buckets should be **private**. CloudFront acts as a proxy between users and S3.

```
User → CloudFront (public endpoint)
            │
            ▼
        S3 bucket (private)
        only accepts requests from CloudFront
```

Same concept as ALB + private EC2. CloudFront = ALB. S3 = private server.

Full CloudFront setup coming in later class.

---

## 🏗️ Architecture Diagram

![S3 Static Website & Versioning Architecture](https://raw.githubusercontent.com/abishaix/devops-log/main/diagrams/day-19-s3-deepdive-architecture.svg)

---

## ✅ Tasks From Today

1. Enable versioning on your S3 bucket
2. Upload a file, make changes, upload again — verify versions in console
3. Delete main object, restore from versioning
4. Enable static website hosting — deploy a simple HTML project
5. Test pre-signed URL — generate one, access it, wait for expiry

---

## ❓ Questions I Still Have

- ACL vs bucket policy — when to use which?
- Athena integration with S3 for complex queries
- CloudFront setup with private S3 bucket

---

## 🔗 GitHub

```
docs: add day 19 notes - S3 versioning, pre-signed URLs, static website hosting
```

---

## ⏭️ Next Steps

- CloudFront + private S3 bucket setup
- S3 storage classes — cost tiers
- S3 + EC2 integration
