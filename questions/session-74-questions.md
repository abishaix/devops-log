# Session 74 — Questions

- For the route table association resource — if a subnet is accidentally associated with two different route tables via two separate `aws_route_table_association` resources, does AWS/Terraform reject that outright, or does one silently take priority (and if so, which)?

- The `.tfstate.backup` file only holds one step back — is there a built-in Terraform way to keep more than one prior version locally, or is that entirely what the S3 bucket versioning from session-72 is for, making the local `.backup` file basically redundant once state lives remotely?

- With `-target`, if the targeted resource actually depends on another resource that hasn't been created yet (e.g., targeting the subnet before the VPC exists), does Terraform automatically pull in that dependency anyway, or does it just fail since the dependency is out of scope for this run?
