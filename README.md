# Automated File Processing Automation

## Overview

This project implements an enterprise-grade serverless file processing platform using AWS services and GitHub Actions CI/CD.

The solution automatically processes files uploaded to Amazon S3, validates data, performs business transformations, maintains audit records, handles failures, and provides monitoring and alerting.

### Key Technologies

* AWS Lambda
* Amazon S3
* Amazon EventBridge
* Amazon DynamoDB
* Amazon SQS (Dead Letter Queue)
* Amazon SNS
* Amazon CloudWatch
* Python 3.12
* GitHub Actions

---

# Architecture

```text
User Uploads File
        |
        v
   S3 Bucket
        |
        v
  EventBridge Rule
        |
        v
 AWS Lambda Function
        |
        +-------------------+
        |                   |
        v                   v
 Validation         Data Processing
        |                   |
        +---------+---------+
                  |
                  v
          DynamoDB Audit
                  |
                  v
           Processed Files

Failures
    |
    +--> Failed Folder
    +--> SNS Notification
    +--> SQS DLQ

Monitoring
    |
    +--> CloudWatch Logs
    +--> CloudWatch Alarms
```

---

# Business Use Case

Organizations often receive files from:

* Customers
* Vendors
* Banking systems
* ERP systems
* Third-party integrations

Instead of manually validating and processing these files, this platform automates the entire workflow.

Benefits:

* Reduced manual effort
* Faster processing
* Improved data quality
* Full auditability
* Enterprise-grade monitoring
* Scalable serverless architecture

---

# Repository Structure

```text
file-processing/
│
├── requirements.txt
│
├── src/
│   ├── lambda_function.py
│   ├── processor.py
│   ├── validator.py
│   └── notifier.py
│
├── tests/
│   └── test_processor.py
│
└── .github/
    └── workflows/
        └── deploy.yml
```

---

# Components

## lambda_function.py

Main Lambda entry point.

Responsibilities:

* Receive EventBridge event
* Read file from S3
* Invoke validation
* Invoke processing
* Update audit records
* Handle exceptions
* Trigger notifications

---

## validator.py

Validates incoming files.

Checks:

* File exists
* CSV format
* Required columns
* Empty records
* Invalid values

Example:

```python
required_columns = [
    "customer_id",
    "name",
    "amount"
]
```

---

## processor.py

Business processing logic.

Responsibilities:

* Read records
* Transform data
* Apply calculations
* Generate output

Example:

```python
tax = amount * 0.10
```

---

## notifier.py

Handles notifications.

Responsibilities:

* Publish SNS alerts
* Send failure notifications
* Send operational alerts

---

## test_processor.py

Unit tests.

Validates:

* Business calculations
* Data transformations
* Validation logic

---

# AWS Resources

## S3 Bucket

Stores files.

Bucket:

```text
company-file-processing-prod
```

Folders:

```text
incoming/
processed/
failed/
archive/
```

### incoming/

New files arrive here.

Example:

```text
incoming/customer_data.csv
```

### processed/

Successfully processed files.

### failed/

Invalid or failed files.

### archive/

Long-term retention.

---

## DynamoDB

Table:

```text
FileProcessingAudit
```

Partition Key:

```text
fileId
```

Stores:

* File Name
* Processing Status
* Record Count
* Processing Time
* Error Details

Example:

```json
{
  "fileId":"123",
  "fileName":"customer_data.csv",
  "status":"SUCCESS",
  "recordCount":500
}
```

---

## EventBridge

Rule:

```text
FileUploadedRule
```

Pattern:

```json
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"]
}
```

Automatically triggers Lambda when a file is uploaded.

---

## Lambda

Function:

```text
company-file-processing-prod
```

Runtime:

```text
Python 3.12
```

Responsibilities:

* Validation
* Processing
* Auditing
* Error handling

---

## SQS Dead Letter Queue

Queue:

```text
FileProcessingDLQ
```

Purpose:

* Capture failed events
* Prevent data loss
* Support troubleshooting

---

## SNS Topic

Topic:

```text
FileProcessingAlerts
```

Purpose:

* Failure notifications
* Operational alerts

Recipients:

* Operations Team
* Support Team
* Application Owners

---

## CloudWatch

Used for:

* Logs
* Metrics
* Alarms
* Monitoring

Example Alarms:

```text
Lambda Errors > 5
Duration > 60 Seconds
Throttles > 0
```

---

# CI/CD Pipeline

GitHub Actions automatically deploys code.

Workflow:

```text
Developer Push
       |
       v
GitHub Actions
       |
       +--> Install Dependencies
       |
       +--> Run Tests
       |
       +--> Package Lambda
       |
       +--> Deploy Lambda
```

File:

```text
.github/workflows/deploy.yml
```

---

# GitHub Secrets

Required Secrets:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

Location:

```text
Repository
    → Settings
        → Secrets and Variables
            → Actions
```

---

# Deployment

Clone repository:

```bash
git clone <repository-url>
cd file-processing
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run tests:

```bash
python -m unittest discover tests
```

Push code:

```bash
git add .
git commit -m "Deploy changes"
git push origin main
```

GitHub Actions automatically deploys the Lambda.

---

# Failure Handling

If processing fails:

1. Error logged to CloudWatch
2. Audit record written to DynamoDB
3. SNS notification sent
4. Event stored in DLQ
5. File moved to failed folder

Benefits:

* No data loss
* Faster troubleshooting
* Full traceability
* 
---

# Future Enhancements

* Multi-environment deployment (DEV/QA/UAT/PROD)
* Infrastructure as Code (Terraform/SAM)
* Data quality framework
* Slack notifications
* Batch processing
* Step Functions orchestration
* Data Lake integration
* API-based ingestion

---

# End-to-End Flow

```text
File Upload
    |
    v
S3 incoming/
    |
    v
EventBridge
    |
    v
Lambda
    |
    +--> Validation
    |
    +--> Processing
    |
    +--> DynamoDB Audit
    |
    +--> CloudWatch Logging
    |
    +--> SNS Notifications
    |
    v
processed/

Failure Path

Lambda Failure
    |
    +--> failed/
    +--> SNS Alert
    +--> DLQ
    +--> CloudWatch Error
```

This project demonstrates an enterprise-grade event-driven file processing architecture commonly used in banking, insurance, healthcare, retail, and large-scale data integration systems.
