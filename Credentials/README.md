Put your Google API json in a file named "GoogleAPI.json".

config.json:
```json
{
        "sql-driver": "ODBC Driver 17 for SQL Server",
        "sql-database": "LostWorld",
        "sql-server": "<IP_ADDRESS|DOCKER_CONTAINER>",
        "sql-uid": "<SQL_USER>",
        "sql-pwd": "{<SQL_PASSWORD>}",
        "sql-port": "1433",
        "spreadsheet-id": "<GOOGLE_SHEET_ID>",
        "log-channel-id": <DISCORD_CHANNEL_ID>,
        "auction-channel-id": <DISCORD_CHANNEL_ID>
}
```

PatreonConfig.json:
```json
{
  "enabled": true,
  "roles":
  {
    "extra-character": "Extra Character"
  }
}
```
