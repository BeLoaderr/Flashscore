from reload_odds import process_quotes
import json
from extract_from_raw_data import (
    extract_ranking,
    extract_scores,
    extract_matches_on_mainboard,
    extract_last5,
    extract_odds_bet365
)


def extract_result_from_match(data):
    if 'PARTITE' in data:
        games = data['PARTITE']
        if games:
            for game in games:
                games[game] = extract_scores(games[game])


def process_match(match, value):
    home, away = match.split(' - ')

    general_ranking_home = extract_ranking(value['MATCH_CODE'], 'CASA')
    general_ranking_away = extract_ranking(value['MATCH_CODE'], 'OSPITE')
    last5_ranking_home = extract_last5(value['MATCH_CODE'], 'CASA')
    last5_ranking_away = extract_last5(value['MATCH_CODE'], 'OSPITE')

    a = general_ranking_home.get(home, {})
    b = last5_ranking_home.get(home, {})
    c = general_ranking_away.get(away, {})
    d = last5_ranking_away.get(away, {})

    extract_result_from_match(b)
    extract_result_from_match(d)

    value['CASA'] = a | b
    value['OSPITE'] = c | d

    e = extract_odds_bet365(value['MATCH_CODE'])

    odds = {
        'OVER 2.5': process_quotes(e.get('O/U Finale 2.5', {}).get('bet365.it', {}).get('Over 2.5', '0')),
        'UNDER 2.5': process_quotes(e.get('O/U Finale 2.5', {}).get('bet365.it', {}).get('Under 2.5', '0')),
    }

    value['ODDS'] = odds


def merge_main_odds():
    matches = extract_matches_on_mainboard()
    counter = 0
    for match, value in matches.items():
        process_match(match, value)
        counter += 1
        print(f'{counter} / {len(matches)}')

    with open('matches_data.json', "w", encoding="utf-8") as json_file:
        json.dump(matches, json_file, indent=4, ensure_ascii=False)
