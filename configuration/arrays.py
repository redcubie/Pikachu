import discord
import configuration.variables as variables

# Group Configuration
STAFFROLES = [
    variables.SERVEROWNER, # Role @Server Owner.
    variables.SERVERMODERATOR, # Role @Server Moderator.
    variables.SERVERBOT, # Role @Server Bot.
]

BOTCHANNELS = [
    variables.TRUSTEDCHAT, # Channel #trusted-chat.
    variables.MODERATORCHAT, # Channel #moderator-chat.
    variables.BOTCOMMANDS, # Channel #bot-commands.
    variables.BOTDISCUSSION, # Channel #bot-discussion.
]

LOCKDOWNCHANNELS = [
    variables.GENERALCHAT, # Channel #general-chat.
    variables.RANDOMCHAT, # Channel #random-chat.
    variables.BOTCOMMANDS, # Channel #bot-commands.
    variables.SMASHGENERAL, # Channel #smash-general.
    variables.SMASHBATTLES, # Channel #smash-battles.
    variables.POKEMONGENERAL, # Channel #pokémon-general.
    variables.POKEMONTRADES, # Channel #pokémon-trades.
    variables.POKEMONBATTLES, # Channel #pokémon-battles.
    variables.DIRECTCHAT, # Channel #direct-chat.
    variables.EVENTCHAT, # Channel #event-chat.
]

LOGCHANNELS = [
    variables.BOTLOGS, # Channel #bot-logs.
    variables.REQUESTLOGS, # Channel #request-logs.
    variables.ACTIONLOGS, # Channel #action-logs.
    variables.MESSAGELOGS, # Channel #message-logs.
    variables.SERVERLOGS, # Channel #server-logs.
]

UNFILTERCHANNELS = [
    variables.BOTDISCUSSION, # Channel #bot-discussion.
    variables.TRUSTEDCHAT, # Channel #trusted-chat.
    variables.MODERATORCHAT, # Channel #moderator-chat.
    variables.BOTLOGS, # Channel #bot-logs.
    variables.REQUESTLOGS, # Channel #request-logs.
    variables.ACTIONLOGS, # Channel #action-logs.
    variables.MESSAGELOGS, # Channel #message-logs.
    variables.SERVERLOGS, # Channel #server-logs.
]

# Program Directories
ROLEINFORMATION = {
    variables.SERVERBOT: {"Nick": "Bot", "Public": False, "Private": False}, # Role @Server Bot.
    variables.SERVEROWNER: {"Nick": "Owner", "Public": False, "Private": False}, # Role @Server Owner.
    variables.SERVERMODERATOR: {"Nick": "Moderator", "Public": False, "Private": False}, # Role @Server Moderator.
    variables.SERVERAFFILIATE: {"Nick": "Affiliate", "Public": False, "Private": True}, # Role @Server Affiliate.
    variables.BOTCONTRIBUTOR: {"Nick": "Contributor", "Public": False, "Private": True}, # Role @Bot Contributor.
    variables.CONTENTCREATOR: {"Nick": "Creator", "Public": False, "Private": True}, # Role @Content Creator.
    variables.TRUSTEDMEMBER: {"Nick": "Trusted", "Public": False, "Private": True}, # Role @Trusted Member.
    variables.PROJECTDEVELOPER: {"Nick": "Developer", "Public": False, "Private": True}, # Role @Project Developer.
    variables.GAMENIGHTPLAYER: {"Nick": "GameNight", "Public": True, "Private": True}, # Role @Game Night Player.
}

# Filter Configuration
MESSAGEFILTER = [
    "freeshop",
    "friishop",
    "freshop",
    "freehop",
    "freesh0p",
    "threeshop",
    "freestore", # Variations of "freeshop."
    "ciangel",
    "tikdevil",
    "tikshop",
    "utikdownloadhelper",
    "utik", # Variation of "utikdownloadhelper."
    "nusspli",
    "nuspli", # Variation of "nusspli."
    "ghosteshop",
    "funkii",
    "funk11",
    "funki",
    "funkey", # Variations of "funkii."
    "usbhelper",
    "villian3ds",
    "vi11ian3ds", # Variation of "villian3ds."
    "wareznx",
    "homebrewgeneralshop",
    "hbgshop", # Variation of "homebrewgeneralshop."
    "goldbrick",
    "stargate",
    "3dsiso",
    "3dscia",
    "wiiuiso",
    "emuparadise",
    "loveroms",
    "coolroms",
    "doperoms",
    "vimm",
    "unbanmii",
    "easymode9",
    "sysconfig",
] # The filter is mostly just piracy-related terms. I'll probably add more soon.