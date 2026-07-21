# Session 78 — Questions

1. When importing a resource, if an attribute is computed-only (set by AWS at creation, not settable in config — like an ARN or a generated ID), does `terraform plan` still flag it as a diff, or does Terraform know to skip computed fields automatically?

2. If two developers both run `terraform import` on the same manually-created resource into their own local state files before either pushes to the shared S3 backend, what happens when the second one pushes — does it error, overwrite, or silently create two conflicting state entries?

3. Does `ignore_changes` only suppress drift going forward, or does it also retroactively stop Terraform from flagging drift that was already recorded in state from a previous `plan` before the lifecycle block was added?

4. With `create_before_destroy` on a resource that has a global uniqueness constraint (like an S3 bucket name or an EIP), how does Terraform create the replacement first if the name/identifier can't exist twice at once?

5. If a `data` block's filter matches more than one resource (e.g. two subnets both tagged the same name by accident), does `terraform plan` error out immediately, or does it silently pick one and proceed?
