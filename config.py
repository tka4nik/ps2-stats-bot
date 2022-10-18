import configparser
from logger import GeneralLogger

factions = {
    1: "<:vs:441405448113881098>",
    2: "<:nc:441405432091901972>",
    3: "<:tr:441405413745754112>"
}

continents_list = {
    2: ['2201', '2202', '2203'],
    4: ['4230', '4240', '4250'],
    6: ['6001', '6002', '6003'],
    8: ['18029', '18030', '18062'],
    344: ['18303', '18304', '18305']
}  # Array of region ids of all warpgates for each continent

zones = {   # Array of ids for each zone
    2: 'Indar',
    4: "Hossin",
    6: "Amerish",
    8: "Esamir",
    344: "Oshur"
}

servers = {
    17: 'Emerald',
    1: 'Connery',
    13: 'Cobalt',
    10: 'Miller',
    40: 'Soltech'
}

war_assets_list = [
    "A.N.V.I.L. (Light)",
    "A.N.V.I.L. (Medium)",
    "A.N.V.I.L. (Heavy)",
    "Orbital Strike",
    "Steel Rain"
]

general = {
    "SERVICE_ID": "",
    "DISCORD_TOKEN": "",
    "DISCORD_GUILD": "",
    "DISCORD_GUILD_ID": "",
}


def get_config(path):
    logger = GeneralLogger()
    parser = configparser.ConfigParser()

    parser.read(path)
    print(parser.sections())

    general["SERVICE_ID"] = parser.get("CENSUS", "SERVICE_ID")
    general["DISCORD_TOKEN"] = parser.get("DISCORD", "DISCORD_TOKEN")
    general["DISCORD_GUILD"] = parser.get("DISCORD", "DISCORD_GUILD")
    general["DISCORD_GUILD_ID"] = parser.get("DISCORD", "DISCORD_GUILD_ID")

    logger.LogInfo("Loaded config", "%d/%m/%y;%H:%M:%S")
