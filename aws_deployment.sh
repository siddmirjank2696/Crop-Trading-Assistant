#!/bin/bash
# A script to automate aws deployment

# Pulling the latest models from GitHub
git pull

# Configure AWS
# aws configure

# Creating an ECR repository
aws ecr describe-repositories --repository-names crop_assistant_repo --query 'repositories[0].repositoryUri' --output text 2>/dev/null || aws ecr create-repository --repository-name crop_assistant_repo --query 'repository.repositoryUri' --output text

# Logging into ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 043309365742.dkr.ecr.us-east-1.amazonaws.com

# Building the docker image
docker build -t crop_assistant_repo .

# Tagging the docker image
docker tag crop_assistant_repo:latest 043309365742.dkr.ecr.us-east-1.amazonaws.com/crop_assistant_repo:deployment

# Cleaning up old images
aws ecr batch-delete-image --repository-name crop_assistant_repo --image-ids imageTag=old-tag > /dev/null

# Pushing the docker image to ECR
docker push 043309365742.dkr.ecr.us-east-1.amazonaws.com/crop_assistant_repo:deployment

# # Creating IAM role for AWS AppRunner if it doesn't exist
# aws iam get-role --role-name AppRunnerECRAccessRole >/dev/null 2>&1 \
# || aws iam create-role --role-name AppRunnerECRAccessRole \
#   --assume-role-policy-document '{
#     "Version": "2012-10-17",
#     "Statement": [
#       {
#         "Effect": "Allow",
#         "Principal": { "Service": "build.apprunner.amazonaws.com" },
#         "Action": "sts:AssumeRole"
#       }
#     ]
#   }'

# # Attaching Read-only role in policy
# aws iam attach-role-policy --role-name AppRunnerECRAccessRole --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly || true

# # Creating an app runner service to host the product
# aws apprunner create-service \
#   --service-name crop-assistant-service \
#   --source-configuration '{
#     "ImageRepository": {
#       "ImageIdentifier": "043309365742.dkr.ecr.us-east-1.amazonaws.com/crop_assistant_repo:deployment",
#       "ImageRepositoryType": "ECR",
#       "ImageConfiguration": { "Port": "8080" }
#     },
#     "AuthenticationConfiguration": {
#       "AccessRoleArn": "arn:aws:iam::043309365742:role/AppRunnerECRAccessRole"
#     }
#   }'

