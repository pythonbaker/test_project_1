Learnings:
AWS account- personal

Created the repo using
git init and poetry new test_project_1

AWS credentials:
added in .env folder (add this file in gitignore to avoid committing to git)

Project 1 : use terraform to deploy aws resources lambda and s3
deploy.sh script to deploy the terraform code.
Lambda - can be deployed either as image or zip file. Try working on zip file first.

To create lambda zip file:
wrote zip_lambda.sh script to copy all files in src (with dependency file i.e requirements.txt) to lambda_function.zip in root folder. This zip file is then used in terraform code for lambda
```
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_file = "${path.module}/lambda_function.zip"
  output_path = "${path.module}/lambda_function.zip"
}
```

In Terraform, path.module is a built‑in variable that points to the filesystem path of the module where the Terraform code is running.
```
- First run zip_lambda code which zips the lambda code from lambda_build folder with requirements file and creates zip folder in terraform folder.
Run bash script to zip lambda file: bash zip_lambda.sh

- Then terraform to use the above zip folder
Run terraform locally via cli:  terraform/deploy.sh
```

Tech stack:
AWS -lambda and s3 bucket
Terraform for deployment

Get the data from a public website : trigger lambda and load into s3 bucket, load into bigquery using airflow?
airflow locally via docker- to move data from s3 to bigquery

SET UP AIRFLOW:
https://airflow.apache.org/docs/apache-airflow/2.3.0/start/docker.html#docker-compose-yaml- follow these instructions
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.0/docker-compose.yaml'
mkdir -p ./dags ./logs ./plugins\necho -e "AIRFLOW_UID=$(id -u)" > .env
docker-compose up airflow-init
docker compose ps
docker-compose up

GITHUB
- Upload the repo to github(pythonbaker)
- create a repo in github
- git remote add origin https://github.com/pythonbaker/test_project_1.git (run this command)
- git remote -v (check if remote repo is connected)
- git add .
- git commit -m "Initial commit: Add project files with Terraform, Airflow, and Lambda configurations"
- git push -u origin main