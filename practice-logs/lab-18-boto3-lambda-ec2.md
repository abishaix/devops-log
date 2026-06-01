# Practice Log — Boto3 & Lambda: Create EC2 with Python

**Date:** June 1, 2026
**Resources Created:** EC2 instances (via Boto3 locally + via Lambda), Lambda function, IAM role with EC2FullAccess
**Region:** us-west-2

---

## Contents

- [What I Built](#what-i-built)
- [Architecture Diagrams](#️-architecture-diagrams)
- [Part 1 — Boto3 Locally](#part-1--boto3-locally)
- [Part 2 — Boto3 in Lambda](#part-2--boto3-in-lambda)
- [Key Observations](#key-observations)
- [Mistakes & Fixes](#-mistakes--fixes)
- [Cleanup](#-cleanup)
- [Screenshots](#-screenshots)

---

## What I Built

Two approaches to creating an EC2 instance programmatically using Python and Boto3:

1. **Local script** — ran Python directly from VS Code on Mac, authenticated via `aws configure`, created and terminated an EC2 instance
2. **Lambda function** — same boto3 code wrapped in a Lambda handler, authenticated via IAM role, triggered via test event

---

## 🏗️ Architecture Diagrams

**Hand-drawn:**

![Boto3 flow diagram](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/boto3-flow-diagram.png)

![Lambda architecture diagram](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/lambda-architecture-diagram.png)

---

## Part 1 — Boto3 Locally

### Setup

Install boto3 and configure AWS credentials:

```bash
pip3 install boto3
aws configure
```

`aws configure` prompts for Access Key ID, Secret Access Key, region (`us-west-2`), and output format (`json`). Credentials are stored in `~/.aws/credentials`.

Verify:

```bash
aws configure list
```

### Create EC2 — `create_ec2.py`

```python
import boto3

client = boto3.client('ec2', region_name='us-west-2')

response = client.run_instances(
    ImageId='ami-029a761f237195c2c',
    InstanceType='t3.micro',
    MinCount=1,
    MaxCount=1
)

print(response)
print(response['Instances'][0]['InstanceId'])
```

Run:

```bash
python3 create_ec2.py
```

Output confirmed instance ID: `i-0158e4fac75cfebdf`

Note: `t2.micro` is not available in `us-west-2` — AWS automatically used `t3.micro`.

### Terminate EC2 — `terminate_ec2.py`

```python
import boto3

def terminate_instance(instance_id):
    client = boto3.client('ec2', region_name='us-west-2')
    response = client.terminate_instances(InstanceIds=[instance_id])
    print(response)

terminate_instance('i-0158e4fac75cfebdf')
```

Response confirmed:

```
PreviousState: running
CurrentState: shutting-down
```

---

## Part 2 — Boto3 in Lambda

### Lambda Function Code

```python
import json
import boto3

def lambda_handler(event, context):
    client = boto3.client('ec2', region_name='us-west-2')
    response = client.run_instances(
        ImageId='ami-029a761f237195c2c',
        InstanceType='t3.micro',
        MinCount=1,
        MaxCount=1
    )
    instance_id = response['Instances'][0]['InstanceId']
    print('Instance created:', instance_id)

    return {
        'statusCode': 200,
        'body': json.dumps('Instance created: ' + instance_id)
    }
```

### Lambda Configuration

| Setting | Value |
|---|---|
| Runtime | Python 3.x |
| Handler | `create_ec2.lambda_handler` |
| Timeout | 30 seconds |
| Memory | 128 MB |
| Execution role | `myec2-fuction-role-3u8trov8` with `AmazonEC2FullAccess` |

### Test Result

```json
{
  "statusCode": 200,
  "body": "\"Instance created: i-008e41bc852b1087d\""
}
```

- **Duration:** 4.9 seconds
- **Billed:** 5.2 seconds — only paid for actual execution time
- Verified instance running in EC2 console ✅

### Lambda Flow

```
Test Event → Lambda Function → IAM Role (EC2FullAccess) → AWS API (us-west-2) → EC2
```

Lambda runs outside the VPC — it hits the AWS API directly in the region. No VPC configuration needed to create EC2 instances via API.

---

## Key Observations

**Boto3 locally vs Lambda — what actually changed:**

| | Local (VS Code) | Lambda |
|---|---|---|
| Auth | `~/.aws/credentials` | IAM role attached to function |
| Trigger | `python3 script.py` | Test event / schedule / trigger |
| Entry point | Top of script | `lambda_handler(event, context)` |
| Billing | EC2 running cost | 5.2 seconds of Lambda compute |
| OS/runtime | Managed by you | Managed by AWS |

The boto3 API calls themselves are identical — only the wrapper and auth method change.

---

## 🐛 Mistakes & Fixes

**1. Region set as AZ**
`aws configure` was set to `us-west-2a` (AZ) instead of `us-west-2` (region). Fixed by rerunning `aws configure`.

**2. Lambda handler mismatch**
File was named `create_ec2.py` but Lambda defaulted to looking for `lambda_function.py`. Fixed by updating handler in Configuration → General configuration to `create_ec2.lambda_handler`.

**3. Lambda timeout**
Default 3-second timeout was too short for the EC2 API call. Fixed by increasing to 30 seconds in Configuration → General configuration.

**4. IAM role missing EC2 permissions**
Lambda execution role had no EC2 permissions — function timed out trying to call the API. Fixed by attaching `AmazonEC2FullAccess` to the role in IAM.

**5. Wrong response key in Lambda code**
Used `response['TerminatingInstances']` in a `run_instances` call. Correct key is `response['Instances']`.

---

## 🧹 Cleanup

1. Terminate EC2 instance `i-008e41bc852b1087d` — via console or terminate script
2. Delete Lambda function `myec2-fuction`
3. Delete IAM role `myec2-fuction-role-3u8trov8` or remove `AmazonEC2FullAccess` policy
4. Delete access key from IAM → Users → Security credentials if no longer needed

---

## 📸 Screenshots

![Lambda create EC2 code](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/lambda-create-ec2-code.png)

![Lambda deploy success](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/lambda-deploy-success.png)

![Lambda test timeout IAM issue](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/lambda-test-timeout-iam-issue.png)

![Lambda role EC2 full access](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/lambda-role-ec2-fullaccess.png)

![Lambda timeout config 3sec](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/lambda-timeout-config-3sec.png)

![Lambda test success EC2 created](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/lambda-test-success-ec2-created.png)

![EC2 created by Lambda](https://github.com/abishaix/devops-log/raw/main/screenshots/lab-18/ec2-created-by-lambda.png)
