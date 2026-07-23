# Session 79 — Terraform: User Data Behavior, Provisioners Intro, Taint
**Date:** July 21, 2026

## Recap: fmt / validate
- `terraform fmt` — reformats/aligns `.tf` files. Must be run **inside the directory containing the files** or it silently does nothing.
- `terraform validate` — checks syntax only. Not strictly necessary before `plan`/`apply` since a syntax error surfaces there anyway, but useful to isolate a syntax problem from a logic problem.

## Data sources — avoiding hardcoded values
- A `data` block looks up an existing resource (AMI, subnet, etc.) using filters, instead of hardcoding an ID in the `.tf` file.
- Example: an AMI `data` block with filters returns whichever AMI matches at apply time — no AMI ID committed to the repo.
- Same idea for subnet IDs — reference via a `data` lookup rather than a literal subnet ID, so nothing sensitive/environment-specific is hardcoded in version control.

## State file corruption — what actually happens
- If using an S3 backend: enable **bucket versioning** on the state bucket. A corrupted/bad state can be rolled back to a previous version.
- Local backend: keep local backup versions.
- State locking (already covered previously) reduces the chance of corruption from concurrent writes in the first place.
- Bottom line: state corruption is rare and recoverable — not something to panic over if versioning/locking are in place.

## EC2 user_data — critical behavior lesson
- `user_data` scripts run **once**, only at instance **launch** (cloud-init), via the `bin/bash` shebang block in advanced instance details.
- **Editing user_data after launch does nothing** — confirmed by live test:
  1. Instance launched with a broken `user_data` (typo in install command) → command not found.
  2. Stopped instance, edited user_data, restarted → script still did not re-run. AWS lets you edit the field on a stopped instance, but that doesn't mean it re-executes.
  3. Tried `cloud-init clean` + reboot (a ChatGPT-suggested fix) → this **wiped SSH host keys, authorized_keys, and network config**, locking out all existing connections. Confirmed working technically, but explicitly **not recommended** — even the AI giving the suggestion flagged it as unsafe in the same breath.
- **Correct approach when user_data needs to change: terminate and recreate the instance** (blue/green style) — same key pair, same subnet, same config, fresh instance. Don't try to force a re-run on a live instance.
- Lesson explicitly called out: never run an AI-suggested remediation command blindly in a shared/production environment — test in an isolated sandbox account first. A mistake here only affects your own practice account; in production the same command could disconnect 100 people across teams.

## user_data via Terraform
- Same script, two ways to provide it in the `aws_instance` resource:
  - Inline heredoc block directly in the resource.
  - `user_data = file("user_data.sh")` — references an external script file, same result as uploading a script manually in the console's advanced details.

## Provisioners — the four types
| Provisioner | Runs where | Notes |
|---|---|---|
| `local-exec` | The machine running `terraform apply` (laptop, CI runner) | For actions that don't touch the remote server at all |
| `remote-exec` | Target server, over SSH | Needs a `connection` block to authenticate |
| `file` | N/A (transfer step) | Copies a local file to the remote server before a `remote-exec` step uses it |
| `null_resource` | N/A — state-tracking wrapper | Covered in depth in Session 80 |

### connection block requirements
- `private_key` — path to the local private key (e.g. `~/.ssh/id_rsa`)
- `user` — `ubuntu` for Ubuntu AMIs, `ec2-user` for Amazon Linux
- `host` — `self.public_ip` (or `aws_instance.server.public_ip` referencing the resource explicitly)

### Key pair via Terraform, using an existing local key
- Instead of generating a brand-new key pair, an `aws_key_pair` resource can reference an **existing local public key** (`~/.ssh/id_rsa.pub`), so the matching private key already on the local machine can be used to connect — fully automated, no manual key generation step.

### Live example — local-exec / file / remote-exec together
- `local-exec`: created a file (`file500`) on the **local** machine (where `terraform apply` runs) — proves this step never touches the server.
- `file` provisioner: copied a local file (`file10`) to the remote server's home directory.
- `remote-exec`: ran an inline script on the remote server (`echo ... > file200`) — proves this step only touches the server, not local.
- Confirmed by SSHing into the server afterward: `file10` (from `file` provisioner) and `file200` (from `remote-exec`) both present remotely; `file500` only exists locally.

## Provisioners are NOT tracked by state
- Modifying a provisioner's command and re-running `terraform plan` shows **no changes** — state only tracks the parent AWS resource (e.g. the EC2 instance), not what's inside its provisioner blocks.
- Confirmed live: changed the `remote-exec` inline command, ran `plan` → 0 changes reported, even though the script content differed from what was last applied.

## terraform taint / untaint
- `terraform taint <resource address>` manually marks a resource for **destroy + recreate** on the next `apply`, regardless of whether its config changed.
- `terraform plan` after tainting shows `1 to add, 1 to destroy` with reason `"tainted; must be replaced"`.
- `terraform untaint <resource address>` reverses this — back to `0 changes` if nothing else changed.
- This is the (blunt) tool available today to force a provisioner rerun, since provisioners aren't independently tracked — tainting recreates the whole resource just to re-trigger the provisioner blocks attached to it.

## Preview — next session
- Wrapping provisioner logic in a separate `null_resource` block (rather than inside the instance block) makes Terraform track that logic as its own resource in state, without forcing the EC2 instance itself to be destroyed/recreated just to rerun a script. Full detail + triggers in Session 80.
