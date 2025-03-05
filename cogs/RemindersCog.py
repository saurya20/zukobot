import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import re

class RemindersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}  # Store reminders as {(user_id, datetime): message}
        self.check_reminders.start()  # Start background task to check reminders

    def cog_unload(self):
        self.check_reminders.cancel()  # Stop background task when cog is unloaded

    @commands.command()
    async def remind(self, ctx, date: str, time: str, *, message: str):
        """Set a reminder: #remind YYYY-MM-DD HH:MM Your message"""
        try:
            # Validate date & time format
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', date) or not re.match(r'^\d{2}:\d{2}$', time):
                await ctx.send("❌ Invalid format! Use `YYYY-MM-DD HH:MM Your message`")
                return

            # Convert to datetime
            reminder_time = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
            now = datetime.datetime.now()

            if reminder_time <= now:
                await ctx.send("⚠️ You cannot set a reminder for the past!")
                return

            # Store reminder
            self.reminders[(ctx.author.id, reminder_time)] = message
            await ctx.send(f"✅ Reminder set for {date} {time}: {message}")

        except Exception as e:
            await ctx.send(f"❌ Error setting reminder: {str(e)}")

    @commands.command()
    async def listreminders(self, ctx):
        """List all active reminders"""
        user_reminders = [f"{dt}: {msg}" for (user, dt), msg in self.reminders.items() if user == ctx.author.id]

        if not user_reminders:
            await ctx.send("📌 You have no active reminders.")
        else:
            reminders_list = "\n".join(user_reminders)
            await ctx.send(f"📜 **Your Active Reminders:**\n{reminders_list}")

    @commands.command()
    async def deletereminder(self, ctx, date: str, time: str):
        """Delete a specific reminder: #deletereminder YYYY-MM-DD HH:MM"""
        try:
            reminder_time = datetime.datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")

            if (ctx.author.id, reminder_time) in self.reminders:
                del self.reminders[(ctx.author.id, reminder_time)]
                await ctx.send(f"🗑️ Reminder for {date} {time} deleted.")
            else:
                await ctx.send("⚠️ No such reminder found.")

        except Exception as e:
            await ctx.send(f"❌ Error deleting reminder: {str(e)}")

    @tasks.loop(seconds=60)
    async def check_reminders(self):
        """Background task to check and send reminders every 60 seconds"""
        now = datetime.datetime.now()
        to_delete = []

        for (user_id, reminder_time), message in self.reminders.items():
            if now >= reminder_time:
                user = self.bot.get_user(user_id)
                if user:
                    await user.send(f"🔔 Reminder: {message}")
                to_delete.append((user_id, reminder_time))

        # Remove expired reminders
        for key in to_delete:
            del self.reminders[key]

    @check_reminders.before_loop
    async def before_check_reminders(self):
        """Wait until the bot is ready before starting the loop"""
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(RemindersCog(bot))
