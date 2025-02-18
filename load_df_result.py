import os
import json


def check_last5matches_counter(match):

    condition_home = 'CASA' in match and 'PARTITE' in match['CASA'] and match['CASA']['PARTITE'] and all(partita.values() for partita in match["CASA"]["PARTITE"].values())
    condition_away = 'OSPITE' in match and 'PARTITE' in match['OSPITE'] and match['OSPITE']['PARTITE'] and all(partita.values() for partita in match["OSPITE"]["PARTITE"].values())

    if condition_home and condition_away:
        counter = 0
        for team in ['CASA', 'OSPITE']:
            for partita in match[team]["PARTITE"]:
                goal_home, goal_away = match[team]["PARTITE"][partita]['1'].split('-')
                if int(goal_home) > 0 or int(goal_away) > 0:
                    counter += 1
        return counter
    return 0


def check_last5matches_medie(match):

    keys = {'GFC', 'GSC', 'PG', 'GFF5', 'GSF5'}
    condition_home_matches = 'CASA' in match and 'PARTITE' in match['CASA'] and all(partita.values() for partita in match["CASA"]["PARTITE"].values())
    condition_away_matches = 'OSPITE' in match and 'PARTITE' in match['OSPITE'] and all(partita.values() for partita in match["OSPITE"]["PARTITE"].values())
    condition_home = all(k in match['CASA'] for k in keys)
    condition_away = all(k in match['OSPITE'] for k in keys)

    if condition_home_matches and condition_away_matches and condition_home and condition_away and int(match['CASA']['PG']) != 0 and int(match['OSPITE']['PG']) != 0:

        media_goal_casa_generale = (int(match['CASA']['GFC']) + int(match['CASA']['GSC'])) / int(match['CASA']['PG'])
        media_goal_ospite_generale = (int(match['OSPITE']['GFC']) + int(match['OSPITE']['GSC'])) / int(match['OSPITE']['PG'])
        media_goal_generale =  (media_goal_casa_generale + media_goal_ospite_generale) / 2

        media_goal_last5_1 = (int(match['CASA']['GFF5']) + int(match['OSPITE']['GSF5'])) / 2
        media_goal_last5_2 = (int(match['OSPITE']['GFF5']) + int(match['CASA']['GSF5'])) / 2
        media_goal_last5 = (media_goal_last5_1 + media_goal_last5_2) / 5

        return media_goal_generale, media_goal_last5
    return 0, 0


def check_file_df_result():
    if not os.path.exists("df_result.json"):
        df_result = {}
        with open("df_result.json", "w", encoding="utf-8") as file:
            json.dump(df_result, file, indent=4)
    with open("df_result.json", "r", encoding="utf-8") as file:
        df_result = json.load(file)
    return df_result


def load_df_result():

    if not os.path.exists("matches_data.json"):
        raise FileNotFoundError("Errore: 'matches_data.json' non esiste. Il programma si interrompe.")

    check_file_df_result()

    with open("matches_data.json", "r", encoding="utf-8") as file:
        matches_data = json.load(file)

    df_result = check_file_df_result()

    for key, value in matches_data.items():
        if key not in df_result:
            over25 = float(value['ODDS']['OVER 2.5'])
            under25 = float(value['ODDS']['UNDER 2.5'])
            if over25 > 0 and under25 > 0:
                pov05 = 1 - (691 * over25 - 266 * under25) / (2500 * under25 * over25)
                counter = check_last5matches_counter(value)
                medie_goal = check_last5matches_medie(value)
                if pov05 > 0.85 and counter > 7 and min(medie_goal) > 2.8 or pov05 > 0.95:
                    df_result[key] = {
                        "CAMPIONATO": value['CAMPIONATO'],
                        "MATCH_CODE": value['MATCH_CODE'],
                        "MATCH_TIME": value['MATCH_TIME'],
                        "ODDS": {
                            "POV05": f'{round(pov05*100, 2)}%',
                            "GOAL_PRIMO_TEMPO": str(counter) if counter != 0 else 'NO DATA',
                            "MEDIA_GOAL_GENERALE": str(round(medie_goal[0], 2)) if medie_goal[0] != 0 else 'NO DATA',
                            "MEDIA_GOAL_FORMA_5": str(round(medie_goal[1], 2)) if medie_goal[1] != 0 else 'NO DATA'
                        }
                    }

    with open("df_result.json", "w", encoding="utf-8") as file:
        json.dump(df_result, file, indent=4)
