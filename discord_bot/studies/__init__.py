import discord
from discord.ext import commands


class Common(commands.Cog):
    """

    """

    async def is_in_right_channel(self, context, dm=False):
        try:
            m_channel = discord.utils.get(context.guild.channels, name="materiais")
            if context.channel.id == m_channel.id:
                q_channel = discord.utils.get(context.guild.channels, name="perguntas")
                if dm:
                    return q_channel
                return True
            else:
                await context.send("Eu só converso pelo canal <materiais>. Da uma passada lá ;)")
                return False
        except Exception as ex:
            #dm??
            return True

    @commands.command()
    async def help(self, context):
        """
            
        """

        where_to_help = context.channel.name

        embed = discord.Embed(
            title="Como usar o bot",
            description="Comandos funcionando (espero) no momento",
            colour=context.author.colour,
        )

        embed.add_field(
            name="Mandar mensagem privada pra mim",
            value="```Toda mensagem que você enviar via dm pra mim, será redirecionada ao canal perguntas "+
            "como uma pergunta de autoria minha. Será totalmente anônima.\n"+
            "Portanto use com cuidado. Vai falar mal do coleguinha não.\n"+
            "Se quiser mandar algum código, basta adicioná-lo entre a tag <code>seu código aqui</code> para uma melhor visualização.\n"+
            "Importante: O código precisa ser a última coisa da mensagem. Tudo após a tag </code> não será processado.\n"+
            "Exemplo: (Funciona melhor com Pascal e C)\n"+
            "---INÍCIO DA MENSAGEM---\n\n"+
            "Pq será q isso não funciona??\n\n"+
            "<code>\n"+
            "#include <stdio.h>\n"+
            "#include <stdlib.h>\n"+

            "int main(int argc, char **argv)\n"+
            "{\n"+
            "    resultado = 3/0;\n"+
            "}\n"+
            "</code>\n\n"+
            "---FIM DA MENSAGEM---\n\n\n"+
            "Além disso, todos os comandos funcionam na dm também. "+
            "Se não quiser pedir nada no grupo, pode pedir exclusivamente pra mim :3```",
            inline=False
        )
        embed.add_field(
            name="$dm",
            value="```Eu envio uma mensagem privada pra você caso você não saiba me encontrar.```"
        )
        embed.add_field(
            name="$m",
            value="```Mostra uma lista com os períodos que possuem disciplinas com materiais. Lembrar de estar no canal materiais.```"
        )
        embed.add_field(
            name="Gerar exercícios em várias dificuldades (Ainda ta beeem cru. Tem quase nada).\n",
            value="```Para gerar um exercício, dê o comando (lembrar de estar no canal alg1):\n"+
                "$gen\n"+
                "Você verá o enunciado do exercício e um exemplo de entrada/saída.\n"+
                "Exercícios retirados da apostila:\n"+
                "CADERNO DE EXERCÍCIOS - INTRODUÇÃO À CIÊNCIA DA COMPUTAÇÃO\n"+
                "IME-USP * 13ª edição - 2005\n"+
                "Cópia feita com permissão do Departamento de Ciência da Computação da Universidade de São Paulo.```",
                inline=False
        )
        
        await context.send(embed=embed)