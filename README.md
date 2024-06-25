# PokeTCGData Workflows
Automated system to ingest daily Pokemon TCG pricing data from **[Pokemon TCG IO API](https://docs.pokemontcg.io/)**.
<br/>The data is displayed in a live dashboard that can be found here. (Coming soon)

> [!NOTE]
> The way this project is deployed/architected may not make sense due to budgeting and to better learn the applications being used.

# Architecture
![Architecture Diagram](/assets/images/poketcgworkflows_highlevel_diagram_3.jpg)

### Tools
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=Apache%20Airflow&logoColor=white) ![dbt](https://img.shields.io/badge/dbt-FF694B?style=for-the-badge&logo=dbt&logoColor=white) ![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white) ![AWS](https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)

### Database
![Azure SQL](https://img.shields.io/badge/azure%20sql-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)

## How to start
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
