# AWS-Fraud-Pipeline
# Serverless Real-Time Fraud Detection Pipeline

An event-driven data engineering architecture built on AWS to ingest, evaluate, and alert on anomalous financial transactions in real-time. 

This project demonstrates the transition from batch processing to real-time streaming analytics. It utilizes decoupled cloud microservices to handle high-velocity data ingestion and rules-based evaluation without the overhead of provisioning persistent servers.

## Architecture Overview

The pipeline leverages four core AWS services operating in the `ap-south-1` (Mumbai) region:

* **Amazon Kinesis:** Acts as the high-throughput ingestion buffer (`TransactionStream`), receiving raw JSON transaction payloads simulating a live point-of-sale system.
* **AWS Lambda:** The serverless compute engine. A Python-based function (`lambda_fun`) is triggered instantly by new records in the Kinesis stream to execute the fraud evaluation logic.
* **Amazon DynamoDB:** A NoSQL database (`UserProfiles`) storing historical user baselines, including home locations and daily spending limits.
* **Amazon SNS:** A pub/sub messaging service (`FraudAlerts`) that instantly routes formatted security alerts to subscribed administrators when the rules engine flags a violation.

## Repository Structure

* `create_table.py` - Provisions the DynamoDB state table using On-Demand capacity.
* `add_user.py` - Establishes the baseline user profiles and spending limits in the database.
* `setup_sns.py` - Creates the SNS topic and registers the administrator email subscription.
* `lambda_function.py` - The core rules engine deployed to AWS. Decodes the base64 Kinesis payload, queries DynamoDB, evaluates the logic, and triggers SNS.
* `fraud.py` - The client-side simulator that injects anomalous transaction data into the Kinesis stream.
* `del.py` - Teardown script to safely destroy the Kinesis stream and prevent continuous hourly billing.

## Execution Flow

When `fraud.py` executes, a JSON payload containing the `UserID`, `Amount`, and `Location` enters the Kinesis stream. 

Lambda intercepts this event in milliseconds and validates the transaction against the user's DynamoDB profile. A transaction is flagged as fraudulent if:
1. The transaction amount exceeds the user's configured `DailyLimit`.
2. The transaction location does not match the user's established `HomeLocation`.

If a violation is detected, Lambda publishes a detailed payload to SNS, which pushes an immediate email alert to the security team detailing the user, the anomalous amount, and the specific reasons for the flag.

## Future Enhancements for Business Intelligence

As a foundation for downstream data analytics, this architecture can be expanded by routing a secondary Kinesis data stream via Amazon Kinesis Data Firehose into an S3 data lake. This allows the real-time classification data (Approved vs. Flagged transactions) to be connected directly to a Power BI dashboard, providing stakeholders with live visualizations of fraud trends and system efficacy.
