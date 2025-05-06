import base64
import re
import math


def decode_base64(data, altchars=b"+/"):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.
    """
    # taken from stack overflow with love
    data = re.sub(rb"[^a-zA-Z0-9%s]+" % altchars, b"", data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b"=" * (4 - missing_padding)
    return base64.b64decode(data, altchars)


def get_stats_from_save(save_data: str) -> dict:
    """returns Stats, breaks like fucking crazy"""
    if isinstance(save_data, str):
        save_data = bytes(save_data, "utf-8")
    save_bytes = decode_base64(save_data)
    if save_bytes is False:  # L Bozo
        return False, False, False, False
    str_data = save_bytes.decode("utf-8", "replace")
    str_data = str_data.split("|")  # Naughty Naughty Ort :>
    version = float(str_data[0])
    spl = str_data[2].split(";")
    bakery_name = spl[3] if spl[3] else "Default Bakery"

    spl = str_data[4].split(";")
    cookies_keys = [
        "cookies",
        "cookiesEarned",
        "cookieClicks",
        "goldenClicks",
        "handmadeCookies",
        "missedGoldenClicks",
        "bgType",
        "milkType",
        "cookiesReset",
        "elderWrath",
        "pledges",
        "pledgeT",
        "nextResearch",
        "researchT",
        "resets",
        "goldenClicksLocal",
        "cookiesSucked",
        "wrinklersPopped",
        "santaLevel",
        "reindeerClicked",
        "seasonT",
        "seasonUses",
        "season",
        "wrinklers_amount",
        "wrinklers_number",
        "prestige",
        "heavenlyChips",
        "heavenlyChipsSpent",
        "heavenlyCookies",
        "ascensionMode",
        "permanentUpgrades",
        "dragonLevel",
        "dragonAura",
        "dragonAura2",
        "chimeType",
        "volume",
        "wrinklers_shinies",
        "wrinklers_amountShinies",
        "lumps",
        "lumpsTotal",
        "lumpT",
        "lumpRefill",
        "lumpCurrentType",
        "vault",
        "heralds",
        "fortuneGC",
        "fortuneCPS",
        "cookiesPsRawHighest",
        "volumeMusic",
        "cookiesSent",
        "cookiesReceived",
    ]

    stats = {
        cookies_keys[i]: str(spl[i]) if i < len(spl) else None
        for i in range(len(cookies_keys))
    }
    cbat = int(float(stats["cookiesEarned"])) + int(float(stats["cookiesReset"]))
    stats["cookiesBakedAllTime"] = cbat
    stats["bakeryName"] = bakery_name
    stats["version"] = version
    return stats


QUANTIFIABLE = {
    "Cookies Baked All Time (CBAT)": "cookiesBakedAllTime",
    "Total Ascensions": "resets",
    "Total Golden Cookie Clicks": "goldenClicks",
    "Missed Golden Cookies": "missedGoldenClicks",
    "Wrinklers Popped": "wrinklersPopped",
    "Total Cookies Received": "cookiesReceived",
    "Total Cookies Sent": "cookiesSent",
}

INFO = {"version": "version", "bakeryName": "bakeryName"}


formatLong = [
    " thousand",
    " million",
    " billion",
    " trillion",
    " quadrillion",
    " quintillion",
    " sextillion",
    " septillion",
    " octillion",
    " nonillion",
]
prefixes = [
    "",
    "un",
    "duo",
    "tre",
    "quattuor",
    "quin",
    "sex",
    "septen",
    "octo",
    "novem",
]
suffixes = [
    "decillion",
    "vigintillion",
    "trigintillion",
    "quadragintillion",
    "quinquagintillion",
    "sexagintillion",
    "septuagintillion",
    "octogintillion",
    "nonagintillion",
]


for i in suffixes:
    for ii in prefixes:
        formatLong.append(" " + ii + i)

formatShort = ["k", "M", "B", "T", "Qa", "Qi", "Sx", "Sp", "Oc", "No"]
prefixes = ["", "Un", "Do", "Tr", "Qa", "Qi", "Sx", "Sp", "Oc", "No"]
suffixes = ["D", "V", "T", "Qa", "Qi", "Sx", "Sp", "O", "N"]

for i in suffixes:
    for ii in prefixes:
        formatShort.append(" " + ii + i)
formatShort[10] = "Dc"


def formatEveryThirdPower(notations: list):
    def format(val):
        base = 0
        notation_value = 0
        if val >= 1_000_000:
            val /= 1000
            while round(val) >= 1000:
                val /= 1000
                base += 1
            if base >= len(notations):
                return "Infinity"
            else:
                notation_value = notations[base]
        return str(round(val * 1000) / 1000) + str(notation_value)
    return format


number_formatters = {
    "short": formatEveryThirdPower(formatShort),
    "long": formatEveryThirdPower(formatLong),
}


def beautify(val, floats=0, format="long"):
    """stolen graciously from ort, who stole it from frozen cookies"""
    negative = val < 0
    decimal = ""
    fixed = round(val, floats)

    if floats > 0 and abs(val) < 1000 and math.floor(fixed) != fixed:
        decimal = "." + str(fixed).split(".")[1]
    val = math.floor(abs(val))

    if floats > 0 and fixed == val + 1: # I have genuinely no idea what this does
        val += 1

    assert format in number_formatters # we got an internal issue if not lol
    formatter = number_formatters[format]

    if "e+" in str(val) and format == "short":
        output = "{:.3f}".format(val)
    else:
        output = re.sub(r"\B(?=(\d{3})+(?!\d))", ",", formatter(val))
    if output == 0:
        negative = False
    return "-" + output if negative else output + decimal


if __name__ == "__main__":
    # For testing purposes
    example_save = "SAVE HERE"
    stats = get_stats_from_save(example_save)

    # Glorious.
    print(f"4.343x10^102 (l)-> {beautify(4.343*10**102)}")  # Outputs: '1 Tretrigintillion'
    print(f"10^202 (l) -> {beautify(1.00 * 10**202)}")  # Outputs: '1.23 billion'
    print(f"10^202 (s) -> {beautify(1.00 * 10**202, format="short")}")  # Outputs: '1.23 billion'
    print(f"10^5 (l)-> {beautify(1.00 * 10**5)}")  # Outputs: '1.23 billion'
