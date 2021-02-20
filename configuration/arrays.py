import discord
import configuration.variables as variables

# Dictionary Configuration
CHANNELINFORMATION = {
    variables.SERVERRULES: {"Bot": False, "Lockdown": False, "Say": False}, # Channel #server-rules
    variables.ANNOUNCEMENTS: {"Bot": False, "Lockdown": False, "Say": True}, # Channel #announcements.
    variables.EVERYBODYVOTES: {"Bot": False, "Lockdown": False, "Say": False}, # Channel #everybody-votes.
    variables.GENERALCHAT: {"Bot": False, "Lockdown": True, "Say": True}, # Channel #general-chat.
    variables.RANDOMCHAT: {"Bot": False, "Lockdown": True, "Say": True}, # Channel #random-chat.
    variables.TRUSTEDCHAT: {"Bot": True, "Lockdown": False, "Say": True}, # Channel #trusted-chat.
    variables.MODERATORCHAT: {"Bot": True, "Lockdown": False, "Say": True}, # Channel #moderator-chat.
    variables.NOMICROPHONE: {"Bot": False, "Lockdown": True, "Say": True}, # Channel #no-microphone.
    variables.BOTCOMMANDS: {"Bot": True, "Lockdown": True, "Say": True}, # Channel #bot-commands.
    variables.DIRECTCHAT: {"Bot": False, "Lockdown": True, "Say": True}, # Channel #direct-chat.
    variables.EVENTCHAT: {"Bot": False, "Lockdown": True, "Say": True}, # Channel #event-chat.
    variables.GITHUBLOGS: {"Bot": False, "Lockdown": False, "Say": False}, # Channel #bot-logs.
    variables.REQUESTLOGS: {"Bot": False, "Lockdown": False, "Say": False}, # Channel #request-logs.
    variables.ACTIONLOGS: {"Bot": False, "Lockdown": False, "Say": False}, # Channel #action-logs.
    variables.SERVERLOGS: {"Bot": False, "Lockdown": False, "Say": False}, # Channel #server-logs.
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

# Other Settings
INVITECODES = {
    "Nincord": "mYjeaZQ",
    "Puginator": "Yh2zWxugVE",
    "Resistance": "ab6P4gB",
}