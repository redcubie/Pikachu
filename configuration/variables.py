import discord, os

# General Configuration
STATUSTYPE = discord.ActivityType.watching # The current action type that appears by default.
STATUSACTIVITY = "Nincord" + " (p!)" # The current action activity that appears by default.

# Role Definitions
SERVERBOT = 450886915340763151 # The ID of the @Server Bot role.
SERVEROWNER = 450886695760691220 # The ID of the @Server Owner role.
SERVERMODERATOR = 450903750648004608 # The ID of the @Server Moderator role.
SERVERAFFILIATE = 473862508415811585 # The ID of the @Server Affiliate role.
SERVERBOOSTER = 616335384791482389 # The ID of the @Server Booster role.
BOTCONTRIBUTOR = 743198831000158218 # The ID of the @Bot Contributor role.
CONTENTCREATOR = 664603430853148706 # The ID of the @Content Creator role.
TRUSTEDMEMBER = 665364949765324800 # The ID of the @Trusted Member role.
PROJECTDEVELOPER = 711046740400406570 # The ID of the @Project Developer role.
NINTENDOCOLLECTOR = 757769140529528922 # The ID of the @Nintendo Collector role.

# Channel Definitions
SERVERRULES = 450903022613168129 # The ID of the #rules channel.
SERVERAFFILIATES = 500342143039176725 # The ID of the #affiliates channel.
ANNOUNCEMENTS = 738920609630912604 # The ID of the #announcements channel.
EVERYBODYVOTES = 450903547911864321 # The ID of the #everybody-votes channel.
GENERALCHAT = 469302882974433290 # The ID of the #general-chat text channel.
RANDOMCHAT = 450875176486305792 # The ID of the #random-chat text channel.
TRUSTEDCHAT = 742819077009047666 # The ID of the #trusted-chat channel.
MODERATORCHAT = 478388911350087709 # The ID of the #moderator-chat text channel.
GENERALCHATV = 453355810794242059 # The ID of the General Chat voice channel.
RANDOMCHATV = 450910610251710465 # The ID of the Random Channel voice channel.
TRUSTEDCHATV = 743275160790106261 # The ID of the Trusted Chat voice channel.
MODERATORCHATV = 482916026674053120 # The ID of the Moderator Chat voice channel.
BOTCOMMANDS = 707036038295584889 # The ID of the #bot-commands text channel.
BOTDISCUSSION = 725061309237952632 # The ID of the #bot-discussion channel.
BOTTESTING = 770115158713303110 # The ID of the #bot-testing channel.
SMASHGENERAL = 552296826376814592 # The ID of the #smash-general channel.
SMASHBATTLES = 649017775825616902 # The ID of the #smash-battles channel.
SINGLESCHATV = 649018265544294430 # The ID of the Singles Chat voice channel.
DOUBLESCHATV = 649018154382786590 # The ID of the Doubles Chat voice channel.
ARENACHATV = 649018569698443265 # The ID of the Arena Chat voice channel.
POKEMONGENERAL = 549359240876130314 # The ID of the #pokémon-general channel.
POKEMONTRADES = 649017960773582882 # The ID of the #pokémon-trades channel.
POKEMONBATTLES = 649017998195032084 # The ID of the #pokémon-battles channel.
TRADECHATV = 649018461623812150 # The ID of the Trade Chat voice channel.
BATTLECHATV = 649018657741078555 # The ID of the Battle Chat voice channel.
DIRECTCHAT = 734148916559478845 # The ID of the #direct-chat text channel.
TOURNAMENTCHAT = 649020355310125067 # The ID of the #tournament-chat text channel.
DIRECTCHATV = 551841037363052546 # The ID of the Direct Chat voice channel.
TOURNAMENTCHATV = 551841124608901150 # The ID of the Tournament Chat voice channel.
BOTLOGS = 725045178720583756 # The ID of the #bot-logs channel.
REQUESTLOGS = 707106126902198302 # The ID of the #request-logs channel.
ACTIONLOGS = 701634899937067018 # The ID of the #action-logs channel.
MESSAGELOGS = 701635047115063376 # The ID of the #message-logs channel.
SERVERLOGS = 701634953410248775 # The ID of the #server-logs channel.

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