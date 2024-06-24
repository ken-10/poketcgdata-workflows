# PokeTCGData Workflows
Automated system to ingest daily Pokemon TCG pricing data from **[Pokemon TCG IO API](https://docs.pokemontcg.io/)**.

> [!NOTE]
> The way this project is deployed/architected may not make sense due to budgeting and to better learn the applications being used.

# Architecture
![Architecture Diagram](/assets/images/poketcgworkflows_highlevel_diagram_3.jpg)

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
