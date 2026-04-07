terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-central-1" 
}

# 1. Create the Data Lake S3 Bucket
resource "aws_s3_bucket" "energy_data_lake" {
  bucket = "smart-meter-raw-data-luka-frankfurt" 
}

# 2. Define the IAM Policy for Snowflake to read the bucket
resource "aws_iam_policy" "snowflake_s3_read_policy" {
  name        = "lstoric_snowflake_s3_read"
  description = "Allows Snowflake Storage Integration to read raw_data"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:GetObjectVersion"
        ]
        Resource = "${aws_s3_bucket.energy_data_lake.arn}/raw_data/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.energy_data_lake.arn
        Condition = {
          StringLike = {
            "s3:prefix" : ["raw_data/*"]
          }
        }
      }
    ]
  })
}

# 3. Create the IAM Role for Snowflake
resource "aws_iam_role" "snowflake_integration_role" {
  name = "lstoric_snowflake_role"

  # The Trust Relationship is initially empty until Snowflake generates the External ID
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          AWS = "*" # To be restricted after Snowflake integration is created
        }
      }
    ]
  })
}

# Attach the policy to the role
resource "aws_iam_role_policy_attachment" "snowflake_role_attach" {
  role       = aws_iam_role.snowflake_integration_role.name
  policy_arn = aws_iam_policy.snowflake_s3_read_policy.arn
}
