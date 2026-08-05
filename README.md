# TICKETME
Serverless Event Registration &amp; Ticketing System built on AWS (Lambda, API Gateway, DynamoDB, SNS etc) 

TicketMe is a serverless event registration and ticketing system developed as the final capstone project for the **Azubi Africa AWS Cloud & AI Intensive Program**.

### Overview

The application modernizes event registration by replacing manual Microsoft Forms and spreadsheet-based workflows with a scalable, cloud-native solution. It enables organizations to create events, manage registrations, prevent duplicate submissions, enforce event capacity limits, and monitor system performance without provisioning or managing servers.

---

### Problem Statement

Traditional event registration processes that rely on online forms and spreadsheets present several challenges:

* Duplicate registrations
* Manual tracking of event capacity
* Limited automation for confirmations and notifications
* Difficulty monitoring application health and usage
* Poor scalability as the number of events and participants increases

---

### Solution

TicketMe addresses these challenges through a fully serverless architecture built on AWS services.

| Component       | Technology          | Purpose                                                                |
| --------------- | ------------------- | ---------------------------------------------------------------------- |
| Frontend        | Web Application     | Provides an interface for browsing events and submitting registrations |
| Backend         | AWS Lambda (Python) | Processes API requests and implements business logic                   |
| API             | Amazon API Gateway  | Exposes RESTful endpoints for the application                          |
| Database        | Amazon DynamoDB     | Stores event and registration data                                     |
| Notifications   | Amazon SNS          | Sends registration confirmation notifications                          |
| Monitoring      | Amazon CloudWatch   | Collects logs, metrics, and application health information             |
| Cost Management | AWS Budgets         | Monitors AWS Free Tier usage and estimated costs                       |
| Infrastructure  | Terraform           | Provisions and manages AWS resources using Infrastructure as Code      |
| CI/CD           | GitHub Actions      | Automates testing and deployment workflows                             |

---

### Architecture

The application follows a serverless architecture in which client requests are routed through Amazon API Gateway to AWS Lambda functions. Business logic is executed within the Lambda functions, while event and registration data are stored in Amazon DynamoDB. Registration notifications are delivered using Amazon SNS, and operational monitoring is provided through Amazon CloudWatch. Infrastructure provisioning and configuration are managed using Terraform, with GitHub Actions supporting automated deployment.

The architecture diagram is available in the `docs/architecture/` directory.

### Technology Stack

The application is built using a fully serverless architecture on Amazon Web Services (AWS).

| Layer                                          | Technology                               |
| ---------------------------------------------- | ---------------------------------------- |
| Cloud Provider                                 | Amazon Web Services (AWS)                |
| Compute                                        | AWS Lambda (Python 3.12)                 |
| API                                            | Amazon API Gateway (REST API)            |
| Database                                       | Amazon DynamoDB                          |
| Notifications                                  | Amazon Simple Notification Service (SNS) |
| Monitoring                                     | Amazon CloudWatch                        |
| Infrastructure as Code                         | Terraform                                |
| Continuous Integration / Continuous Deployment | GitHub Actions                           |
| Frontend                                       | HTML, CSS, and JavaScript                |

---

### Project Status

The project is currently under active development as part of the Azubi Africa AWS Cloud & AI Intensive Program. New features, infrastructure improvements, and documentation are being added incrementally as development progresses.

---

### Repository Structure

The repository is organized to separate application source code, infrastructure, documentation, and deployment workflows, making the project easier to maintain and extend.

ticketme/
├── backend/lambda/ # Lambda function source code
├── infrastructure/ # Terraform IaC
├── frontend/ # Web application
├── tests/ # Automated tests
├── docs/ # Architecture, API, deployment docs
├── presentation/ # Capstone presentation materials
└── .github/workflows/ # CI/CD pipelines

### Author

This project was developed by **Dunstan Banyaa** as the capstone project for the **Azubi Africa AWS Cloud & AI Intensive Program**. It demonstrates the design, implementation, and deployment of a fully serverless event registration system using Amazon Web Services (AWS), Infrastructure as Code (Terraform), and modern DevOps practices.

