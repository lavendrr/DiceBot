import discord
from discord.ext import commands
from pandas import read_csv
import random
import typing

creds = read_csv('credentials.csv').set_index('key').transpose()
bot_token = creds['bot_token'].loc['value']

intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.message_content = True

#client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)

@bot.tree.command(name = 'hello')
async def hello(interaction):
    await interaction.response.send_message('hello!')

@bot.tree.command()
async def repeat(interaction, input: str):
    await interaction.response.send_message(f'you said: {input}')

@bot.tree.command()
async def roll(interaction, dice_amount: typing.Literal[4,6,8,10,12,20], dice_value: int, operation: typing.Literal['add', 'subtract', 'multiply', 'division']):
    #await interaction.response.defer()
    out = []
    die = 0
    while die < dice_amount:
        out.append(random.randint(1, dice_value))
        die += 1
    await interaction.response.send_message(content = str(out))

@bot.tree.command()
async def alchemy(interaction, die1: int, die2: int, die3: int = None, die4: int = None):
    dice_list = [die1, die2, die3, die4]
    while (None in dice_list):
        dice_list.remove(None)

    target_dict = {
        1: 'You or one ally you can see that is present on the scene',
        2: 'You or one ally you can see that is present on the scene',
        3: 'You or one ally you can see that is present on the scene',
        4: 'You or one ally you can see that is present on the scene',
        5: 'You or one ally you can see that is present on the scene',
        6: 'You or one ally you can see that is present on the scene',
        7: 'One enemy you can see that is present on the scene',
        8: 'One enemy you can see that is present on the scene',
        9: 'One enemy you can see that is present on the scene',
        10: 'One enemy you can see that is present on the scene',
        11: 'One enemy you can see that is present on the scene',
        12: 'You and every ally present on the scene',
        13: 'You and every ally present on the scene',
        14: 'You and every ally present on the scene',
        15: 'You and every ally present on the scene',
        16: 'You and every ally present on the scene',
        17: 'Every enemy present on the scene',
        18: 'Every enemy present on the scene',
        19: 'Every enemy present on the scene',
        20: 'Every enemy present on the scene'
        }
    effect_dict = {
        1: 'treats their Dexterity and Might dice as if they were one size higher (up to a maximum of d12) until the end of your next turn.',
        2: 'treats their Insight and Willpower dice as if they were one size higher (up to a maximum of d12) until the end of your next turn.',
        3: 'suffers 20 air damage.',
        4: 'suffers 20 bolt damage.',
        5: 'suffers 20 dark damage.',
        6: 'suffers 20 earth damage.',
        7: 'suffers 20 fire damage.',
        8: 'suffers 20 ice damage.',
        9: 'gains Resistance to air and fire damage until the end of the scene.',
        10: 'gains Resistance to bolt and ice damage until the end of the scene.',
        11: 'gains Resistance to dark and earth damage until the end of the scene.',
        12: 'suffers enraged.',
        13: 'suffers poisoned.',
        14: 'suffers dazed, shaken, slow, and weak.',
        15: 'recovers from all status effects.',
        16: 'recovers 50 Hit Points and 50 Mind Points.',
        17: 'recovers 50 Hit Points and 50 Mind Points.',
        18: 'recovers 100 Hit Points.',
        19: 'recovers 100 Mind Points.',
        20: 'recovers 100 Hit Points and 100 Mind Points.'
        }
    
    roll_combos = set()

    for target_die_idx in range(len(dice_list)):
        for effect_die_idx in range(len(dice_list)):
            if target_die_idx != effect_die_idx:
                roll_combos.add((dice_list[target_die_idx], dice_list[effect_die_idx]))

    potion_list = [f'**({t})** {target_dict[t]} **({e})** {effect_dict[e]}' for (t, e) in sorted(roll_combos, reverse = True)]
    output = '\n'.join(potion_list)

    await interaction.response.send_message(content = output)

@bot.command()
async def hello(ctx):
    await ctx.reply('hello')

@bot.command()
async def sync(ctx):
    await ctx.reply(str(await (bot.tree.sync())))

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    #print('Time: {}'.format(datetime.now(pytz.timezone('US/Central')).strftime('%H:%M:%S %Z on %b %d, %Y')))
    print('------')

bot.run(bot_token)