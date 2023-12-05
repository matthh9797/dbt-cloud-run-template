# DBT Cloud Run Template

## Key Contacts

- Matthew Henderson [matthewh@netextremity.com](matthewh@netextremity.com) - Owner

## Pre-requisites

There are several ways to recreate this article but to follow along line for line you will need:

 - The [gcloud CLI](https://cloud.google.com/sdk/docs/install) installed and configured.
 - [Anaconda](https://www.anaconda.com/products/distribution) installed and configured.
 - You have a billable GCP project setup.
 - [Docker](https://www.docker.com/)
 - [VS Code](https://code.visualstudio.com/)
 - [VS Code Extension - Cloud Code](https://cloud.google.com/code) (For local development)

## Getting Started

Let's create a new conda environment with dbt-bigquery and Flask.

```bash
conda create -n dbt-cloud-run pip
conda activate dbt-cloud-run
pip install dbt-bigquery
pip install google-cloud-logging
pip install Flask
```

## Update your DBT Profile

Update `dbt/profiles.yml` with YOUR_DATASET and YOUR_PROJECT.

```yml
YOUR_DBT_PROJECT:
  target: dev
  outputs:
    dev:
      dataset: YOUR_DATASET
      job_execution_timeout_seconds: 300
      job_retries: 1
      location: EU
      method: oauth
      priority: interactive
      project: YOUR_PROJECT
      threads: 4
      type: bigquery
    prod:
      dataset: YOUR_DATASET
      job_execution_timeout_seconds: 300
      job_retries: 1
      location: EU
      method: oauth
      priority: interactive
      project: YOUR_PROJECT
      threads: 4
      type: bigquery
```

## Deploy App to Cloud Run

```cmd
SERVICE_ACCOUNT=YOUR_SERVICE_ACCOUNT
SERVICE_NAME=YOUR_SERVICE_NAME # e.g. dbt-daily
REGION=YOUR_REGION # e.g. europe-west2

gcloud builds submit \
  --tag gcr.io/$(gcloud config get-value project)/${SERVICE_NAME}

gcloud run deploy ${SERVICE_NAME} --region $REGION \
    --image gcr.io/$(gcloud config get-value project)/${SERVICE_NAME} \
    --service-account ${SERVICE_ACCOUNT}@$(gcloud config get-value project).iam.gserviceaccount.com \
    --platform managed \
    --no-allow-unauthenticated
```
