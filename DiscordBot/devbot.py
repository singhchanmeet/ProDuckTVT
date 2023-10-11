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

import re

# ...
@bot.command()
async def schedule_task(ctx, time, *, task_description):
    """Schedule a task for a user to be notified about."""
    try:
        # Use regular expressions to extract the numeric part as the time duration
        match = re.match(r'(\d+)\s*(?:minutes|mins)?', time, re.IGNORECASE)
        if match:
            minutes = int(match.group(1))
        
            # Remove the time and related text from the task_description
            task_description = task_description.replace('minutes', '').strip()
            task_description = task_description.replace('mins', '').strip()

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
        
            if ctx.author.id in user_tasks:
                if ctx.guild:
                    server = ctx.guild
                    text_channel = server.text_channels[0]
                    await text_channel.send(f"{ctx.author.mention}, Did you complete the task: '{task_description}'? (yes/no)")
                else:
                    # print(ctx.author)
                    await ctx.author.send(f"Did you complete the task: '{task_description}'? (yes/no)")
                
                def check(response):
                    # server = ctx.guild
                    # text_channel = server.text_channels[0]
                    return response.author == ctx.author and response.channel == text_channel
                    
                try:
                    # server = ctx.guild
                    # text_channel = server.text_channels[0]
                    response = await bot.wait_for('message',  timeout=300)  # Pass text_channel as an argument
                    response_content = response.content.strip().lower()
                    
                    if response_content == 'yes':
                        if ctx.guild:
                            await text_channel.send("Great!")
                        else:
                            await ctx.author.send("Great!")
                        del user_tasks[ctx.author.id]
                    elif response_content == 'no':
                        if ctx.guild:
                            await text_channel.send("Please provide a new time to complete the task (e.g., '30 minutes').")
                        else:
                            await ctx.author.send("Please provide a new time to complete the task (e.g., '30 minutes').")
                        new_time_response = await bot.wait_for('message', timeout=300)  # Pass text_channel as an argument
                        new_time = new_time_response.content.strip()
                        
                        # Update the task with the new time
                        match = re.match(r'(\d+)\s*(?:minutes|mins)?', new_time, re.IGNORECASE)
                        if match:
                            if ctx.guild:
                                new_minutes = int(match.group(1))
                                user_tasks[ctx.author.id]['notification_time'] = notification_time + datetime.timedelta(minutes=new_minutes)
                                await text_channel.send(f"Task rescheduled to {new_time}.")
                            else:
                                await ctx.author.send(f"Task rescheduled to {new_time}.")
                        else:
                            if ctx.guild:
                                await text_channel.send("Invalid time format. Task not rescheduled.")
                            else:
                                await ctx.author.send("Invalid time format. Task not rescheduled.")
                except asyncio.TimeoutError:
                    text_channel = server.text_channels[0]
                    await text_channel.send("No response received. Task not rescheduled.")
        else:
            await ctx.send("Invalid time format. Please use 'X minutes' or 'X mins' followed by the task description.")
    except ValueError:
        await ctx.send("Invalid time format. Please use 'X minutes' or 'X mins' followed by the task description.")

@bot.command()
async def set_status(ctx, activity):
    """Set the user's current activity."""
    valid_activities = ['coding', 'gaming', 'other']
    
    if activity.lower() not in valid_activities:
        await ctx.send("Invalid activity. Please choose from 'coding', 'gaming', or 'other'.")
        return
    
    user_id = ctx.author.id
    
    if user_id in user_tasks:
        current_activity = user_tasks[user_id]['activity']
        start_time = user_tasks[user_id]['start_time']
        
        if current_activity in ['coding', 'gaming']:
            elapsed_time = datetime.datetime.now() - start_time
            if ctx.guild:
                # Command was invoked in a server, send the message to the server's text channel
                server = ctx.guild
                text_channel = server.text_channels[0]  # You can customize this to send to a specific channel
                await text_channel.send(f"{ctx.author.mention}, You did {current_activity} for {str(elapsed_time)[0]} hours {str(elapsed_time)[2:4]} minutes and {str(elapsed_time)[5:7]} seconds.")
            else:
                # Command was invoked in a personal chat, send the message as a direct message
                await ctx.author.send(f"You did {current_activity} for {str(elapsed_time)[0]} hours {str(elapsed_time)[2:4]} minutes and {str(elapsed_time)[5:7]} seconds.")
    
    user_tasks[user_id] = {
        'activity': activity.lower(),
        'start_time': datetime.datetime.now()
    }
    
    await ctx.send(f"You are now doing '{activity}'.")
    
    if activity.lower() in ['coding', 'gaming']:
        # await asyncio.sleep(7200)  # Wait for 2 hours
        await asyncio.sleep(10)  # Wait for 2 hours
        
        if user_id in user_tasks and user_tasks[user_id]['activity'] == activity.lower():
            end_time = datetime.datetime.now()
            elapsed_time = end_time - user_tasks[user_id]['start_time']
            
            if ctx.guild:
                # Command was invoked in a server, send the notification to the server's text channel
                server = ctx.guild
                text_channel = server.text_channels[0]  # You can customize this to send to a specific channel
                await text_channel.send(f"{ctx.author.mention}, You have been {activity} for {str(elapsed_time)[0]} hours {str(elapsed_time)[2:4]} minutes and {str(elapsed_time)[5:7]} seconds. You should take a rest now.")
            else:
                # Command was invoked in a personal chat, send the notification as a direct message
                await ctx.author.send(f"You have been {activity} for {str(elapsed_time)[0]} hours {str(elapsed_time)[2:4]} minutes and {str(elapsed_time)[5:7]} seconds. You should take a rest now.")


# @bot.command()
# async def list_activities(ctx):
#     """List the user's Discord activities."""
#     user = ctx.author
#     print(user)
#     activities = user.activities
#     print(activities)

#     if activities:
#         game_activities = [activity.name for activity in activities if isinstance(activity, discord.Game)]
#         if game_activities:
#             await ctx.send(f"{user.mention} is currently playing: {', '.join(game_activities)}")
#         else:
#             await ctx.send(f"{user.mention} is not currently playing any games.")
#     else:
#         await ctx.send(f"{user.mention} is not currently engaged in any activities.")

# @bot.command()
# async def list_activities(ctx):
#     """List the user's Discord activities."""
#     user = ctx.author
#     member = ctx.guild.get_member(user.id)  # Get the Member object
#     print(user)
    
#     if member is not None:
#         activities = member.activities
        
#         if activities:
#             game_activities = [activity.name for activity in activities if isinstance(activity, discord.Game)]
#             if game_activities:
#                 await ctx.send(f"{user.mention} is currently playing: {', '.join(game_activities)}")
#             else:
#                 await ctx.send(f"{user.mention} is not currently playing any games.")
#         else:
#             await ctx.send(f"{user.mention} is not currently engaged in any activities.")
#     else:
#         await ctx.send("You must use this command in a server where the bot is a member to retrieve activity information.")




# Run the bot with your token
bot.run('MTE1OTA0MDUxNTQyNjIyNjE4Nw.G9v_Xr.jLTR4gwqHP8fDN2oh8TRqquy-6r6kv8XHEYeK0')
