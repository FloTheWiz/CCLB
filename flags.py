from pathlib import Path
import logging
import json

logger = logging.getLogger(__name__)
data_path = Path("data")
flags_path = data_path / "flags"
country_json_path = flags_path / "country.json"


# ! These need changing whenever the file structure changes.
def get_country_json() -> dict:
    try:
        with open(country_json_path) as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Config file not found. Please ensure 'country.json' exists.")
        raise


def parse_country_json(list) -> dict:
    output = {}
    for country in list:
        if bool(country["iso"]):
            output[country["code"]] = country
    return output


def get_flag_files() -> dict:
    """
    Returns:
        dict: "1x1":{"flag":"flag.svg"},"4x3":{"flag":"flag.svg"}
    """
    ref_table = {}
    for top_file in flags_path.iterdir():
        if top_file.is_dir():
            ref_table[top_file.name] = {}
            for sub_file in top_file.iterdir():
                ref_table[top_file.name][
                    sub_file.name.replace(".svg", "")
                ] = sub_file.name
    return ref_table


country_json = get_country_json()
country_json.sort(key=lambda x: x["name"])
country_codes = [flag["code"] for flag in country_json]

flag_files = get_flag_files()


def check_codes():
    """Checks all filenames are in country.json,
    and all codes are filenames
    """
    result = True
    error = ""
    for size in flag_files:
        for flag, filename in flag_files[size].items():
            if flag not in country_codes:
                error += "Flag {} is missing from country.json | ".format(flag)
                result = False
    for code in country_codes:
        if code not in flag_files["4x3"]:
            error += "Flag {} is missing from /4x3 | ".format(code)
            result = False
        if code not in flag_files["1x1"]:
            error += "Flag {} is missing from /1x1 | ".format(code)
            result = False
    return result, error


def run_flag_tests() -> bool:
    result, error = check_codes()
    if result:
        logger.info("Flag Checks Passed")
    else:
        logger.error(f"Flag Checks NOT Passed: CHECKS: {result} :: {error}")
    return result
