# TicketMe Deployment Guide

Complete, from-scratch setup instructions for deploying TicketMe to your own AWS account.

## Prerequisites

- AWS account with an IAM user (not root) with appropriate permissions
- AWS CLI v2, configured (`aws configure`)
- Terraform >= 1.5.0
- Python 3.12 available (for local Lambda package builds; separate from your general dev Python version)
- Git

## 1. Clone the repository

```powershell
git clone https://github.com/Fiber-dunstan/TICKETME.git
cd TICKETME
```

## 2. Set up the Python environment (for tests and local scripts)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

## 3. Run the backend test suite

```powershell
pytest tests/ -v
```

All 14 tests should pass before proceeding — this confirms the Lambda logic itself is correct, independent of any AWS deployment.

## 4. Configure Terraform variables

Create `infrastructure/terraform.tfvars` (this file is gitignored — never commit it):

```hcl
alert_email          = "your-email@example.com"
monthly_budget_limit  = "5"
```

`alert_email` is required — it receives SNS operational alerts, registration confirmations, and AWS Budget notifications.

## 5. Build the Lambda deployment packages

```powershell
.\scripts\build_lambda_packages.ps1
```

This combines each handler's code with shared utilities into `build/`, ready for Terraform to zip and upload. Re-run this any time backend code changes.

## 6. Provision the infrastructure

```powershell
cd infrastructure
terraform init
terraform fmt -check -recursive
terraform validate
terraform plan
terraform apply
```

Review the plan carefully before typing `yes`. This creates: 2 DynamoDB tables, 4 IAM roles, 4 Lambda functions, a full API Gateway REST API with CORS, an S3 bucket + CloudFront distribution for the frontend, 2 SNS topics, 4 CloudWatch alarms, and 1 AWS Budget — around 60 resources in total.

**Note:** CloudFront distribution creation can take 3–8 minutes; this is normal.

## 7. Confirm your SNS email subscription

Check your inbox for an email from AWS titled "AWS Notification - Subscription Confirmation" and click **Confirm subscription**. Without this, you won't receive alerts or registration confirmations.

## 8. Seed sample events

```powershell
cd ..
python scripts/seed_events.py
```

## 9. Update the frontend's API URL

Open `frontend/js/api.js` and confirm `API_BASE_URL` matches your Terraform output:

```powershell
cd infrastructure
terraform output api_base_url
```

## 10. Deploy the frontend

```powershell
cd ..
.\scripts\deploy_frontend.ps1
```

This syncs `frontend/` to S3 and invalidates the CloudFront cache. Your live URL is printed at the end (also available via `terraform output frontend_url`).

## 11. Verify everything end-to-end

Visit your live frontend URL and test: browsing events, registering, viewing/cancelling registrations, and confirm you receive the SNS confirmation email.

## Tearing down

To avoid any ongoing cost, destroy all resources when you're done:

```powershell
cd infrastructure
terraform destroy
```

Review the destroy plan carefully before confirming — this is irreversible.