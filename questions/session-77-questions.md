# Session 77 — Questions

- If a module lives on GitHub and I call it with `source = "github.com/org/repo//path"`, does Terraform clone the entire repo on every `apply`, or does it cache the module locally after the first pull — and if it's cached, how does it know to re-pull when the module source itself gets updated upstream?

- With each caller getting its own independent state file, if I want to know later "which environments are actually using this module version," is that something Terraform tracks anywhere, or is it entirely on the team to keep a manual record since state files don't reference each other?

- The IAM user leftover inside the EC2 module caused errors even though the caller only passed EC2-related values — but what if the unrelated resource had no required arguments and would have applied cleanly with defaults? Would that fail silently (an IAM user quietly created that nobody asked for), or does Terraform still surface it in the plan output as something to notice?

- For a multi-resource module like the S3 one (bucket + versioning + ownership + ACL as separate blocks) — if I only want the bucket and skip everything else, do I just not pass values for those features, or does the module need internal conditional logic (like `count` or a boolean flag) to actually skip creating those resource blocks?

- When browsing the official Terraform Registry S3 module and seeing ~1500 lines covering "all requirements," is there a practical downside to always reaching for the fullest-featured public module versus writing a smaller, team-specific one — extra complexity, slower plans, harder to audit what's actually being created?

- Local relative-path sourcing (`../day9-modules/ec2-module`) only works because everything is on the same machine — once that gets pushed to GitHub and called with a GitHub source instead, does the local relative-path version still work as a fallback, or does the module block need to be rewritten entirely to switch source types?
