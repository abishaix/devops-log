# Session 72 — Questions

- If two teammates run `terraform apply` at nearly the same time against the same S3 backend, what actually stops a race condition — is bucket versioning alone enough, or is a lock (DynamoDB table, or native S3 locking) required for that specific problem?

- For the inline-block drift behavior — if a security group mixes inline `ingress {}` blocks in the `aws_security_group` resource with separate standalone `aws_security_group_rule` resources for the *same* SG, does Terraform error out on the conflict, or does one silently win?

- Does the default destroy-then-create replacement apply to every attribute that forces replacement, or only some? Are there resource types where `create_before_destroy` is actually unsafe to turn on (e.g., something with a globally unique name that can't exist twice at once)?
