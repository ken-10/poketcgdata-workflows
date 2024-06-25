# PokeTCGData Workflows
Automated system to ingest daily Pokemon TCG pricing data from **[Pokemon TCG IO API](https://docs.pokemontcg.io/)**.
<br/>The data is displayed in a live dashboard that can be found here. (Coming soon)

> [!NOTE]
> The way this project is deployed/architected may not make sense due to budgeting and to better learn the applications being used.

# Architecture
![Architecture Diagram](/assets/images/poketcgworkflows_highlevel_diagram_3.jpg)

### Tools
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white) ![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white) ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)  ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

### Database/Cloud Hosting
![Azure SQL](https://img.shields.io/badge/azure%20sql-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white) ![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)


## Setup

This does require a Azure SQL Database or Microsoft SQL Server instance to store data. There is usually a free tier for Azure SQL Database.<br/><br/>
<ins>**If you want to run this 100% locally**</ins>, skip the steps related to terraform and AWS CLI. Also, set up a **[Microsoft SQL Server 2022 Linux container with Docker](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker?view=sql-server-ver16&tabs=cli&pivots=cs1-bash)** locally on your own as the database.

> [!CAUTION]
> Although there are free tiers for Azure SQL and AWS EC2 instances, <ins>please be aware that costs may incur with these services.</ins><br/> **I am not responsible for any costs that occur.**

### Prerequisites
- To run on local/development, install the following on your local machine:
  - **[Docker]**(https://www.docker.com/products/docker-desktop/)
- To deploy on AWS via Terraform, install the following on your local machine:
  - Install **[Terraform CLI]**(https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli)  
  - Create an AWS account
  - Install and configure AWS CLI

### How to start Airflow locally
There is a powershell script setup.sh that contains scripted functions to bring containers up, down, and restart them (locally).

👆 To bring up the environment, run the following command:
```
sh setup.sh start
```

👇 To bring down the environment, run the following command:
```
sh setup.sh down
```

🔄 To restart the environment, run the following command:
```
sh setup.sh restart
```
