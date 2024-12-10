# Minimal Provider Setup

This repository is a minimal provider setup for [Market Router](https://api.marketrouter.ai). It contains the necessary code to deploy an API that will serve as a provider in Market Router.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Market API Key Setup](#market-api-key-setup)
- [Configuration Variables](#setting-up-configuration-variables)
- [Running the API Locally](#running-the-api-locally)
- [Cloud Deployment (AWS)](#cloud-deployment-aws)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Bid Strategy**: Scans for open instances and creates a proposal with the minimum bid allowed ($0.01).
- **API Authentication**: Uses a static API key for authentication. Future enhancements could include proposal-based API keys for more granular control.
- **Completions Endpoint**: OpenAI-compatible wrapper with the model provided in the configuration file.

## Installation

### Prerequisites
- Python 3.11
- Docker
- AWS CLI
- Terraform

### Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/GroupLang/minimal-provider-llm-router.git
   cd minimal-provider-llm-router
   ```

2. **Install required libraries**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Set up environment space**

   - **Set up environment variables**

     Copy the sample environment file and configure it as per your requirements.

     ```bash
     [ ! -f .env ] && cp .env.template .env
     ```

   - **Install pre-commit**

     Install the pre-commit hooks to ensure that your commits meet the project's standard for code quality and formatting.

     ```bash
     pre-commit install
     ```

## Market API Key Setup

### Registration

```bash
curl -X 'POST' \
  'https://api.marketrouter.ai/v1/auth/register' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "email": "user@example.com",
  "username": "string",
  "fullname": "string",
  "password": "string"
}'
```

### Login

After receiving a **HTTP 201** status code, you can proceed to login:

```bash
curl -X 'POST' \
  'https://api.marketrouter.ai/v1/auth/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=<USERNAME_HERE>&password=<PASSWORD_HERE>'
```

### API Key Creation

With the token received in the response `{"access_token":<TOKEN_HERE>, "token_type":"bearer"}`, you can create an API KEY to access the Market:

```bash
curl -X 'POST' \
  'https://api.marketrouter.ai/v1/auth/create-api-key?name=<API_KEY_NAME>&is_live=true' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer <TOKEN_HERE>'
```

A successful response (with **HTTP 201** status code) looks like this:

```json
{
    "api_key":<YOUR_API_KEY>,
    "name":<API_KEY_NAME>,
    "is_live":true
}
```

### Account Top Up

To ensure your balance is positive, call this endpoint:

```bash
curl -X 'POST' \
  'https://api.marketrouter.ai/v1/payment/deposit' \
  -H 'accept: application/json' \
  -H 'X-API-KEY: <YOUR_API_KEY>' \
  -H 'Content-Type: application/json' \
  -d '{
  "amount": 10,
  "description": "Deposit/Withdraw to account"
}'
```

## Setting Up Configuration Variables

Fill the `.env` with the following variables:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `NOTDIAMOND_API_KEY`
- `APP_COMPLETIONS_ENDPOINT`: The endpoint that requesters will use.

## Running the API Locally

Build the Docker image and run the API:

```bash
docker build -t test . --no-cache
docker run -p 80:80 --env-file .env test
```

## Cloud Deployment (AWS)

The `infrastructure/` directory contains all the necessary Terraform files to deploy the API in AWS.

1. **AWS Credentials**: Store them in `$HOME/.aws`.
2. **Create Secrets**: If it's the first time deploying, create the secrets in AWS Secret Manager:

   ```bash
   bash create_secrets.sh
   ```

3. **Deploy the API**:

   ```bash
   bash deploy.sh
   ```

### Setting the App Completions Endpoint with a Custom Domain

To get a static endpoint, obtain the DNS name from the Application Load Balancer. Add the DNS name record to your domain registrar. Update the secret `APP_COMPLETIONS_ENDPOINT` in AWS Secrets Manager and redeploy the API.

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) for more information.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
