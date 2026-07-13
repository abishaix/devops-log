# Session 73 — Questions

- If both S3 native locking (`use_lockfile = true`) and a DynamoDB `lock_table` are configured on the same backend at once, and it just produces a "duplicated" warning rather than an error — is there an actual precedence (does one win), or is it purely redundant and should just be cleaned up to avoid confusion?

- Does `terraform force-unlock` work the same way against an S3-native lock as it does against a DynamoDB lock entry, or is the underlying lock ID/mechanism different enough that the safety considerations change between the two?

- The "day-04/terraform.tfstate" vs "day-05/terraform.tfstate" key-path pattern shown here — is that specifically a training workaround for reusing one practice bucket across days, or is that genuinely how real projects namespace state per environment (dev/staging/prod) inside a single bucket? And if so, how does that compare to just using Terraform workspaces for the same purpose?
