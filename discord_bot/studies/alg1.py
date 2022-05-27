import time
import discord
from discord.ext import commands
import json
import random


class Alg1Bot(commands.Cog):
    """

    """

    alg1_id = 900731533491597343

    exercises_dir = "discord_bot/studies/db_exercises"

    exercise_tips = ""
    exercise_tip_number = 0
    exercise = ""
    exercise_init_message = None
    msg_to_erase = None

    to_do_exercise = False


    def __init__(self, bot):
        """
            __init__
        """

        self.bot = bot
        self.study_channel = None

    @commands.command()
    async def gen(self, context):
        challengeFile = ""
        
        await context.message.delete()
        m_channel = discord.utils.get(context.guild.channels, name="alg1")
        if context.channel.id == m_channel.id:
            if self.to_do_exercise:
                end = await context.send("Tem um exercício sendo feito ainda. Para fechá-lo, dê o comando:\n"+
                                    "`$ok`")
                time.sleep(3)
                await end.delete()
                return
            try:
                with open(f"{self.exercises_dir}/exercises.json", "r") as json_file:
                    challengeFile = json.load(json_file)
            except Exception as ex:
                #print("arquivo nao encontrado")
                return
            
            self.to_do_exercise = True
            self.exercise = random.choice(list(challengeFile.values()))

            embed = discord.Embed(
                title=f"Exercício {self.exercise['dificuldade']}\n{self.exercise['description']}",
                description=f"{self.exercise['exemplo']}\n\n"+
                            "`Para resolução passo a passo, dê o comando: $dica`"
            )

            self.exercise_init_message = await context.send(embed=embed)

    @commands.command()
    async def dica(self, context):
        
        await context.message.delete()
        m_channel = discord.utils.get(context.guild.channels, name="alg1")
        if context.channel.id == m_channel.id:
            try:
                self.exercise_tips += f"{self.exercise_tip_number + 1} - {self.exercise['dica'][self.exercise_tip_number]}\n"
            except Exception as ex:
                end = await context.send("As dicas acabaram ou nenhum exercício foi escolhido. :/")
                time.sleep(3)
                await end.delete()
                return
            else:
                description = f"{self.exercise_tips}\n"
                if self.exercise_tip_number + 1 < len(self.exercise['dica']):
                    description += "`Próxima dica: $dica`\n"
                self.exercise_tip_number += 1
                embed = discord.Embed(
                    title="Dica",
                    description=description
                )

                if self.msg_to_erase:
                    await self.msg_to_erase.delete()
                self.msg_to_erase = await context.send(embed=embed)

    @commands.command()
    async def ok(self, context):
        await context.message.delete()
        m_channel = discord.utils.get(context.guild.channels, name="alg1")
        if context.channel.id == m_channel.id:
            end = await context.send("Exercício em andamento finalizado. Apagando sessão passada...")
    
            self.exercise_tips = ""
            self.exercise_tip_number = 0
            self.exercise = ""

            if self.msg_to_erase:
                await self.msg_to_erase.delete()
                time.sleep(1)
            if self.exercise_init_message:
                await self.exercise_init_message.delete()
                time.sleep(1)

            self.msg_to_erase = None
            self.exercise_init_message = None
            self.to_do_exercise = False

            await end.delete()