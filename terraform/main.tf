# RANDOM TEXT
resource "random_string" "texto" {
  length = 5 
  special = false
  upper = false
}

#BUCKET
resource "aws_s3_bucket" "deadbycloud" {
  bucket = "${var.bucket_name}-${random_string.texto.result}"
  force_destroy = true
}