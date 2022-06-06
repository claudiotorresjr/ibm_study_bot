import os
import discord
from discord.ext import commands
import asyncio

import studies


class StudyBot(studies.Common):
    """

    """

    material_dir = "discord_bot/studies/materiais"

    save_info_for_dms = {}
    periodos = {}
    disciplinas_periodos = {}
    disciplinas = {}

    materiais_id = 983389296423764008 #891015271551225886
    perguntas_id = 891355416167088158 #891015309153153055

    def __init__(self, bot):
        """
            __init__
        """

        self.bot = bot
        self.study_channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        """
            É ativada sempre que alguma mensagem é enviada no servidor

            param message: mensagem enviada
        """

        #self.get_all_materials_location()

    def get_materials_location(self, p_dir):
        all_lines = ""
        try:
            with open(f"{self.material_dir}/{p_dir}/disciplinas", "r") as file:
                all_lines = file.readlines()
        except Exception as ex:
            print(f"Arquivo disciplinas nao encontrado no periodo pedido. ", ex)
            return
    
        aux_d = {}
        disciplinas_periodos = {}
        for line in all_lines:
            print(line.split(',', 1))
            code, name = line.split(',', 1)
            name = name.replace('\n', '')

            have_d = False
            #se tem o diretorio da disciplina
            try:
                if os.path.isdir(f"{self.material_dir}/{p_dir}/{code}"):
                    have_d = True
            except Exception as ex:
                print(f"Não existe a disciplina no periodo. ", ex)

            self.disciplinas[code] = [name, have_d, p_dir]

            aux_d[code] = [name, have_d]

        disciplinas_periodos[p_dir] = aux_d
            
        return aux_d

    @commands.Cog.listener()
    async def on_message(self, message):
        """
            É ativada sempre que alguma mensagem é enviada no servidor (ou enviada diretamente pro bot)
            Mas só irá funcionar na DM do bot.

            param message: mensagem enviada
        """
        if message.author.bot:
            return

        message_content = message.content
        if isinstance(message.channel, discord.channel.DMChannel) and not message_content.startswith('$'):
            channel_id = self.perguntas_id

            code = False
            description = message_content
            if "<code>" in message_content and "</code>" in message_content:
                before_code = message_content.split("<code>")[0]
                after_code = message_content.split("<code>")[1][1:].split("</code>")[0]

                description = before_code
                value = f"```cpp\n{after_code}```"

                code = True

            embed = discord.Embed(
                title="Pergunta dum migo",
                description=f"```{description}```",
            )

            if code:
                embed.add_field(name="Código", value=value, inline=False)
        
            try:
                await self.bot.get_channel(channel_id).send(embed=embed)
            except Exception as ex:
                pass
            #await self.bot.get_channel(channel_id).send(question)
            #await context.message.author.send("Pronto, sua pergunta foi feita no canal <perguntas>")

    @commands.command()
    async def dm(self, context):
        """
            
        """

        channel = await self.is_in_right_channel(context, True)
        if channel:
            author_name = context.author
            self.save_info_for_dms[author_name] = channel.id
            
            embed = discord.Embed(
                title="Essa é uma mensagem privada :3",
                description="Aceito qualquer comando aqui. O que não começar com o prefixo de comandos, será entendido como uma pergunta."
            )
        
            await context.message.author.send(embed=embed)

    @commands.command()
    async def m(self, context):
        """
            
        """

        if await self.is_in_right_channel(context):
            number_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣"]

            periodos = []
            for i, dir in enumerate(os.listdir(f"{self.material_dir}")):
                periodos.append(dir)

            description = "Reaja ao emoji do período para ver as disciplinas\n\n"

            periodos = sorted(periodos)
            for i, dir in enumerate(sorted(periodos)):
                description += f"{number_emojis[i]} - {dir.replace('_', 'º')}\n\n"
            
            embed = discord.Embed(
                title="Períodos",
                description=description
            )

            sent_message = await context.send(embed=embed)
            total_p = len(periodos)

            for i in range(total_p):
                await sent_message.add_reaction(number_emojis[i])

            #remove os emojis nao utilizados da lista
            used_emojis = number_emojis[0:total_p]

            args = [context, number_emojis, used_emojis, sent_message, periodos]
            asyncio.get_event_loop().create_task(self.wait_periodo_reaction(args))

    async def wait_periodo_reaction(self, args):
        context = args[0]
        number_emojis = args[1]
        used_emojis = args[2]
        sent_message = args[3]
        periodos = args[4]

        def check(reaction, user):
            """
                Ter a certeza de que somente as reações do usuário que chamou o comando serão processadas

                param reaction: reação dada na mensagem
                param user: usuário que reagiu
            """

            return (user == context.author and str(reaction.emoji) in number_emojis)


        while True:
            try:
                #espera por 20 segundos (timeout) até receber alguma reação. apaga a mensagem se nao houver
                reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=check)

                if str(reaction.emoji) in used_emojis:
                    #o indice do emoji escolhido é indice do vetor de periodos
                    p_index = used_emojis.index(str(reaction.emoji))

                    disciplinas_periodos = self.get_materials_location(periodos[p_index])
                    value = ""
                    all_codes = []
                    i = 1
                    for c, d in disciplinas_periodos.items():
                        color = "diff\n- "
                        if d[1]:
                            #só salva os codigos q existem
                            all_codes.append([c, d[0]])
                            color = "diff\n+ "
                        value += f"```{color}{i}: ({c}) {d[0]}\n```"

                        i += 1

                    message = f"{value}\n"

                    embed = discord.Embed(
                        title="Reaja ao emoji da disciplina para ver os temas",
                        description="Reaja ao emoji da disciplina para ver os temas.\n"+
                                    "Para uma experiência mais prática, vá ao canal da disciplina, "+
                                    "e dê o comando:\n`help`\n para saber o que pode ser feito por lá :D\n"+
                                    "(Por enquanto temos só para Alg1)"
                    )
                    embed.add_field(name="Disciplinas", value=value, inline=False)

                    message = await context.send(embed=embed)
                    await sent_message.delete()
                    for j in range(len(all_codes)):
                        await message.add_reaction(number_emojis[j])

                    used_emojis = number_emojis[0:i-1]
                    sent_message = message

                    args = [context, number_emojis, used_emojis, sent_message, p_index, periodos[p_index], all_codes]
                    asyncio.get_event_loop().create_task(self.wait_disciplina_reaction(args))
                    break
                else:
                    #remove reação se estiver na ultima/primeira posicao e a pessoa tentar forçar
                    await sent_message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                try:
                    await message.delete()
                except Exception:
                    pass
                #acaba com o loop após o timeout
                break

    async def wait_disciplina_reaction(self, args):
        context = args[0]
        number_emojis = args[1]
        used_emojis = args[2]
        sent_message = args[3]
        p_index = args[4]
        periodo = args[5]
        all_codes = args[6]

        def check(reaction, user):
            """
                Ter a certeza de que somente as reações do usuário que chamou o comando serão processadas

                param reaction: reação dada na mensagem
                param user: usuário que reagiu
            """

            return (user == context.author and str(reaction.emoji) in number_emojis)


        while True:
            try:
                #espera por 20 segundos (timeout) até receber alguma reação. apaga a mensagem se nao houver
                reaction, user = await self.bot.wait_for("reaction_add", timeout=20, check=check)

                if str(reaction.emoji) in used_emojis:
                    #o indice do emoji escolhido é indice do vetor de periodos
                    code_index = used_emojis.index(str(reaction.emoji))
                    print(all_codes[code_index])
                    embed = discord.Embed(
                        title=f"Temas para {all_codes[code_index][1]}",
                        description="Para acessar o tema, complete  o comando a seguir:\n"+
                        f"***$t {p_index+1} {all_codes[code_index][0]} <identificador do tema>***\n"+
                        f"Exemplo para material de identificador 1: ***$t {p_index+1} {all_codes[code_index][0]} 1***"
                    )

                    #temas_disciplina = self.get_materials_location(periodos[p_index])
                    for i, dir in enumerate(os.listdir(f"{self.material_dir}/{periodo}/{all_codes[code_index][0]}")):
                        theme_files = f"```{i+1} - {dir}```"
                        embed.add_field(name=f"\u200b", value=theme_files, inline=True)                    

                    #await sent_message.delete()
                    message = await context.send(embed=embed)
                    await sent_message.delete()
                    break
                else:
                    #remove reação se estiver na ultima/primeira posicao e a pessoa tentar forçar
                    await sent_message.remove_reaction(reaction, user)

            except asyncio.TimeoutError:
                try:
                    await message.delete()
                except Exception:
                    pass
                #acaba com o loop após o timeout
                break

    @commands.command()
    async def t(self, context, *args):
        """
            
        """

        if await self.is_in_right_channel(context):
            if len(args) != 3:
                await context.send(
                    "Comando inválido. Uso: **$t <periodo> <código disciplina> <identificador do tema>**\n"+
                    "Caso haja alguma dúvida, execute o comando **$m** e siga as orientações."
                )
                return

            periodo = f"{args[0]}_periodo"
            code = args[1]
            theme = args[2]
            
            lines = ""
            theme_found = ""

            error_message = "Desculpa, tive problemas ao encontrar o material pedido. "+ \
                "Você pode ter digitado algo errado. Para ter certeza dos materiais disponíveis, "+ \
                "execute o comando **$m** e siga as orientações."

            try:
                for i, tf in enumerate(os.listdir(f"{self.material_dir}/{periodo}/{code}")):
                    if i+1 != int(theme):
                        continue
                    try:
                        with open(f"{self.material_dir}/{periodo}/{code}/{tf}", "r") as file:
                            lines = file.readlines()
                            theme_found = tf
                            break

                    except Exception as ex:
                            print(ex)
                            await context.send(error_message)
                            return
            except Exception as ex:
                    #print(ex)
                    await context.send(error_message)
                    return


            if lines == "":
                await context.send(error_message)
                return

            embed = discord.Embed(
                title=f"Materiais sobre {theme_found} disponíveis",
                description="Bons estudos :D"
            )
            for l in range(0, len(lines)-1, 2):
                embed.add_field(name=f"{lines[l]}", value=f"{lines[l+1]}", inline=False)

            await context.send(embed=embed)