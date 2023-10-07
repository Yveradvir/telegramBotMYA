import os

with open("config.py", "w") as file:
    lines = [
        "BOT_TOKEN   =\n",
        "ADMINS      = []\n\n",
        "IP          =\n",
        "PGUSER      =\n",
        "PGPASSWORD  =\n",
        "DBNAME      =\n",
        "DBPORT      =\n"
    ]

    file.write("".join(lines))