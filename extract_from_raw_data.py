import re
from bs4 import BeautifulSoup
from datetime import datetime
from get_data_from_website import (get_ranking_from_match,
                                   get_scores,
                                   get_all_matches,
                                   get_last5_from_match,
                                   get_odds)


def is_timestamp_passed(timestamp_num):
    timestamp_dt = datetime.strptime(str(timestamp_num), "%Y%m%d%H%M")
    return timestamp_dt < datetime.now()


def extract_matches_on_mainboard():

    matches = {}
    raw_data = get_all_matches()

    soup = BeautifulSoup(raw_data, "html.parser")
    board = soup.find("div", id="score-data")

    current_championship = None
    match_time = None
    today_date = datetime.today().strftime("%Y%m%d")

    for element in board.find_all():
        if element.name == "h4":
            current_championship = element.get_text(strip=True).replace("Classifiche", "")
        elif element.name == "span" and not element.get("class"):
            raw_time = element.get_text(strip=True)
            try:
                match_time = f"{today_date}{raw_time.replace(':', '')}"
            except ValueError:
                match_time = None
        if element.get("class"):
            if element.name == "a" and "sched" in element.get("class"):
                match_url = element.get("href")
                match_text = element.find_previous(string=True).strip()

                matches[match_text] = {'CAMPIONATO': current_championship,
                                       'MATCH_CODE': match_url.split('/')[2],
                                       'MATCH_TIME': match_time
                                       }

    return matches


def extract_scores(prompt):

    scores = {}
    raw_data = get_scores(prompt)
    matches = re.findall(r'AC\u00f7(\d) Tempo\u00acIG\u00f7(\d+)\u00acIH\u00f7(\d+)', raw_data)

    for match in matches:
        tempo = f"{match[0]}"
        scores[tempo] = f"{match[1]}-{match[2]}"

    return scores


def extract_last5(prompt, type_prompt):

    data = get_last5_from_match(prompt, type_prompt)
    rankings = {}

    if data:

        lines = data.split("\n")

        structured_data = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = re.match(r"([A-Z]+[A-Z0-9]*)[: ](.+)", line)
            if match:
                key, value = match.groups()
                structured_data.append({key: value})

        structured_data = [d for d in structured_data if not any(k in d for k in ["HCN", "HCT", "IPU", "IPI"])]

        rankings = {}

        posizioni_ETN = [i for i, element in enumerate(structured_data) if "ETN" in element]
        sottocategorie = [structured_data[posizioni_ETN[i]: posizioni_ETN[i + 1]] for i in range(len(posizioni_ETN) - 1)]
        sottocategorie.append(structured_data[posizioni_ETN[-1]:])

        def verifica_valore(lista_di_liste):
            for sotto_lista in lista_di_liste:
                if sotto_lista and isinstance(sotto_lista[0], dict):
                    if ' 5' in sotto_lista[0].values():
                        return True
            return False

        if verifica_valore(sottocategorie):

            for value in sottocategorie:
                if value[0]['ETN'].strip() == '5':
                    structured_data = value[1:]
                    break

            posizioni_TN = [i for i, element in enumerate(structured_data) if "TN" in element]
            teams_list = [structured_data[posizioni_TN[i]: posizioni_TN[i + 1]] for i in range(len(posizioni_TN) - 1)]
            teams_list.append(structured_data[posizioni_TN[-1]:])

            for team in teams_list:

                tn_dict = next(d for d in team if "TN" in d)
                nome_squadra = str(tn_dict["TN"]).strip()

                tg_dict = next(d for d in team if "TG" in d)
                goal = str(tg_dict["TG"]).strip()

                tm_dict = next(d for d in team if "TM" in d)
                partite_giocate = int(str(tm_dict["TM"]).strip())

                if partite_giocate == 5:
                    goal_fatti = int(goal.split(':')[0])
                    goal_subiti = int(goal.split(':')[1])
                else:
                    goal_fatti = 0
                    goal_subiti = 0

                posizioni_LMU = [i for i, element in enumerate(team) if "LMU" in element]

                matches_dict = {}
                if posizioni_LMU:
                    matches_list = [team[posizioni_LMU[i]: posizioni_LMU[i + 1]] for i in range(len(posizioni_LMU) - 1)]
                    matches_list.append(team[posizioni_LMU[-1]:])

                    if len(matches_list) == 6:
                        i = 1
                        for match in matches_list[-5:]:
                            lme_dict = next(d for d in match if "LME" in d)
                            link_partita = str(lme_dict["LME"]).strip()
                            matches_dict[f'Partita {i}'] = link_partita
                            i += 1

                rankings[nome_squadra] = {'GFF5': goal_fatti,
                                          'GSF5': goal_subiti,
                                          'PARTITE': matches_dict}

    return rankings


