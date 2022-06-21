import time
import discord
from discord.ext import commands
import json
import random
import re

import psycopg2
from database import database as db

class ProfsBot(commands.Cog):
    profs_id = 988887833689337856


    def __init__(self, bot):
        """
            __init__
        """

        self.bot = bot

        #cria o banco de dados.
        self.database = db.Database()
        self.database.connect()
        self.database.create_table()

        self.all_profs = {
            "Aldri Luiz dos Santos": "aldri@inf.ufpr.br ",
            "Andre Luis Vignatti": "vignatti@inf.ufpr.br",
            "Andre Luiz Pires Guedes": "andre@inf.ufpr.br",
            "Andre Ricardo Abed Gregio": "gregio@inf.ufpr.br",
            "Andrey Ricardo Pimentel": "andrey@inf.ufpr.br",
            "Antonio Edison Urban": "urban@inf.ufpr.br",
            "Armando Luiz Nicolini Delgado": "nicolui@inf.ufpr.br",
            "Aurora Trinidad Ramirez Pozo": "aurora@inf.ufpr.br",
            "Bruno Muller Junior": "bmuller@inf.ufpr.br",
            "Carlos Alberto Maziero": "maziero@inf.ufpr.br",
            "Carmem Satie Hara": "carmem@inf.ufpr.br",
            "Daniel Alfonso Gonçalves de Oliveira": "dagoliveira@inf.ufpr.br",
            "Davi Menotti Gomes": "menotti@inf.ufpr.br",
            "Eduardo Cunha de Almeida": "eduardo@inf.ufpr.br",
            "Eduardo Jaques Spinosa": "spinosa@inf.ufpr.br",
            "Eduardo Todt": "todt@inf.ufpr.br",
            "Elenice Mara Matos Novak": "elenice@inf.ufpr.br",
            "Elias Procopio Duarte Junior": "elias@inf.ufpr.br",
            "Fabiano Silva": "fabiano@inf.ufpr.br",
            "Guilherme Alex Derenievicz": "guilherme@inf.ufpr.br",
            "Leticia Mata Peres": "lmperes@inf.ufpr.br", 
            "Lucas Ferrari de Oliveira": "lferrari@inf.ufpr.br",
            "Luciano Silva": "luciano@inf.ufpr.br",
            "Luis Allan Kunzle": "kunzle@inf.ufpr.br",
            "Luis Carlos Erpen de Bona": "bona@inf.ufpr.br",
            "Luiz Carlos Pessoa Albini": "albini@inf.ufpr.br",
            "Luiz Eduardo Soares de Oliveira": "lesoliveira@inf.ufpr.br",
            "Marco Antonio Zanata Alves": "mazalves@inf.ufpr.br",
            "Marcos Alexandre Castilho": "marcos@inf.ufpr.br",
            "Marcos Didonet Del Fabro": "didonet@inf.ufpr.br",
            "Marcos Sfair Sunye": "sunye@inf.ufpr.br",
            "Michele Nogueira Lima": "michele@inf.ufpr.br",
            "Murilo Vicente Gonçalves da Silva": "murilo@inf.ufpr.br",
            "Natasha Malveira Costa Valentim": "natasha@inf.ufpr.br",
            "Olga Regina Pereira Bellon": "olga@inf.ufpr.br",
            "Paulo Eliseu Portella": "portella@inf.ufpr.br",
            "Paulo Ricardo Lisboa de Almeida": "paulo@inf.ufpr.br",
            "Renato Carmo": "renato@inf.ufpr.br",
            "Roberto Andre Hexsel": "roberto@inf.ufpr.br",
            "Roberto Pereira": "rpereira@inf.ufpr.br",
            "Silvia Regina Vergilio": "silvia@inf.ufpr.br",
            "Wagner Machado Nunan Zola": "wagner@inf.ufpr.br"
        }

        for name, email in self.all_profs.items():
            self.database.commit_query(
                "INSERT INTO PROFS (NAME, EMAIL, STARS, VOTES, COMMENTS) VALUES \
                    ('{}', '{}', '{}', '{}', {})".format(name, email, 0, 0, psycopg2.extras.Json({}))
            )

    @commands.command()
    async def add(self, context, *args):
        #TODO: arrumar email
        pass
        # self.database.commit_query(
        #     "INSERT INTO PROFS (NAME, STARS, VOTES, COMMENTS) VALUES \
        #         ('{}', '{}', '{}', {})".format(' '.join(args), 0, 0, psycopg2.extras.Json({}))
        # )

    @commands.command()
    async def prof(self, context, *args):
        database_info = self.database.select_rows_dict_cursor(
            "SELECT * FROM PROFS", True)

        profs = []
        for a in database_info:
            if re.search(' '.join(args), str(a[1]), re.IGNORECASE):
                profs.append(a)

        message = None
        if len(profs) == 0:
            message = f"Nenhum professor encontrado com essa busca\n"
        elif len(profs) > 1:
            message = f"Temos {len(profs)} professores com essa busca:\n```"
            for name in profs:
                message += f"{name[1]}\n"
            message += "```\n"
            message += f"Faça a busca com o nome completo.\n"

        if message:
            await context.send(message)
            return

        prof = profs[0]
        embed = discord.Embed(
            title=f"{prof[1]} (ID: {prof[0]})",
            description=prof[2],
            colour=context.author.colour,
        )

        stars = 0.0
        if prof[4] != 0:
            stars = prof[3]/prof[4]
        
        embed.add_field(
            name=f"Votos",
            value=f"🗳️: {prof[4]}\n⭐: {stars}/5",
            inline=False
        )
        
        size = 9
        if len(prof[5]) < 9:
            size = len(prof[5])
        r = [random.choice(list(prof[5])) for i in range(size)]
        for i in r:
            embed.add_field(
                name=prof[5][i],
                value=i,
                inline=True
            )

        await context.send(embed=embed)


    @commands.command()
    async def op(self, context, *args):
        if not isinstance(context.channel, discord.channel.DMChannel):
            await context.send(
                "Opiniões só podem ser mandadas via mensagem privada pra mim.\n"
            )
            return

        if len(args) < 4:
            await context.send(
                "Comando inválido. Deve ser no formato: $op <ID prof> <codigo da materia> <opiniao (limite 200 caracteres)>\n"+
                "`ID prof` é o numero que aparece ao buscar o professor no comando `prof`.\n"
            )
            return

        args = list(args)
        key = args[0]
        materia = args[1]
        
        args.pop(0)
        args.pop(0)
        opiniao = ' '.join(args)

        comments = self.database.select_rows_dict_cursor(
            "SELECT COMMENTS FROM PROFS WHERE KEY = '{}'".format(key), True)
        
        update_op = {}
        for c in comments[0]:
            for o, m in c.items():
                update_op[o] = m

        update_op[opiniao] = materia

        self.database.commit_query(
            "UPDATE PROFS SET COMMENTS = {} WHERE KEY = '{}'".format(
                psycopg2.extras.Json(update_op), key)
        )

    @commands.command()
    async def vote(self, context, *args):
        if not isinstance(context.channel, discord.channel.DMChannel):
            await context.send(
                "Votos só podem ser mandados via mensagem privada pra mim.\n"
            )
            return

        if len(args) != 2:
            await context.send(
                "Comando inválido.\n"
            )
            return

        if int(args[1]) < 0 or int(args[1]) > 5:
            await context.send(
                "Pontuação deve estar entre 0 e 5.\n"
            )
            return


        database_info = self.database.select_rows_dict_cursor(
            "SELECT STARS, VOTES FROM PROFS WHERE KEY = '{}'".format(args[0]), True)

        stars = int(args[1]) + int(database_info[0][0])
        votes = int(database_info[0][1]) + 1

        self.database.commit_query(
            "UPDATE PROFS SET STARS = '{}' WHERE KEY = '{}'".format(stars, args[0])
        )
        self.database.commit_query(
            "UPDATE PROFS SET VOTES = '{}' WHERE KEY = '{}'".format(votes, args[0])
        )

        await context.send(
            "Voto feito :)\n"
        )