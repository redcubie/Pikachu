import discord
import configuration.variables as variables

STAFFROLES = {
    variables.SERVERBOT, # Role @Server Bot.
    variables.SERVEROWNER, # Role @Server Owner.
    variables.SERVERMODERATOR, # Role @Server Moderator.
}

LOCKDOWNCHANNELS = {
    variables.GENERALCHAT, # Channel #general-chat.
    variables.RANDOMCHAT, # Channel #random-chat.
    variables.BOTCOMMANDS, # Channel #bot-commands.
    variables.SMASHGENERAL, # Channel #smash-general.
    variables.SMASHBATTLES, # Channel #smash-battles.
    variables.POKEMONGENERAL, # Channel #pokémon-general.
    variables.POKEMONTRADES, # Channel #pokémon-trades.
    variables.POKEMONBATTLES, # Channel #pokémon-battles.
    variables.MARIOCHAT,  # Channel #mario-chat.
    variables.ZELDACHAT, # Channel #zelda-chat.
    variables.KIRBYCHAT, # Channel #kirby-chat.
    variables.FIREEMBLEMCHAT, # Channel #fire-emblem-chat.
    variables.ANIMALCROSSINGCHAT, # Channel #animal-crossing-chat.
    variables.SPLATOONCHAT # Channel #splatoon-chat.
}

LOCKDOWNCHANNELSV = {
    variables.GENERALCHATV, # Channel General Chat.
    variables.RANDOMCHATV, # Channel Random Chat.
    variables.BOTCOMMANDSV, # Channel Bot Commands.
    variables.SINGLESCHATV, # Channel Singles Chat.
    variables.DOUBLESCHATV, # Channel Doubles Chat.
    variables.ARENACHATV, # Channel Arena Chat.
    variables.TRADECHATV, # Channel Trade Chat.
    variables.BATTLECHATV, # Channel Battle Chat.
}

LOGCHANNELS = {
    variables.BOTLOGS, # Channel #bot-logs.
    variables.REQUESTLOGS, # Channel #request-logs.
    variables.ACTIONLOGS, # Channel #action-logs.
    variables.MESSAGELOGS, # Channel #message-logs.
    variables.SERVERLOGS, # Channel #server-logs.
}
