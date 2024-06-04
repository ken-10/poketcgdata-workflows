import logging

from discord_webhook import DiscordWebhook, DiscordEmbed


def send_failure_message(webhook_link: str, dag_id: str, task_id: str, log_url: str, run_id: str):
    logging.info("Sending failure discord message...")
    webhook = DiscordWebhook(webhook_link)
    embed = DiscordEmbed(title=f"Airflow Failure - {dag_id}", color='CC0000')
    embed.add_embed_field(name="DAG ID", value=dag_id, inline=True)
    embed.add_embed_field(name="Run ID", value=run_id, inline=True)
    embed.add_embed_field(name="Task", value=task_id, inline=False)
    embed.add_embed_field(name="Log URL", value=f"**[Click here to view log]({log_url})**")
    webhook.add_embed(embed)
    webhook.execute()
    logging.info("Failure message sent")
