import re
import json
from load_df_result import check_file_df_result
from extract_from_raw_data import extract_odds_bet365


def process_quotes(quotes):
    match = re.match(r"^([\d.]+)(?:\[(.)]([\d.]+))?$", str(quotes))
    if match:
        base_value = match.group(1)
        modifier = match.group(2)
        right_value = match.group(3)

        if modifier and right_value:
            return right_value
        return base_value
    return quotes


def reload_odds():
    df_result = check_file_df_result()

    for key, value in df_result.items():
        e = extract_odds_bet365(value['MATCH_CODE'])
        over25 = process_quotes(e.get('O/U Finale 2.5', {}).get('bet365.it', {}).get('Over 2.5', '0'))
        under25 = process_quotes(e.get('O/U Finale 2.5', {}).get('bet365.it', {}).get('Under 2.5', '0'))
        if over25 > 0 and under25 > 0:
            pov05 = 1 - (691 * over25 - 266 * under25) / (2500 * under25 * over25)
            value['ODDS']['POV05'] = f'{round(pov05*100, 2)}%'

    with open("df_result.json", "w", encoding="utf-8") as file:
        json.dump(df_result, file, indent=4)
