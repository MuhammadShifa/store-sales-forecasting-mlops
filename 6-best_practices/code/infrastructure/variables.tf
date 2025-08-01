variable "aws_region" {
  description = "AWS region to create resources"
  default     = "ap-south-1"
}

variable "project_id" {
  description = "project_id"
  default = "store-sales-predictions"
}

variable "source_stream_name" {
  description = ""
}


variable "output_stream_name" {
  description = ""
}