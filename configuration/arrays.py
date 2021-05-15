import discord
import configuration.variables as variables

# Dictionary Configuration
CHANNELINFORMATION = {
    variables.SERVERRULES: {"Bot": False, "Lockdown": False, "Say": False, "Voice": None}, # Channel #server-rules
    variables.MESSAGEBOARD: {"Bot": False, "Lockdown": False, "Say": True, "Voice": None}, # Channel #message-board.
    variables.EVERYBODYVOTES: {"Bot": False, "Lockdown": False, "Say": False}, "Voice": None, # Channel #everybody-votes.
    variables.GENERALHANGOUT: {"Bot": False, "Lockdown": True, "Say": True, "Voice": variables.GENERALVCHAT}, # Channel #general-hangout.
    variables.RANDOMHANGOUT: {"Bot": False, "Lockdown": True, "Say": True, "Voice": variables.RANDOMVCHAT}, # Channel #random-hangout.
    variables.ELITEHANGOUT: {"Bot": True, "Lockdown": False, "Say": True, "Voice": variables.ELITEVCHAT}, # Channel #elite-hangout.
    variables.STAFFHANGOUT: {"Bot": True, "Lockdown": False, "Say": True, "Voice": variables.STAFFVCHAT}, # Channel #staff-hangout.
    variables.NOMICROPHONE: {"Bot": False, "Lockdown": True, "Say": True, "Voice": None}, # Channel #no-microphone.
    variables.BOTCOMMANDS: {"Bot": True, "Lockdown": True, "Say": True, "Voice": None}, # Channel #bot-commands.
    variables.DIRECTHANGOUT: {"Bot": False, "Lockdown": True, "Say": True, "Voice": variables.DIRECTVCHAT}, # Channel #direct-hangout.
    variables.EVENTHANGOUT: {"Bot": False, "Lockdown": True, "Say": True, "Voice": variables.EVENTVCHAT}, # Channel #event-hangout.
    variables.GITHUBLOGS: {"Bot": False, "Lockdown": False, "Say": False, "Voice": None}, # Channel #bot-logs.
    variables.REQUESTLOGS: {"Bot": False, "Lockdown": False, "Say": False, "Voice": None}, # Channel #request-logs.
    variables.ACTIONLOGS: {"Bot": False, "Lockdown": False, "Say": False, "Voice": None}, # Channel #action-logs.
    variables.SERVERLOGS: {"Bot": False, "Lockdown": False, "Say": False, "Voice": None}, # Channel #server-logs.
}

ROLEINFORMATION = {
    variables.SERVERBOT: {"Nick": "Bot", "Staff": True, "Public": False}, # Role @Server Bot.
    variables.SERVEROWNER: {"Nick": "Owner", "Staff": True, "Public": False}, # Role @Server Owner.
    variables.SERVERMODERATOR: {"Nick": "Moderator", "Staff": True, "Public": False}, # Role @Server Moderator.
    variables.SERVERAFFILIATE: {"Nick": "Affiliate", "Staff": False, "Public": False}, # Role @Server Affiliate.
    variables.SERVERBOOSTER: {"Nick": "Booster", "Staff": False, "Public": False}, # Role @Server Booster.
    variables.BOTCONTRIBUTOR: {"Nick": "Contributor", "Staff": False, "Public": False}, # Role @Bot Contributor.
    variables.CONTENTCREATOR: {"Nick": "Creator", "Staff": False, "Public": False}, # Role @Content Creator.
    variables.ELITEMEMBER: {"Nick": "Elite", "Staff": False, "Public": False}, # Role @Elite Member.
    variables.GAMENIGHTPLAYER: {"Nick": "GameNight", "Staff": False, "Public": True}, # Role @Game Night Player.
}

# Other Settings
INVITECODES = {
    "Nincord": "mYjeaZQ",
    "Puginator": "Yh2zWxugVE",
    "Resistance": "ab6P4gB",
}