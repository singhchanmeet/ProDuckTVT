import discord
from discord.ext import commands
import asyncio
import datetime

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dictionary to store user tasks and their respective notification times
user_tasks = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

@bot.command()
async def hello(ctx):
    """Responds with a greeting."""
    print(ctx.author)
    await ctx.send(f'Hello, {ctx.author.mention}!')

@bot.command()
async def say(ctx, *, message):
    """Repeats a given message."""
    await ctx.send(message)

@bot.command()
async def calculate(ctx, *, expression):
    """Calculates a mathematical expression."""
    try:
        result = eval(expression)
        await ctx.send(f'Result: {result}')
    except Exception as e:
        await ctx.send(f'Error: {str(e)}')

@bot.command()
async def schedule_task(ctx, time, *, task_description):
    """Schedule a task for a user to be notified about."""
    try:
        # Split the command input to separate the time duration and task description
        time_parts = time.split()
        if len(time_parts) >= 2:
            # Extract the minutes and task description
            minutes = int(time_parts[0])
            task_description = ' '.join(time_parts[1:]) + ' ' + task_description
        
            # Calculate the time to notify the user
            notification_time = ctx.message.created_at + datetime.timedelta(minutes=minutes)
        
            # Store the task and notification time in the dictionary
            user_tasks[ctx.author.id] = {
                'task_description': task_description,
                'notification_time': notification_time
            }
        
            await ctx.send(f'Task scheduled: {task_description} in {minutes} minutes.')
        
            # Wait for the specified time and then notify the user
            await asyncio.sleep(minutes)
            # await asyncio.sleep(minutes * 60)
        
            if ctx.author.id in user_tasks:
                # Check if the command was invoked in a server or a personal chat
                if ctx.guild:
                    # Command was invoked in a server, send the notification to the server's text channel
                    server = ctx.guild
                    text_channel = server.text_channels[0]  # You can customize this to send to a specific channel
                    await text_channel.send(f"{ctx.author.mention}, Did you complete the task: '{task_description}'?")
                else:
                    # Command was invoked in a personal chat, send the notification as a direct message
                    await ctx.author.send(f"Did you complete the task: '{task_description}'?")
                
                del user_tasks[ctx.author.id]  # Remove the task from the dictionary after notification
        else:
            await ctx.send("Invalid time format. Please use 'X minutes' or 'X mins' followed by the task description.")
    except ValueError:
        await ctx.send("Invalid time format. Please use 'X minutes' or 'X mins' followed by the task description.")



# Run the bot with your token
bot.run('MTE1OTA0MDUxNTQyNjIyNjE4Nw.Gun2Pz.v4uh0NzZYgH9HMwyu0Bgyzi66ay-0f5p0EYQIU')
