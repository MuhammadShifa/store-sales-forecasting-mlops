
# 🚀 Infrastructure with Terraform

In this module, we are exploring one of the most critical skills in MLOps:  
**Infrastructure as Code (IaC)** — using **Terraform**.

### What is Infrastructure as Code (IaC)?

**Infrastructure as Code (IaC)** refers to the practice of provisioning and managing infrastructure through code instead of manual configuration.

### What is Terraform?

**Terraform** is an open-source tool by HashiCorp that facilitates Infrastructure as Code using a declarative configuration language called **HCL (HashiCorp Configuration Language)**.

**Installation:** [Click for Terraform Installation](https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli) 

## Architecture Diagram — Real-time Store Sales Prediction Pipeline

```
                                            +----------------------------+
                                            |  S3 Bucket: Model Artifacts|
                                            +----------------------------+
                                                          | 
                                                          | Get Model
                                                          v
+--------------------+     +-----------------+     +--------------+                               +-------------------------+
| Kinesis Stream     | --> |  CW Event       |--->|   AWS Lambda  |--->publish prediction event-->|      Kinesis Stream     |
| Input(sales Events)|     | Lambda Trigger  |     +--------------+                               |Output(sales Predictions)| 
+--------------------+     +-----------------+            ^                                       +-------------------------+   
                                                          |         
                                                          | Get Image                                         
                                                    +-------------+           
                                                    |    ECR      |
                                                    +-------------+

        
```

> This architecture lives inside the AWS Cloud.  
> It supports **event-driven inference** for real-time store sales predictions using **Kinesis**, **Lambda**, **ECR**, and **S3**.


### Project Structure

```
module6/
└── infrastructure/
    ├── main.tf            # Backend + AWS provider
    ├── variables.tf       # Global variables
    └── modules/
        └── kinesis/
            ├── main.tf    # Kinesis stream definition
            └── variables.tf
```

---

## Step-by-Step Progress

### Step 1: Configure Remote State with S3

Terraform state is used to track resource changes. A remote S3 bucket is configured to store this state securely.

**`infrastructure/main.tf`**
```hcl
terraform {
  required_version = ">= 1.0"
  backend "s3" {
    bucket  = "tf-state-store-sales-prediction"
    key     = "store-sales-prediction-stg.tfstate"
    region  = "ap-south-1"
    encrypt = true
  }
}
```

> **Note:** The S3 bucket `tf-state-store-sales-prediction` was created manually via the AWS console.


### Step 2: Set Up the AWS Provider

**`infrastructure/main.tf`**
```hcl
provider "aws" {
  region = var.aws_region
}
```

**`infrastructure/variables.tf`**
```hcl
variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "ap-south-1"
}
```


### Step 3: Create a Terraform Module for Kinesis

##### Kinesis Stream Module: Detailed Explanation (`modules/kinesis/main.tf`)
This configuration defines an **AWS Kinesis Data Stream**, which is used for handling streaming data in the MLOps architecture.

```hcl
resource "aws_kinesis_stream" "stream" {
  name                 = var.stream_name
  shard_count          = var.shard_count
  retention_period     = var.retention_period
  shard_level_metrics  = var.shard_level_metrics

  tags = {
    CreatedBy = var.tags
  }
}

output "stream_arn" {
  value = aws_kinesis_stream.stream.arn
}
```
### Output Definition

```hcl
output "stream_arn" {
  value = aws_kinesis_stream.stream.arn
}
```

This block outputs the Amazon Resource Name (ARN) of the Kinesis stream, which can be used as a reference in other modules like Lambda configuration.

This design allows the stream to be created dynamically and reused across environments through input variables. It supports both ingestion (input stream) and result forwarding (output stream) in the real-time inference pipeline.

### Infrastructure Integration

In `infrastructure/main.tf`, the kinesis stream is configured like this:
```hcl
# sales_events
module "source_kinesis_stream" {
  source = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  stream_name = "${var.source_stream_name}-${var.project_id}"
  tags = var.project_id
}
```

**`infrastructure/variables.tf`**
```hcl
variable "source_stream_name" {
  description = ""
}
```
### Step 4: Add Kinesis Output Stream

In addition to the input stream, a second **Kinesis stream** was created for publishing sales prediction events.

**`infrastructure/main.tf`**
```hcl
# sales_predictions
module "output_kinesis_stream" {
  source = "./modules/kinesis"
  retention_period = 48
  shard_count = 2
  stream_name = "${var.output_stream_name}-${var.project_id}"
  tags = var.project_id
}
```

**`infrastructure//variables.tf`**
```hcl
variable "output_stream_name" {
  description = ""
}
```


### Running Terraform command

Before running the terraform command, make sure `tf-state-store-sales-prediction` S3 bucket is created manually and the following variable should be exported:
```bash
export AWS_ACCESS_KEY_ID='your aws acces key'
export AWS_SECRET_ACCESS_KEY='your aws secret key'
export AWS_DEFAULT_REGION='your aws default region'

```


Navigate to the `infrastructure` directory and run the following commands:

#### Initialize Terraform
```bash
terraform init
```

If multiple AWS profiles are used:
```bash
terraform init --profile <your-profile-name>
```

#### Preview the Execution Plan
```bash
terraform plan
```
This will required the input_stream_name and output_stream_name, 
```bash
var.output_stream_name
  Enter a value: sales-predictions
var.source_stream_name
  Enter a value: sales-events
```

#### Apply the Plan
```bash
terraform apply 
```

🖼️ <img src="../results_images/8aterranform_appy.png" alt=" terraform apply" width="600"/>


This will also required the input stream_name and output stream name.
Later on, we will pas these values from `vars` folder.

After approval, the Kinesis stream `sales-events-stg` and `sales-predictions-stg` will be created.

🖼️ <img src="../results_images/8b-terranform-stream-created.png" alt="terraform stream" width="600"/>

#### Destroy the resource
```bash
terraform destroy
```
This command will destroy/delete the created resource

---
