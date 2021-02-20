import discord, os

# General Configuration
STATUSTYPE = discord.ActivityType.watching # The current action type that appears by default.
STATUSACTIVITY = "Nincord" # The current action activity that appears by default.

# Role Definitions
SERVERBOT = 450886915340763151 # The ID of the @Server Bot role.
SERVEROWNER = 450886695760691220 # The ID of the @Server Owner role.
SERVERMODERATOR = 450903750648004608 # The ID of the @Server Moderator role.
SERVERAFFILIATE = 473862508415811585 # The ID of the @Server Affiliate role.
SERVERBOOSTER = 616335384791482389 # The ID of the @Server Booster role.
BOTCONTRIBUTOR = 743198831000158218 # The ID of the @Bot Contributor role.
CONTENTCREATOR = 664603430853148706 # The ID of the @Content Creator role.
TRUSTEDMEMBER = 665364949765324800 # The ID of the @Trusted Member role.
GAMENIGHTPLAYER = 782122240547618866 # The ID of the @Game Night Player role.

# Channel Definitions
SERVERRULES = 450903022613168129 # The ID of the #server-rules channel.
ANNOUNCEMENTS = 738920609630912604 # The ID of the #announcements channel.
EVERYBODYVOTES = 450903547911864321 # The ID of the #everybody-votes channel.
GENERALCHAT = 469302882974433290 # The ID of the #general-chat text channel.
RANDOMCHAT = 450875176486305792 # The ID of the #random-chat text channel.
TRUSTEDCHAT = 742819077009047666 # The ID of the #trusted-chat channel.
MODERATORCHAT = 478388911350087709 # The ID of the #moderator-chat text channel.
NOMICROPHONE = 767236139525472306 # The ID of the #no-microphone channel.
BOTCOMMANDS = 707036038295584889 # The ID of the #bot-commands text channel.
DIRECTCHAT = 734148916559478845 # The ID of the #direct-chat text channel.
EVENTCHAT = 649020355310125067 # The ID of the #event-chat text channel.
GITHUBLOGS = 725045178720583756 # The ID of the #github-logs channel.
REQUESTLOGS = 707106126902198302 # The ID of the #request-logs channel.
ACTIONLOGS = 772214347363516418 # The ID of the #action-logs channel.
SERVERLOGS = 772229127138443264 # The ID of the #server-logs channel.

# Essential Configuration
if os.path.exists("configuration/secrets.py"):
    import configuration.secrets as secrets
    DBACCOUNT = secrets.DBACCOUNT # The key URL for the database account.
    BOTTOKEN = secrets.BOTTOKEN # The Discord bot authorization token.
    MONGODBURI = secrets.MONGODBURI # The URI for the bot's database.
else:
    DBACCOUNT = os.environ["DATABASE_ACCOUNT"] # The key URL for the database account.
    BOTTOKEN = os.environ["BOT_TOKEN"] # The Discord bot authorization token.
    MONGODBURI = os.environ["MONGODB_URI"] # The URI for the bot's database.
    HEROKUCOMMIT = os.environ["HEROKU_SLUG_COMMIT"] # The commit ID provided by Heroku.