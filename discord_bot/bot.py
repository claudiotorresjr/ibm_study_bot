import argparse
import discord
from discord.ext import commands

from studies import study
from studies import alg1
from studies import profs

def get_arguments():
    """
        Get command line arguments
    """

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t", help="Test env", action='store_true'
    )

    options = parser.parse_args()
    return options


def main(test_env):
    """
        Função principal que inicializa o bot e todas as suas funções

        param test_env: flag que indica se estamos em um ambiente de testes
    """

    #args = get_arguments()

    prefix = "$"
    TOKEN = "ODkwMzUyMjk0ODMzNTc4MDA0.YUujMQ.IsA4kJlgh3P0vg6ya5RFaHxmYtc"

    if test_env:
        print("Bot para testes")
        prefix = "#"
        TOKEN = "OTg4ODc1NjQ4NzA3NzM1NTgy.GNLxea.2w2UGB5WHuEqnXDEcu_SHWAGAqPz4_pipqTdzU"
    
    intents = discord.Intents.default()
    intents.members = True
    my_bot = commands.Bot(command_prefix=prefix, help_command=None, intents=intents)

    my_bot.add_cog(study.StudyBot(my_bot))
    my_bot.add_cog(alg1.Alg1Bot(my_bot))
    my_bot.add_cog(profs.ProfsBot(my_bot))

    my_bot.run(TOKEN)


if __name__ == '__main__':
    args = get_arguments()

    main(args.t)