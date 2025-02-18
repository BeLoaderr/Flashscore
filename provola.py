import json


def convert_time(match_time):
    return f"{match_time[8:10]}:{match_time[10:]}"


html_content = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Partite</title>
    <style>
        table { width: 100%%; border-collapse: collapse; margin: 20px 0; font-size: 18px; }
        th, td { border: 1px solid black; padding: 10px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h2>Siete dei salami</h2>
    <table>
        <tr>
            <th>Partita</th>
            <th>Campionato</th>
            <th>Ora</th>
            <th>POV05</th>
            <th>Goal 1° Tempo</th>
            <th>Media Goal</th>
            <th>Media Goal Ultimi 5</th>
        </tr>
"""


file_path = "df_result.json"
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

data = dict(sorted(data.items(), key=lambda x: x[1]["MATCH_TIME"]))
for match, details in data.items():
    match_time = convert_time(details["MATCH_TIME"])
    odds = details["ODDS"]

    html_content += f"""
        <tr>
            <td>{match}</td>
            <td>{details["CAMPIONATO"]}</td>
            <td>{match_time}</td>
            <td>{odds.get("POV05", "N/A")}</td>
            <td>{odds.get("GOAL_PRIMO_TEMPO", "N/A")}</td>
            <td>{odds.get("MEDIA_GOAL_GENERALE", "N/A")}</td>
            <td>{odds.get("MEDIA_GOAL_FORMA_5", "N/A")}</td>
        </tr>
    """

# Chiusura della tabella e della pagina HTML
html_content += """
    </table>
</body>
</html>
"""

# Salvataggio del file HTML
with open("partite.html", "w", encoding="utf-8") as file:
    file.write(html_content)
