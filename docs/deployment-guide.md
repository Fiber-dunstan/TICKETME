# 🎟 TicketMe

**A serverless Event Registration & Ticketing System, built entirely on AWS.**

Final capstone project for the Azubi Africa AWS Cloud & AI Intensive Program.

**🔗 Live Demo:** [https://d24m8nf71z49d9.cloudfront.net](https://d24m8nf71z49d9.cloudfront.net)

---

## Table of Contents

- [Overview](#overview)
- [The Problem](#the-problem)
- [The Solution](#the-solution)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Screenshots](#screenshots)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Testing](#testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Security](#monitoring--security)
- [Cost Optimization](#cost-optimization)
- [Lessons Learned](#lessons-learned)
- [Future Improvements](#future-improvements)
- [Documentation](#documentation)
- [Author](#author)

---

## Overview

TicketMe replaces manual, spreadsheet-based event registration workflows with a fully serverless, cloud-native REST API and web application. It handles event discovery, registration, duplicate/capacity prevention, cancellation, email confirmations, and real-time monitoring — all without managing a single server.

## The Problem

Organizations commonly manage event signups through Microsoft Forms feeding into Excel spreadsheets. This approach:
- Doesn't scale past a handful of events or attendees
- Has no real-time capacity enforcement — overbooking is common
- Allows duplicate registrations with no automated prevention
- Provides no automated confirmations or notifications
- Offers zero operational visibility (no logs, no alerts, no monitoring)

## The Solution

A serverless system where:
- Events and registrations live in **DynamoDB**, not spreadsheets
- Business logic runs in **AWS Lambda**, scaling automatically with demand and costing nothing when idle
- **API Gateway** exposes a clean REST API consumed by a modern frontend
- **SNS** sends automated registration confirmations
- **CloudWatch** monitors error rates in real time and alerts via SNS if they exceed 5%
- **AWS Budgets** guards against unexpected cost
- The entire system is defined as code (**Terraform**) and deployed via a tested, automated **CI/CD pipeline** (GitHub Actions)

## Architecture

┌─────────────────────┐
                │   Browser (SPA)      │
                │  Vanilla JS frontend  │
                └──────────┬───────────┘
                           │ HTTPS
                ┌──────────▼───────────┐
                │  CloudFront + S3      │
                │  (static hosting)      │
                └──────────┬───────────┘
                           │
                ┌──────────▼───────────┐
                │   API Gateway (REST)  │
                └──────────┬───────────┘
                           │
    ┌──────────────────────┼──────────────────────┐
    ▼                      ▼                        ▼
    ┌───────────────┐ ┌──────────────────┐ ┌─────────────────────┐
│ list_events │ │ register │ │ get_registrations │
│ Lambda │ │ Lambda │ │ Lambda │
└───────┬────────┘ └────────┬─────────┘ └──────────┬──────────┘
│ │ │
│ ┌────────▼─────────┐ │
│ │ cancel_registration│ │
│ │ Lambda │ │
│ └────────┬─────────┘ │
│ │ │
└──────────────────────┼──────────────────────────┘
▼
┌──────────────────────┐
│ DynamoDB │
│ events / registrations │
└──────────┬───────────┘
│
┌──────────▼───────────┐
│ CloudWatch Logs │
│ + Error-Rate Alarms │
└──────────┬───────────┘
│
┌──────────▼───────────┐
│ SNS │
│ Ops Alerts / Confirms │
└───────────────────────┘

See [`docs/architecture/`](docs/architecture/) for the full architecture writeup and data model.

## Tech Stack

| Layer | Technology |
|---|---|
| Cloud Provider | AWS |
| Compute | AWS Lambda (Python 3.12) |
| API | Amazon API Gateway (REST) |
| Database | Amazon DynamoDB |
| Notifications | Amazon SNS |
| Monitoring | Amazon CloudWatch (Logs, Metric Alarms) |
| Cost Control | AWS Budgets |
| Infrastructure as Code | Terraform |
| CI/CD | GitHub Actions |
| Frontend | Vanilla JavaScript (ES Modules), CSS3, HTML5 |
| Hosting | Amazon S3 + CloudFront (CDN, HTTPS) |
| Testing | pytest, moto (AWS mocking) |

## Features

- Browse, search, and filter live events
- Register for events with real-time validation
- Duplicate registration prevention (per email + event)
- Capacity enforcement using atomic, race-condition-safe DynamoDB updates
- View and cancel registrations by email
- Automated email confirmation on registration (via SNS)
- Skeleton loading states, toast notifications, empty/error states
- Dark/light theme toggle
- Fully responsive, mobile-friendly design
- Least-privilege IAM — a dedicated role per Lambda function
- CloudWatch error-rate alarms (metric math: errors ÷ invocations)
- AWS Budgets cost-tracking safety net
- Fully automated CI: unit tests + Terraform validation on every push/PR

## Screenshots

### Application

| Events | Registration | My Registrations |
|---|---|---|
| ![Events](docs/screenshots/events-page.png) | ![Registration](docs/screenshots/registration-modal.png) | ![My Registrations](docs/screenshots/my-registrations.png) |

### Infrastructure (Terraform-provisioned)

| DynamoDB | Lambda | API Gateway |
|---|---|---|
| ![DynamoDB](docs/screenshots/dynamodb-tables.png) | ![Lambda](docs/screenshots/lambda-functions.png) | ![API Gateway](docs/screenshots/api-gateway.png) |

### Monitoring & CI/CD

| CloudWatch Alarms | SNS Topics | AWS Budget |
|---|---|---|
| ![Alarms](docs/screenshots/cloudwatch-alarms.png) | ![SNS](docs/screenshots/sns-topics.png) | ![Budget](docs/screenshots/aws-budget.png) |

| GitHub Actions CI | Test Results |
|---|---|
| ![CI](docs/screenshots/github-actions-passing.png) | ![Tests](docs/screenshots/pytest-results.png) |

## Project Structure

ticketme/
├── backend/
│ └── lambda/
│ ├── list_events_handler/
│ ├── register_handler/
│ ├── get_registrations_handler/
│ ├── cancel_registration_handler/
│ └── shared/ # response_utils, logger, validators
├── frontend/
│ ├── index.html
│ ├── css/ # design system, components, animations
│ └── js/
│ ├── api.js # centralized API client
│ ├── router.js # hash-based SPA router
│ ├── state.js
│ ├── views/ # events, registrations
│ └── components/ # eventCard, modal, toast
├── infrastructure/ # Terraform: DynamoDB, IAM, Lambda,
│ # API Gateway, S3, CloudFront, SNS,
│ # CloudWatch alarms, AWS Budgets
├── tests/ # pytest + moto unit tests
├── scripts/ # build & deploy automation
├── docs/
│ ├── architecture/
│ ├── api/
│ ├── screenshots/
│ └── deployment-guide.md
├── presentation/
└── .github/workflows/ # CI: backend tests, Terraform validate

## Getting Started

Full step-by-step setup instructions are in [`docs/deployment-guide.md`](docs/deployment-guide.md). Summary:

```powershell
# Clone
git clone https://github.com/Fiber-dunstan/TICKETME.git
cd TICKETME

# Backend: set up Python environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt

# Run tests
pytest tests/ -v

# Deploy infrastructure
cd infrastructure
terraform init
terraform apply

# Seed sample data
cd ..
python scripts/seed_events.py

# Deploy frontend
.\scripts\deploy_frontend.ps1
```

## Testing

14 unit tests cover all 4 Lambda functions — happy paths and every failure branch (validation errors, missing resources, duplicates, capacity limits) — using `moto` to simulate AWS services in-memory, with zero cost and no real AWS calls.

```powershell
pytest tests/ -v
```

## CI/CD Pipeline

Two GitHub Actions workflows run automatically:

- **`backend-tests.yml`** — runs the full pytest suite on every push/PR to `main`/`develop`
- **`terraform-validate.yml`** — checks Terraform formatting and validity on every change to `infrastructure/`

Branch protection on `main` requires both checks to pass before a merge is allowed — a genuine automated quality gate, not just advisory.

**Branching strategy:** `main` (stable) ← `develop` (integration) ← `feature/*` branches, via Pull Requests.

## Monitoring & Security

- **Least-privilege IAM**: each Lambda has its own role with only the exact permissions it needs
- **Input validation & sanitization** on every write endpoint
- **CloudWatch Logs** for every function, with 14-day retention (cost control)
- **CloudWatch Alarms**: error rate (errors ÷ invocations) monitored per function, alerting via SNS if it exceeds 5%
- **SNS**: operational alerts (ops team) + registration confirmations (end users)
- **AWS Budgets**: monthly spend alerts at 80% actual / 100% forecasted

## Cost Optimization

- DynamoDB `PAY_PER_REQUEST` billing — no idle cost
- Lambda — pay only per invocation, generous AWS Free Tier
- CloudWatch Log Groups with explicit 14-day retention (prevents unbounded log storage cost)
- CloudFront `PriceClass_100` — cheapest tier, sufficient edge coverage
- AWS Budgets as an explicit safety net

## Lessons Learned

A few real debugging challenges worth highlighting (detailed in [`docs/troubleshooting.md`](docs/troubleshooting.md)):
- Python module-name collisions across Lambda handlers during testing
- DynamoDB reserved keywords (`capacity`, `status`) requiring `ExpressionAttributeNames`
- API Gateway CORS preflight requiring explicit `passthrough_behavior`
- API Gateway not reliably URL-decoding path parameters — solved with explicit `unquote()`
- Git branching discipline — the practical cost of merging into the wrong base branch, and how consistent `git status` checks and `gh pr create --base develop` solved it for good

## Future Improvements

- Single-table DynamoDB design for reduced read/write costs at scale
- Cognito-based authentication for an admin dashboard
- QR code ticket generation and PDF ticket download
- Event-attendance forecasting using historical registration data (ML-ready architecture)
- Custom domain + ACM certificate for the CloudFront distribution
- Terraform remote state (S3 backend + DynamoDB locking) for team collaboration

## Documentation

- [Architecture & Data Model](docs/architecture/data-model.md)
- [API Reference](docs/api/api-reference.md)
- [Deployment Guide](docs/deployment-guide.md)
- [Troubleshooting Guide](docs/troubleshooting.md)
- [Presentation](presentation/)

## Author

**Dunstan Banyaa**
Built as a capstone project for the Azubi Africa AWS Cloud & AI Intensive Program.
