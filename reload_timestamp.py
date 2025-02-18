import json
from load_df_result import check_file_df_result
from extract_from_raw_data import is_timestamp_passed


def reload_timestamp():
    df_result = check_file_df_result()

    for key, value in df_result.items():
        if is_timestamp_passed('MATCH_TIME'):
            del df_result[key]

    with open("df_result.json", "w", encoding="utf-8") as file:
        json.dump(df_result, file, indent=4)