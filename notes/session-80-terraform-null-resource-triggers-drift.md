# Session 80 — Terraform: null_resource, Triggers, Drift
**Date:** July 22, 2026

## Why null_resource exists
- Provisioners (`local-exec`, `remote-exec`, `file`) live inside a `resource` block, but **Terraform state does not track what they do** — only whether the parent AWS resource itself changed (confirmed live in Session 79).
- If you change a provisioner's script/command with no other config change, `terraform plan` shows **zero changes** — Terraform doesn't know the script changed.
- `null_resource` is a dummy resource that Terraform *does* track in state, purely so you have something to attach provisioners/triggers to without touching real infrastructure (e.g. an EC2 instance).
- Putting provisioners directly in the EC2 resource block means any forced change there (e.g. via `taint`) destroys and recreates the **server itself**. Isolating them in a `null_resource` means only the null_resource gets destroyed/recreated — the EC2 instance is untouched.

## Triggers
- `null_resource` supports a `triggers` block to force re-execution.
  - **Timestamp trigger** (`timestamp()`): reruns the provisioner on *every* `terraform apply`, regardless of whether anything changed. Destroys and recreates the null_resource each time.
  - **Script hash trigger** (`filemd5()` / similar over the script file): only reruns when the actual script content changes — Terraform compares the hash to what's stored in state. Preferred over timestamp — avoids unnecessary reruns on every apply.
- Confirmed live: after switching to a timestamp trigger, `terraform plan` always showed `1 to add, 1 to destroy` for the null_resource, even with zero config changes. After switching to a hash trigger, `plan` showed `0 changes` when the script was untouched, and `1 to add, 1 to destroy` only once the script content actually changed (hash value changed in state).

## Terraform drift
- Drift = difference between your local `.tf` config and the actual remote state, caused by **manual out-of-band changes** (someone edited something directly in the console).
- Signature: `terraform plan` shows changes **you didn't author** — e.g. you expected "9 to add" but see "1 modify, 1 destroy" that doesn't match your config diff.
- Not drift: plan output that matches exactly what you changed in the file.

## local-exec vs remote-exec vs file provisioner
| Provisioner | Runs where | Use case |
|---|---|---|
| `local-exec` | Machine running `terraform apply` (your laptop/CI runner) | Needs local tooling installed (e.g. `mysql` client) to reach a **public** RDS endpoint directly |
| `file` | N/A (copy step) | Copies a local file (e.g. `init.sql`) onto a remote instance before running a script there |
| `remote-exec` | Target server (via SSH, needs a `connection` block) | Runs commands **on** the EC2 instance — e.g. install a package, then execute a script |

Ordering matters: `connection` block → `file` provisioner (copy script) → `remote-exec` (run it). Putting `file` inside `remote-exec` or vice versa produces an error.

### Worked example — RDS + local-exec
- Create RDS → `null_resource` with `local-exec` running `mysql -h <endpoint> -u admin -p... < init.sql` from the machine running Terraform.
- Only works if RDS is **publicly reachable** and the local machine has the `mysql` client installed — Terraform doesn't install it for you. The null_resource fails with "command not found" if the client is missing locally.
- Confirmed live: running without the MySQL client installed locally produced exactly this failure — RDS resource itself succeeded, only the null_resource (local-exec step) failed. Plan afterward showed `2 to add` (RDS + null_resource each count as a resource).

### Worked example — remote-exec variant
- Needs an EC2 instance (with key pair + `connection` block) in between: copy `init.sql` via `file` provisioner, then run `mysql ... < /tmp/init.sql` via `remote-exec`, after installing the client (e.g. `apt install mariadb-client -y`).
- Sudo requirement: EC2 default user has sudo available, but commands must **explicitly** invoke it — omitting `sudo` produced a "permission denied" error on the package install step (e.g. `apt-get` lock file).
- Confirmed live: forgetting `sudo` on `apt-get install` failed with a lock-file permission error; adding `sudo` fixed it.

## Autoscaling groups & Lambda — scope boundary
- Terraform's responsibility ends at **provisioning**. It creates the ASG with your launch template + min/max settings — it does not manage instance count changes, scaling events, or crashes from undersized max capacity. That's the ASG's own runtime behavior, not Terraform's.
- Same logic for Lambda: Terraform configures the function and its schedule/event source. If the schedule expression or event pattern is wrong, that's a configuration error, not something Terraform is responsible for at runtime.

## Practical notes
- No fixed rule on how many provisioners to use per project — use only what the requirement demands (don't force `file` + `local-exec` + `remote-exec` if you don't need all three).
- `terraform taint` (from Session 79) remains the manual override to force destroy+recreate on any resource, independent of triggers.
- Instructor's course-progress signal: Terraform expected to wrap in ~4 more sessions from this point; CI/CD next (~1 week/8 days); then Maven/SonarQube (~2 days each, developer-owned tools); Docker + Kubernetes projected to take through ~October given the batch's pace.
