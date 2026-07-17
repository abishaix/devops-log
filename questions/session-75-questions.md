# Session 75 — Questions

- If `publicly_accessible = true` but I never intend to connect from outside the VPC, is there any downside to just leaving it `false` and always going through a bastion or SSM instead — even in a lab? Or does something else in the stack quietly assume public access?

- The DB subnet group needs 2 AZs even for a single-AZ instance. If I only ever run one instance and never plan to go Multi-AZ, is that AZ diversity requirement purely an AWS API constraint, or does RDS actually use the second AZ for something even in single-instance mode?

- For the `for_each` route table association fix — if I add a third subnet to the VPC later, does that new subnet automatically pick up the association just by being added to the `locals` list, or do I have to touch the `aws_route_table_association` resource itself too?

- When the read replica's `replica_source_db` needs the primary's ARN instead of its identifier, is that specific to when a DB subnet group is attached, or is ARN always required for replicas and it only became visible as an error once a subnet group entered the picture?

- The DNS hostnames setting was off in the custom VPC but on by default in the default VPC — is that difference AWS-wide, or could a custom VPC template/module ever ship with it pre-enabled, and I just got unlucky with this specific `aws_vpc` block?

- With `manage_master_user_password = true` handing credentials to Secrets Manager, does Terraform's state file still end up storing the password in plaintext anywhere, or is that exactly the problem this flag is meant to avoid?

- In the multi-developer drift scenario (someone deletes the S3 bucket manually, first apply wins and recreates it) — what happens if both developers run `apply` at nearly the same time? Is that where S3 native locking from session-73 actually kicks in, or is drift recreation a separate mechanism from the locking discussion entirely?
