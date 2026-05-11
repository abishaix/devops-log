# Day 21 — Nginx Reverse Proxy & Frontend/Backend Architecture
**Date:** May 11, 2026

---

## 📚 Concepts Covered
- Where static files execute (browser vs server)
- Web server role (Nginx as content deliverer)
- Why client browsers can't reach internal load balancers
- Nginx as reverse proxy — replacing AWS ALB with a public EC2
- Nginx upstream blocks for multi-server load balancing
- Path-based routing via Nginx
- Two solutions for frontend-backend communication: reverse proxy vs dynamic frameworks

---

## 🧠 Theory Notes

### Where Does Code Execute?

Web server (Nginx/Apache) delivers HTML, JS, CSS files to the client. Those files execute **inside the client browser**, not on the server.

- Static files on S3 → executed on client machine
- Static files on Nginx EC2 → still executed on client browser
- Server's job: deliver the content. Browser's job: run it.

### Why Client Can't Reach Internal Load Balancer

Frontend code runs in the browser (on the user's laptop). If that code tries to call a backend API pointing to an **internal load balancer** (private IP), it fails — the browser is outside the VPC, it can't reach private IPs.

```
User Laptop (Browser)
  └─ Executes frontend JS
       └─ Tries to call backend internal LB → ❌ NOT REACHABLE
```

The browser is external. Internal LBs are private. This is the core problem.

### Web Server vs Reverse Proxy

Same Nginx process, different config:

| Mode | What It Does |
|---|---|
| Web Server | Delivers static HTML/CSS/JS to clients |
| Reverse Proxy | Accepts client requests, forwards them to a backend server |

### Nginx as Your Own Load Balancer

Instead of AWS ALB, you can use a **public EC2 running Nginx** to redirect traffic into private servers. This is exactly what a load balancer does — take client requests, forward to targets.

```
Client → Public EC2 (Nginx reverse proxy) → Private EC2 (Flask/Node app on :5000)
```

Nginx config for basic reverse proxy:
```nginx
server {
    listen 80;
    location / {
        proxy_pass http://<private-ip>:5000;
    }
}
```

### Nginx Upstream — Multiple Backend Servers

For multiple backends, define an upstream block:

```nginx
upstream flaskapp {
    server <private-ip-1>:5000;
    server <private-ip-2>:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://flaskapp;
    }
}
```

Nginx round-robins between servers by default — same as ALB default behavior.

### Path-Based Routing in Nginx

```nginx
upstream app1_backend {
    server <ip1>:5000;
}

upstream app2_backend {
    server <ip2>:5000;
}

server {
    listen 80;
    location /app1 {
        proxy_pass http://app1_backend;
    }
    location /app2 {
        proxy_pass http://app2_backend;
    }
}
```

This is the same logic as ALB listener rules with path conditions.

### Two Solutions for Frontend-Backend Access Problem

**Option 1 — Nginx Reverse Proxy (recommended for static frontends)**
- Frontend code calls `/api` (relative path, not the backend IP directly)
- Nginx reverse proxy config on the frontend server intercepts `/api` calls
- Nginx forwards them to the backend internal LB or private IP
- Client browser never touches the backend directly

**Option 2 — Dynamic Framework (no reverse proxy needed)**
- Use Flask, Django, React SSR, etc.
- Framework executes code **server-side**, not in the browser
- Server-to-server communication works fine within the same VPC
- No need for reverse proxy since the request never leaves the VPC

### Why Nginx Reverse Proxy ≠ AWS ALB at Scale

| | Nginx on EC2 | AWS ALB |
|---|---|---|
| High availability | Single server — SPOF | Multi-AZ by default |
| Scalability | One EC2 handles everything | Fully managed, handles millions of req/s |
| ASG integration | Manual IP updates required | Native target group integration |
| Maintenance | You manage OS, Nginx, restarts | Fully managed |

Use Nginx reverse proxy for: local dev, small projects, learning. Use AWS ALB for: production.

---

## 💻 Commands & Code

### Deploy Python Flask App on Private EC2

```bash
# Install pip
sudo yum install python3-pip -y

# Install dependencies from requirements file
pip3 install -r requirements.txt

# Run the app (replace app.py with your filename)
python3 app.py
# App runs on port 5000 (defined inside app.py)
```

### Install and Start Nginx

```bash
sudo yum install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Edit Nginx Config for Reverse Proxy

```bash
# Config file location
sudo vi /etc/nginx/nginx.conf
# Or add a new file under:
sudo vi /etc/nginx/conf.d/reverse-proxy.conf
```

### Restart Nginx After Config Change

```bash
sudo systemctl restart nginx
```

### Quick Test from CLI

```bash
curl http://<public-ip>        # should hit Nginx and get backend response
curl http://<private-ip>:5000  # direct backend test (from within VPC only)
```

---

## 🏗️ Architecture / Diagrams

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="820" height="480" style="background:#ffffff;font-family:Arial,sans-serif">

  <!-- Title -->
  <text x="410" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#1a1a2e">Nginx Reverse Proxy — Frontend/Backend Architecture</text>

  <!-- Client -->
  <rect x="20" y="80" width="120" height="60" rx="8" fill="#e8f4f8" stroke="#4a90d9" stroke-width="2"/>
  <text x="80" y="107" text-anchor="middle" font-size="13" font-weight="bold" fill="#1a1a2e">Client</text>
  <text x="80" y="125" text-anchor="middle" font-size="11" fill="#555">Browser</text>

  <!-- Arrow Client → Nginx -->
  <line x1="140" y1="110" x2="220" y2="110" stroke="#4a90d9" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="180" y="103" text-anchor="middle" font-size="10" fill="#888">HTTP :80</text>

  <!-- VPC box -->
  <rect x="210" y="55" width="580" height="400" rx="10" fill="#f9f9ff" stroke="#9b59b6" stroke-width="2" stroke-dasharray="8,4"/>
  <text x="225" y="75" font-size="12" fill="#9b59b6" font-weight="bold">VPC (10.0.0.0/16)</text>

  <!-- Public Subnet -->
  <rect x="230" y="85" width="200" height="340" rx="8" fill="#e8f8e8" stroke="#27ae60" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="330" y="103" text-anchor="middle" font-size="11" fill="#27ae60" font-weight="bold">Public Subnet</text>

  <!-- Nginx EC2 -->
  <rect x="255" y="115" width="150" height="80" rx="8" fill="#27ae60" stroke="#1e8449" stroke-width="2"/>
  <text x="330" y="142" text-anchor="middle" font-size="13" font-weight="bold" fill="#fff">Nginx EC2</text>
  <text x="330" y="159" text-anchor="middle" font-size="11" fill="#d5f5e3">Reverse Proxy</text>
  <text x="330" y="176" text-anchor="middle" font-size="10" fill="#d5f5e3">Port :80</text>

  <!-- IGW label -->
  <text x="330" y="215" text-anchor="middle" font-size="10" fill="#555">Public IP: 13.x.x.x</text>
  <text x="330" y="230" text-anchor="middle" font-size="10" fill="#555">Private IP: 10.0.0.x</text>

  <!-- Nginx config snippet -->
  <rect x="245" y="250" width="170" height="75" rx="5" fill="#f0fff0" stroke="#27ae60" stroke-width="1"/>
  <text x="330" y="267" text-anchor="middle" font-size="10" font-weight="bold" fill="#1e8449">nginx.conf</text>
  <text x="255" y="283" font-size="9" fill="#333">proxy_pass</text>
  <text x="255" y="295" font-size="9" fill="#e74c3c">http://10.0.1.x:5000</text>
  <text x="255" y="310" font-size="9" fill="#555">↑ private IP of backend</text>

  <!-- Arrow Nginx → Private EC2 -->
  <line x1="430" y1="155" x2="510" y2="155" stroke="#e74c3c" stroke-width="2" marker-end="url(#arrowred)"/>
  <text x="470" y="147" text-anchor="middle" font-size="10" fill="#e74c3c">proxy_pass</text>
  <text x="470" y="170" text-anchor="middle" font-size="10" fill="#e74c3c">:5000</text>

  <!-- Private Subnet -->
  <rect x="510" y="85" width="250" height="340" rx="8" fill="#fef9e7" stroke="#f39c12" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="635" y="103" text-anchor="middle" font-size="11" fill="#f39c12" font-weight="bold">Private Subnet</text>

  <!-- Backend EC2 -->
  <rect x="545" y="115" width="170" height="80" rx="8" fill="#e67e22" stroke="#d35400" stroke-width="2"/>
  <text x="630" y="142" text-anchor="middle" font-size="13" font-weight="bold" fill="#fff">Backend EC2</text>
  <text x="630" y="159" text-anchor="middle" font-size="11" fill="#fdebd0">Python Flask</text>
  <text x="630" y="176" text-anchor="middle" font-size="10" fill="#fdebd0">Port :5000 (private)</text>

  <text x="630" y="215" text-anchor="middle" font-size="10" fill="#555">No Public IP</text>
  <text x="630" y="230" text-anchor="middle" font-size="10" fill="#555">Private IP: 10.0.1.x</text>

  <!-- app.py snippet -->
  <rect x="545" y="250" width="175" height="75" rx="5" fill="#fef9e7" stroke="#f39c12" stroke-width="1"/>
  <text x="632" y="267" text-anchor="middle" font-size="10" font-weight="bold" fill="#d35400">app.py</text>
  <text x="555" y="283" font-size="9" fill="#333">@app.route('/message')</text>
  <text x="555" y="297" font-size="9" fill="#333">def hello():</text>
  <text x="555" y="311" font-size="9" fill="#333">  return "Hello from backend"</text>

  <!-- X mark — direct browser to backend -->
  <line x1="80" y1="200" x2="560" y2="200" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="6,3"/>
  <text x="320" y="195" text-anchor="middle" font-size="11" fill="#e74c3c">❌ Browser CANNOT reach private IP directly</text>

  <!-- Legend -->
  <rect x="230" y="360" width="510" height="75" rx="6" fill="#f5f5f5" stroke="#ccc" stroke-width="1"/>
  <text x="485" y="378" text-anchor="middle" font-size="11" font-weight="bold" fill="#333">Key Takeaway</text>
  <text x="240" y="395" font-size="10" fill="#333">✅ Browser calls Nginx public IP → Nginx proxy_pass to backend private IP → response back</text>
  <text x="240" y="412" font-size="10" fill="#333">❌ Browser calls backend private IP directly → not reachable from outside VPC</text>
  <text x="240" y="429" font-size="10" fill="#333">✅ Same VPC: Nginx EC2 ↔ Backend EC2 communicate via private IPs freely</text>

  <!-- Arrow markers -->
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#4a90d9"/>
    </marker>
    <marker id="arrowred" markerWidth="10" markerHeight="7" refX="10" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#e74c3c"/>
    </marker>
  </defs>
</svg>
```

---

## ✅ What I Practiced
- Traced request flow: client → Nginx (public EC2) → Flask app (private EC2)
- Followed deployment of Flask app on private server using `yum install python3-pip` + `pip3 install`
- Understood why hardcoding backend public IP in frontend HTML works but is not production-safe
- Understood why private IP in frontend HTML breaks when script executes in browser
- Traced Nginx upstream block config for round-robin across multiple backend IPs

---

## ❓ Questions I Still Have
- When Nginx upstream IPs change (ASG scaling), how do you update without restarting Nginx? (dynamic DNS / service discovery)
- What's the difference between Nginx and HAProxy for reverse proxy use cases?
- How does Nginx handle SSL termination before proxying to backend?

---

## ⏭️ Next Steps
- Practice: deploy Flask on private EC2, Nginx reverse proxy on public EC2, verify end-to-end
- Practice: Nginx upstream with two backend servers — confirm round-robin
- Practice: path-based routing with two upstream blocks
- Next class: S3 static hosting (pending) + likely NAT Gateway deep dive

---

## 🔗 GitHub
`https://github.com/abishaix/devops-log`

```bash
cd ~/Documents/devops-log
mv ~/Downloads/day-21-nginx-reverse-proxy.md notes/
git add notes/day-21-nginx-reverse-proxy.md README.md
git commit -m "docs: add day 21 notes - nginx reverse proxy and frontend/backend architecture"
git push origin main
```
