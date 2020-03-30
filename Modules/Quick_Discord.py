async def log_to_discord(self, log: str):
    log_channel = self.bot.get_channel(689614915253567564)
    await log_channel.send(log)
