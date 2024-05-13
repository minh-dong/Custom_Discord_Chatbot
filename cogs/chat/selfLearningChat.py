#
# A simple self learning chat bot that will respond to members' messages. If it is not know in the database, the
# bot will ask them to help the bot learn.
#


import discord
from discord.ext import commands
from chatbot import get_knowledge_base_filename, load_knowledge_base, save_knowledge_base, find_best_match, get_answer_for_questions
import os


class SelfLearningChat(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.filename = get_knowledge_base_filename()

        # If the file does not exist, let's create it for the first time
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write("{\n")
                file.write("  \"questions\": [\n")
                file.write("  ]\n")
                file.write("}\n")

    @commands.hybrid_command(name="chat",
                             brief="Chat with me!",
                             description="Chat with me!")
    async def chat(self,
                   ctx: discord.ext.commands,
                   *,
                   user_message: str,
                   store_message: str = None) -> None:
        # Get the knowledge base
        knowledge_base: dict = load_knowledge_base(self.filename)

        #print(ctx.message.content)
        #print(user_message)

        if store_message is None:
            # Get the answer for the msg
            best_match: str | None = find_best_match(user_message, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                answer: str = get_answer_for_questions(best_match, knowledge_base)
                await ctx.send(answer)
            else:
                await ctx.send("I don't know how to respond to you. Can you teach me by using the following command? " +
                               "/chat user_message:(your message) store_message:(how I should respond)")

        elif store_message is not None:
            knowledge_base["questions"].append({"question": user_message, "answer": store_message})
            save_knowledge_base(self.filename, knowledge_base)
            await ctx.send("Thank you for teaching me how to respond back in the future! Database updated! :)")


# To add the bot to the cogs list
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(SelfLearningChat(bot))