def extract_ranking(prompt, type_prompt):

    data = get_ranking_from_match(prompt, type_prompt)
    rankings = {}

    if data:

        lines = data.split("\n")

        structured_data = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = re.match(r"([A-Z]+[A-Z0-9]*)[: ](.+)", line)
            if match:
                key, value = match.groups()
                structured_data.append({key: value})

        structured_data = [d for d in structured_data if not any(k in d for k in ["HCN", "HCT", "IPU", "IPI"])]

        rankings = {}

        posizioni_TN = [i for i, element in enumerate(structured_data) if "TN" in element]
        teams_list = [structured_data[posizioni_TN[i]: posizioni_TN[i + 1]] for i in range(len(posizioni_TN) - 1)]
        teams_list.append(structured_data[posizioni_TN[-1]:])

        for team in teams_list:

            tn_dict = next(d for d in team if "TN" in d)
            nome_squadra = str(tn_dict["TN"]).strip()

            tg_dict = next(d for d in team if "TG" in d)
            goal = str(tg_dict["TG"]).strip()
            goal_fatti = int(goal.split(':')[0])
            goal_subiti = int(goal.split(':')[1])

            tm_dict = next(d for d in team if "TM" in d)
            partite_giocate = int(str(tm_dict["TM"]).strip())

            rankings[nome_squadra] = {'GFC': goal_fatti,
                                      'GSC': goal_subiti,
                                      'PG': partite_giocate}

    return rankings


def extract_odds_bet365(prompt):

    data = get_odds(prompt)
    lines = data.split("¬")
    structured_data = []
    odds = {}

    if data:

        for line in lines:
            line = line.strip()
            if not line:
                continue

            match = re.match(r"([^÷]+)÷([^÷]+)", line)
            if match:
                key, value = match.groups()
                structured_data.append({key: value})

        structured_data = [
            {k.replace('~', ''): v for k, v in d.items()} if isinstance(d, dict) else d
            for d in structured_data
        ]

        structured_data = [d for d in structured_data if not any(k in d for k in ["OPI", "OE"])]

        posizioni_OA = [i for i, element in enumerate(structured_data) if "OA" in element]

        if posizioni_OA:
            type_odds = [structured_data[posizioni_OA[i]: posizioni_OA[i + 1]] for i in range(len(posizioni_OA) - 1)]
            type_odds.append(structured_data[posizioni_OA[-1]:])

            for type_odd in type_odds:

                type_odd_str = str(type_odd[0]['OA']).strip()

                if type_odd_str in ['1X2', 'O/U', 'Gol']:

                    posizioni_OB = [i for i, element in enumerate(type_odd) if "OB" in element]
                    odds_description = [type_odd[posizioni_OB[i]: posizioni_OB[i + 1]] for i in
                                        range(len(posizioni_OB) - 1)]
                    odds_description.append(type_odd[posizioni_OB[-1]:])

                    for odd_description in odds_description:

                        odd_description_str = str(odd_description[0]['OB']).strip()

                        if odd_description_str == 'Finale':

                            posizioni_OC = [i for i, element in enumerate(odd_description) if "OC" in element]
                            if posizioni_OC:
                                quota_names = [odd_description[posizioni_OC[i]: posizioni_OC[i + 1]] for i in
                                               range(len(posizioni_OC) - 1)]
                                quota_names.append(odd_description[posizioni_OC[-1]:])
                            else:
                                quota_names = [odd_description]

                            for quota in quota_names:

                                lx_dict = next((d for d in quota if "LX" in d), None)
                                type_quota_1 = str(lx_dict["LX"]).strip() if lx_dict else None

                                ly_dict = next((d for d in quota if "LY" in d), None)
                                type_quota_2 = str(ly_dict["LY"]).strip() if ly_dict else None

                                lz_dict = next((d for d in quota if "LZ" in d), None)
                                type_quota_3 = str(lz_dict["LZ"]).strip() if lz_dict else None

                                if 'OC' in quota[0]:
                                    oc_str = str(quota[0]['OC']).strip()
                                    if type_quota_1:
                                        type_quota_1 += ' ' + oc_str
                                    if type_quota_2:
                                        type_quota_2 += ' ' + oc_str
                                    if type_quota_3:
                                        type_quota_3 += ' ' + oc_str
                                else:
                                    oc_str = ''

                                posizioni_OD = [i for i, element in enumerate(quota) if "OD" in element]
                                bookmakers = [quota[posizioni_OD[i]: posizioni_OD[i + 1]] for i in range(len(posizioni_OD) - 1)]
                                bookmakers.append(quota[posizioni_OD[-1]:])

                                bookmakers_dict = {}
                                for bookmaker in bookmakers:
                                    bookmaker_str = str(bookmaker[0]['OD']).strip()

                                    if bookmaker_str == 'bet365.it':

                                        xa_dict = next((d for d in bookmaker if "XA" in d), None)
                                        quota_1 = str(xa_dict["XA"]).strip() if xa_dict else None

                                        xb_dict = next((d for d in bookmaker if "XB" in d), None)
                                        quota_2 = str(xb_dict["XB"]).strip() if xb_dict else None

                                        xc_dict = next(d for d in bookmaker if "XC" in d)
                                        quota_3 = str(xc_dict["XC"]).strip()

                                        quota_pairs = [
                                            (type_quota_1, quota_1),
                                            (type_quota_2, quota_2),
                                            (type_quota_3, quota_3),
                                        ]

                                        quote_dict = {}
                                        for type_quota, x in quota_pairs:
                                            if type_quota is not None and x is not None:
                                                quote_dict[type_quota] = x

                                        bookmakers_dict[bookmaker_str] = quote_dict

                                odds[f'{type_odd_str} {odd_description_str} {oc_str}'.strip()] = bookmakers_dict
    return odds
