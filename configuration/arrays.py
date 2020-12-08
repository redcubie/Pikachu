import discord
import configuration.variables as variables

# Dictionary Configuration
CHANNELINFORMATION = {
    variables.SERVERRULES: {"Bot": False, "Lockdown": False, "Filter": False, "Say": False}, # Channel #server-rules
    variables.ANNOUNCEMENTS: {"Bot": False, "Lockdown": False, "Filter": False, "Say": True}, # Channel #announcements.
    variables.EVERYBODYVOTES: {"Bot": False, "Lockdown": False, "Filter": False, "Say": False}, # Channel #everybody-votes.
    variables.GENERALCHAT: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #general-chat.
    variables.RANDOMCHAT: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #random-chat.
    variables.TRUSTEDCHAT: {"Bot": True, "Lockdown": False, "Filter": False, "Say": True}, # Channel #trusted-chat.
    variables.MODERATORCHAT: {"Bot": True, "Lockdown": False, "Filter": False, "Say": True}, # Channel #moderator-chat.
    variables.BOTCOMMANDS: {"Bot": True, "Lockdown": True, "Filter": True, "Say": True}, # Channel #bot-commands.
    variables.BOTDISCUSSION: {"Bot": True, "Lockdown": False, "Filter": False, "Say": True}, # Channel #bot-discussion.
    variables.SMASHGENERAL: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #smash-general.
    variables.SMASHBATTLES: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #smash-battles.
    variables.POKEMONGENERAL: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #pokémon-general.
    variables.POKEMONTRADES: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #pokémon-trades.
    variables.POKEMONBATTLES: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #pokémon-battles.
    variables.DIRECTCHAT: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #direct-chat.
    variables.EVENTCHAT: {"Bot": False, "Lockdown": True, "Filter": True, "Say": True}, # Channel #event-chat.
    variables.BOTLOGS: {"Bot": False, "Lockdown": False, "Filter": False, "Say": False}, # Channel #bot-logs.
    variables.REQUESTLOGS: {"Bot": False, "Lockdown": False, "Filter": False, "Say": False}, # Channel #request-logs.
    variables.ACTIONLOGS: {"Bot": False, "Lockdown": False, "Filter": False, "Say": False}, # Channel #action-logs.
    variables.MESSAGELOGS: {"Bot": False, "Lockdown": False, "Filter": False, "Say": False}, # Channel #message-logs.
    variables.SERVERLOGS: {"Bot": False, "Lockdown": False, "Filter": False, "Say": False}, # Channel #server-logs.
}

ROLEINFORMATION = {
    variables.SERVERBOT: {"Nick": "Bot", "Staff": True, "Public": False}, # Role @Server Bot.
    variables.SERVEROWNER: {"Nick": "Owner", "Staff": True, "Public": False}, # Role @Server Owner.
    variables.SERVERMODERATOR: {"Nick": "Moderator", "Staff": True, "Public": False}, # Role @Server Moderator.
    variables.SERVERAFFILIATE: {"Nick": "Affiliate", "Staff": False, "Public": False}, # Role @Server Affiliate.
    variables.SERVERBOOSTER: {"Nick": "Booster", "Staff": False, "Public": False}, # Role @Server Booster.
    variables.BOTCONTRIBUTOR: {"Nick": "Contributor", "Staff": False, "Public": False}, # Role @Bot Contributor.
    variables.CONTENTCREATOR: {"Nick": "Creator", "Staff": False, "Public": False}, # Role @Content Creator.
    variables.TRUSTEDMEMBER: {"Nick": "Trusted", "Staff": False, "Public": False}, # Role @Trusted Member.
    variables.GAMENIGHTPLAYER: {"Nick": "GameNight", "Staff": False, "Public": True}, # Role @Game Night Player.
}

# Array Configuration
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

# Other Settings
INVITECODES = {
    "Nincord": "mYjeaZQ",
    "Apple": "cnNdKdg",
    "Resistance": "ab6P4gB",
}