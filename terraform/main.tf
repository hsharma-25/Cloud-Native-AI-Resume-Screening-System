provider "aws" {
  region = "us-east-1"
}

resource "aws_security_group" "resumeiq_sg" {
  name        = "resumeiq-security-group"
  description = "Security group for ResumeIQ DevOps project"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30007
    to_port     = 30007
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 30244
    to_port     = 30244
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "resumeiq_server" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "m7i-flex.large"

  vpc_security_group_ids = [aws_security_group.resumeiq_sg.id]

  tags = {
    Name = "ResumeIQ-DevOps-Server"
  }
}