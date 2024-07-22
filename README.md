# Inventory Management Backend

## I. Create AWS IAM User

1. Navigate to [IAM Management Console](https://console.aws.amazon.com/iam).
2. Click the **Create user** button.
3. Enter the **user name**.
4. Check the checkbox: **Provide user access to the AWS Management Console - optional**.
5. Select the radio button: **I want to create an IAM user**.
6. Select the radio button: **Custom password**.
8. Uncheck the checkbox: **Users must create a new password at next sign-in - Recommended**.

### Set Permissions

1. Choose **Add user to group (default)**.
2. Check the created group.
3. Submit.

## I.1. Create Access Key

1. Go to the user dashboard.
2. Click **Create access key** link in the summary section.
3. Select the radio button: **Command Line Interface (CLI)**.
4. Check the checkbox: **I understand the above recommendation and want to proceed to create an access key**.
5. Submit.
6. Save the **Access key** and **Secret access key**.

## II. Build and Push the Docker Image to Amazon ECR

### II.1. AWS CLI Instruction

1. Install AWS CLI: [AWS CLI V2 MSI Installer](https://awscli.amazonaws.com/AWSCLIV2.msi).
2. Verify the installation:

    ```bash
    aws --version
    ```

   Restart if it doesn't work.

### II.2. Configure AWS CLI

1. Run command line:

    ```bash
    aws configure
    ```

2. Enter the following details:
    - **AWS Access Key ID**: Your AWS access key ID.
    - **AWS Secret Access Key**: Your AWS secret access key.
    - **Default region name**: `us-east-1` (or your preferred region).
    - **Default output format**: `json` (or your preferred format).

### II.3. Authenticate Docker to ECR and Push the Image

1. Run the following command line:

    ```bash
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS Account ID>.dkr.ecr.us-east-1.amazonaws.com
    ```

   Replace `us-east-1` with your preferred region.

   Replace `<AWS Account ID>` with your AWS account ID.

### II.4. Create a Repository in ECR (if not already created)

1. Run the following command line:

    ```bash
    aws ecr create-repository --repository-name inventory-management-backend
    ```

   Replace `inventory-management-backend` with your preferred repository name.

### II.5. Build the Docker Image

1. Run the following command line:

    ```bash
    docker build -t inventory-management-backend -f Dockerfile.lambda .
    ```

   `Dockerfile.lambda` is the Dockerfile for lambda in your project.

   Don't remove the last dot (`.`).

### II.6. Tag the Docker Image

1. Run the following command line:

    ```bash
    docker tag inventory-management-backend:latest <AWS Account ID>.dkr.ecr.us-east-1.amazonaws.com/inventory-management-backend:latest
    ```

   Replace `<AWS Account ID>` with your AWS account ID.

### II.7. Push the Docker Image to ECR

1. Run the following command line:

    ```bash
    docker push <AWS Account ID>.dkr.ecr.us-east-1.amazonaws.com/inventory-management-backend:latest
    ```

   Replace `<AWS Account ID>` with your AWS account ID.

### II.8. Deploy Your Serverless Application

1. Run the following command line:

    ```bash
    serverless deploy
    ```
