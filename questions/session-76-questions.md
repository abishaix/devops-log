# Session 76 — Questions

- If the sandbox tears down resources every 8 hours and `terraform plan` just quietly recreates everything on the next run, is there any way to notice *before* running plan/apply that the remote is gone — or is refreshing state genuinely the only signal, meaning drift can sit unnoticed for the whole 8-hour window?

- `source_code_hash` tracks the zip file's hash so Terraform can detect code changes — but does it hash the zip's compressed bytes, or the contents inside it? If I re-zip the exact same source with a different compression tool or timestamp, would the hash change even though the code itself didn't?

- For the trust policy vs. permissions split on the IAM role — if I attach two different policies to the same Lambda role (basic execution plus something custom), does Terraform apply them in any particular order, or does that not matter since they're just permissions layered onto the same role regardless of attachment sequence?

- The EventBridge setup needed three resources — rule, target, and permission. Is the `aws_lambda_permission` block specifically required because EventBridge is a different AWS account/service boundary invoking the function, or would any trigger source (S3, API Gateway, etc.) need that same explicit permission resource?

- With implicit dependency detection working off attribute references, what happens if I reference `aws_iam_role.lambda_role.name` in one resource and `aws_iam_role.lambda_role.arn` in another — does Terraform still recognize both as depending on the same role, or does it matter which attribute is referenced for the dependency graph to pick it up?

- For the homework (S3-based Lambda deployment) — once the code lives in S3 instead of being uploaded directly, does `source_code_hash` still work the same way, or does S3-sourced Lambda code need a different change-detection mechanism since Terraform isn't holding the zip file locally anymore?
