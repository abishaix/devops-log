# Lab 20 — Prometheus + AlertManager + PagerDuty Monitoring Stack

- **Date:** July 5, 2026
- **Region:** us-east-1 (N. Virginia)
- **Resources:** 2× EC2 t2.medium (Ubuntu 26.04), 1 security group, PagerDuty free-trial account (Events API v2)
- **Repo source scripts:** `github.com/abishaix/Monitoring-Alerting` (`node.sh`, `grafna-promethous.sh`)

---

## Contents

- [What I Built](#what-i-built)
- [Architecture](#architecture)
- [Infrastructure Summary](#infrastructure-summary)
- [Part 1 — Node Exporter on Target-Server](#part-1--node-exporter-on-target-server)
- [Part 2 — Monitoring Stack on Monitoring-Server](#part-2--monitoring-stack-on-monitoring-server)
- [Part 3 — Security Group Rules](#part-3--security-group-rules)
- [Part 4 — PagerDuty Integration](#part-4--pagerduty-integration)
- [Part 5 — Alert Rules](#part-5--alert-rules)
- [Scenario A — InstanceDown](#scenario-a--instancedown)
- [Scenario B — HighCPUUsage](#scenario-b--highcpuusage)
- [Troubleshooting & Notes](#troubleshooting--notes)
- [Cleanup](#cleanup)
- [Cost](#cost)

---

## What I Built

A two-node Prometheus monitoring stack with end-to-end alerting to PagerDuty. A **Target-Server** runs node_exporter; a **Monitoring-Server** runs Prometheus, AlertManager, Grafana, and a self-monitoring node_exporter. Prometheus scrapes both hosts over private networking (static targets), evaluates three alert rules, and on firing hands off to AlertManager, which routes to PagerDuty over Events API v2 — creating an incident and email notification.

Two alert scenarios were driven to completion:

1. **InstanceDown** — stopped the target EC2, watched `up == 0` go PENDING → FIRING → PagerDuty incident.
2. **HighCPUUsage** — loaded CPU on the target, watched the idle-based rule go PENDING → FIRING → PagerDuty incident, cross-checked against CloudWatch.

The install was script-driven (cloned repo + `sh node.sh`, `sh grafna-promethous.sh`) rather than manual binary steps.

---

## Architecture

### ASCII flow

```
stress --cpu (target)          node_server DOWN (target stopped)
        │                               │
        ▼                               ▼
node_exporter :9100 ──scrape (15s)──► Prometheus :9090
                                         │ evaluate system-alerts
                                         │   InstanceDown  up == 0            for 1m
                                         │   HighCPUUsage  idle-based > 40    for 2m
                                         │   HighDiskUsage fs used > 80       for 2m
                                         ▼ FIRING
                                     AlertManager :9093
                                         │ route → receiver: pagerduty
                                         ▼ Events API v2 (routing_key)
                                     PagerDuty (alert-abnormality)
                                         ▼
                                     incident + email → on-call
```

### Hand-drawn (draw.io)

![Hand-drawn architecture](../screenshots/lab-20/lab-20-27-architecture-diagram.png)

### Generated SVG

![Monitoring stack architecture](../diagrams/lab-20-prometheus-monitoring-stack.svg)

---

## Infrastructure Summary

| Resource | Name | Type | Notes |
|---|---|---|---|
| EC2 (target) | node_server | t2.medium, Ubuntu 26.04 | node_exporter :9100; public 98.89.29.27 / private 172.31.24.199 |
| EC2 (monitoring) | graf_server / grafana-prometheus | t2.medium, Ubuntu 26.04 | Prometheus, AlertManager, Grafana, node_exporter; public 52.91.242.133 / private 172.31.29.156 |
| Security group | graf-pro (sg-02aec8d18334ec28e) | — | inbound: 9090, 9100, 3000, 9093, SSH 22 |
| PagerDuty service | alert-abnormality | Events API v2 | Prometheus integration; escalation policy alert-abnormality-ep |

Both instances in the same VPC; Prometheus scrapes the target over its private IP.

---

## Part 1 — Node Exporter on Target-Server

Cloned the install repo and ran the node script on the target:

```bash
git clone https://github.com/abishaix/Monitoring-Alerting.git
cd Monitoring-Alerting
sh node.sh
```

`node.sh` installs node_exporter and registers it as a systemd service on :9100. Verified by browsing to `http://98.89.29.27:9100` — the Node Exporter landing page (version 1.8.2) with a Metrics link confirms it's serving.

![Clone repo and run node script](../screenshots/lab-20/lab-20-01-clone-run-node-script.png)
![Node exporter web page](../screenshots/lab-20/lab-20-02-node-exporter-web.png)
![Node exporter :9100](../screenshots/lab-20/lab-20-03-node-exporter-9100.png)

---

## Part 2 — Monitoring Stack on Monitoring-Server

On the monitoring host, ran the stack script:

```bash
cd Monitoring-Alerting
sh grafna-promethous.sh
```

The script installs Prometheus, Grafana, AlertManager, and node_exporter, then creates and enables all four systemd services. Completion banner prints the three UI endpoints:

- Prometheus `http://<server-ip>:9090`
- Grafana `http://<server-ip>:3000`
- AlertManager `http://<server-ip>:9093`

![Install monitoring stack](../screenshots/lab-20/lab-20-08-install-monitoring-stack.png)
![Install completed](../screenshots/lab-20/lab-20-09-install-completed.png)

---

## Part 3 — Security Group Rules

Security group `graf-pro` inbound rules, named per service — prometheus (9090), node-exporter (9100), grafana (3000), alert-manager (9093), plus SSH (22).

![SG inbound rules](../screenshots/lab-20/lab-20-10-sg-inbound-rules.png)
![SG rules with alertmanager](../screenshots/lab-20/lab-20-11-sg-rules-alertmanager.png)

> **Networking note (SG-referencing-SG):** node_exporter :9100 on the target only needs to be reachable from the monitoring server. In a hardened build, the target's SG allows 9100 sourced from the monitoring server's SG (not 0.0.0.0/0) — the inbound rule lives on the target, trusting the monitoring SG. Same methodical component-elimination pattern as tracing a Meraki AP switchport at work.

---

## Part 4 — PagerDuty Integration

Created a PagerDuty service `alert-abnormality` and added a **Prometheus** integration (Events API v2). Copied the 32-char **Integration Key** and wired it into `alertmanager.yml` as the `routing_key`.

AlertManager config (routing_key redacted):

```yaml
route:
  receiver: pagerduty
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h

receivers:
  - name: pagerduty
    pagerduty_configs:
      - routing_key: "<REDACTED>"
        severity: "critical"
```

AlertManager systemd unit runs as user `prometheus` with `--config.file=/etc/alertmanager/alertmanager.yml` and `--storage.path=/var/lib/alertmanager`.

![PagerDuty create service integration](../screenshots/lab-20/lab-20-04-pagerduty-prometheus-integration.png)
![PagerDuty integration key](../screenshots/lab-20/lab-20-05-pagerduty-integration-key.png)
![Integration key on-call](../screenshots/lab-20/lab-20-06-integration-key-oncall.png)
![alertmanager.yml config](../screenshots/lab-20/lab-20-07-alertmanager-yml-config.png)

> **Security:** the routing key was visible in several screenshots during the lab. Since this repo is public, that key was rotated in PagerDuty after the lab. Never commit a live routing key.

---

## Part 5 — Alert Rules

Rule group `system-alerts` in `/etc/prometheus/alert.rules.yml`, three rules:

| Alert | Expression | for | severity |
|---|---|---|---|
| InstanceDown | `up == 0` | 1m | critical |
| HighCPUUsage | `100 - (avg by (instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 40` | 2m | critical |
| HighDiskUsage | `(1 - (node_filesystem_avail_bytes{fstype!~"tmpfs\|overlay"} / node_filesystem_size_bytes{fstype!~"tmpfs\|overlay"})) * 100 > 80` | 2m | warning |

All three load in Status → Rules with state OK, evaluation interval 1m.

![Prometheus rules loaded](../screenshots/lab-20/lab-20-12-prometheus-rules-loaded.png)
![Prometheus alerts inactive](../screenshots/lab-20/lab-20-13-prometheus-alerts-inactive.png)

> **Rule / annotation mismatch (as-built, left uncorrected):** the HighCPUUsage `expr` threshold is `> 40`, but its `description` annotation text reads "CPU usage > 20%". These disagree in the deployed rule — the expression is authoritative (fires at >40% idle-inverted). Recording as-is; worth aligning the annotation to the real threshold in a follow-up.

---

## Scenario A — InstanceDown

Stopped `node_server` from the EC2 console. Prometheus lost the scrape target, `up` for that instance went to 0.

1. **Baseline** — CPU query on the target returned ~0.19%, well under the HighCPU threshold, so HighCPU stayed inactive (correct — isolates the InstanceDown signal).
2. **PENDING** — InstanceDown entered PENDING while the `for: 1m` timer ran.
3. **FIRING** — after 1m, state flipped to FIRING (active since `2026-07-05T10:40:49Z`), labels `alertname=InstanceDown instance=node_server job=ec2-node-exporters severity=critical`.
4. **PagerDuty** — incident `#1 [FIRING:1] (InstanceDown node_server ec2-node-exporters critical)`, High urgency, triggered; email received with the firing details (`summary: Instance node_server is down`).

![CPU not triggered (baseline)](../screenshots/lab-20/lab-20-14-promql-cpu-not-triggered.png)
![node_server stopping](../screenshots/lab-20/lab-20-15-ec2-node-server-stopping.png)
![InstanceDown pending](../screenshots/lab-20/lab-20-16-instancedown-pending.png)
![InstanceDown firing](../screenshots/lab-20/lab-20-17-instancedown-firing.png)
![PagerDuty email](../screenshots/lab-20/lab-20-18-pagerduty-triggered-email.png)
![PagerDuty incident triggered](../screenshots/lab-20/lab-20-19-pagerduty-instancedown-triggered.png)

---

## Scenario B — HighCPUUsage

Restarted the target, then loaded its CPU (`stress`) to push idle-inverted usage above 40%.

1. **Low** — CPU query first showed ~0.19% (idle, no load).
2. **High** — under load the query returned ~73%, above the 40% threshold.
3. **PENDING** — HighCPUUsage entered PENDING (active since `2026-07-05T11:24:49Z`, value 100), `for: 2m` timer running.
4. **FIRING** — after 2m, FIRING; AlertManager UI showed the alert grouped under the `pagerduty` receiver with description "CPU usage > 20% for more than 2 minutes. VALUE = 100%", summary "High CPU usage detected on node_server".
5. **CloudWatch cross-check** — EC2 CloudWatch CPU utilization for `i-03870620805c25840 (node_server)` confirmed the load spike independently.
6. **PagerDuty** — incident `#2 [FIRING:1] (HighCPUUsage node_server critical)`, High urgency, triggered on service alert-abnormality.

![CPU low](../screenshots/lab-20/lab-20-20-promql-cpu-low.png)
![CPU high ~73%](../screenshots/lab-20/lab-20-21-promql-cpu-high.png)
![CloudWatch CPU](../screenshots/lab-20/lab-20-22-cloudwatch-cpu.png)
![HighCPU pending](../screenshots/lab-20/lab-20-23-highcpu-pending.png)
![AlertManager active alert](../screenshots/lab-20/lab-20-24-alertmanager-active-alert.png)
![HighCPU firing](../screenshots/lab-20/lab-20-25-highcpu-firing.png)
![PagerDuty HighCPU triggered](../screenshots/lab-20/lab-20-26-pagerduty-highcpu-triggered.png)

---

## Troubleshooting & Notes

- **Verify locally, then outward.** CPU expression tested directly in the Prometheus Graph tab before trusting the alert — the query returning a value (73%) above threshold confirms the metric pipeline before AlertManager/PagerDuty are in the picture.
- **PENDING vs FIRING.** PENDING means the expression is already true but the `for:` timer hasn't elapsed. It's not a failure — it's the debounce that stops flapping alerts from paging. InstanceDown (1m) pages faster than HighCPUUsage (2m) by design.
- **The `up` metric** is the cheapest, most reliable health signal — `up == 0` needs no exporter-specific metric, just a failed scrape.
- **AlertManager handoff check** (if PagerDuty stays quiet): `curl -s localhost:9093/api/v2/alerts` and `journalctl -u alertmanager`. A 202 from PagerDuty means accepted; a 4xx usually means a bad routing_key.

---

## Cleanup

```bash
```

Deletion order (dependencies first):

1. Terminate `node_server` and `graf_server` — wait for Terminated state.
2. Delete security group `graf-pro` (after both instances terminated).
3. Resolve the PagerDuty test incidents (#1 InstanceDown, #2 HighCPUUsage).
4. Rotate/delete the PagerDuty Events API v2 routing key (exposed in lab screenshots).

Default VPC left in place.

---

## Cost

Two `t2.medium` instances are **not** free-tier (free tier is t2.micro/t3.micro). Running two t2.medium (~$0.0464/hr each in us-east-1) for a few hours is roughly $0.20–0.40 total. No NAT Gateway, ALB, or RDS. PagerDuty on free trial. Terminate promptly — the t2.medium sizing is the only meaningful cost here.
