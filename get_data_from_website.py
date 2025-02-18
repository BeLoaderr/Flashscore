import requests

headers = {
    "accept": "*/*",
    "accept-language": "it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "no-cache",
    "origin": "https://www.diretta.it",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.diretta.it/",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "x-fsign": "SW9D1eZo",
}


def get_all_matches():
    response = requests.get('https://m.diretta.it/', headers=headers)
    return response.text


def get_ranking_from_match(match, type_ranking):

    if type_ranking == 'CASA':
        url = f"https://400.flashscore.ninja/400/x/feed/df_to_1_{match}_2"
    else:
        url = f"https://400.flashscore.ninja/400/x/feed/df_to_1_{match}_3"

    response = requests.get(url, headers=headers)
    data = response.text.replace("¬", "\n").replace("÷", ": ")
    return data


def get_last5_from_match(match, type_ranking):

    if type_ranking == 'CASA':
        url = f"https://400.flashscore.ninja/400/x/feed/df_to_1_{match}_8"
    else:
        url = f"https://400.flashscore.ninja/400/x/feed/df_to_1_{match}_9"

    response = requests.get(url, headers=headers)
    data = response.text.replace("¬", "\n").replace("÷", ": ")
    return data


def get_scores(match):
    url = f"https://400.flashscore.ninja/400/x/feed/df_sui_1_{match}"
    response = requests.get(url, headers=headers)
    return response.text


def get_odds(match):
    url = f'https://400.flashscore.ninja/400/x/feed/df_od_1_{match}'
    response = requests.get(url, headers=headers)
    return response.text
