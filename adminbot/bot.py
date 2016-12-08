#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""bot.py: A Telegram bot to admin your server"""

# ----------------------------------------------------------------------#
#                               ,
#                              ▓█      ██
#                             ▄█▌      ╙█▌
#                             ▀█▌      "█▌
#                             ▐█H ╓▄▄▄  █▌
#                             ▓█▄╣█████╥██
#                     ▄▄┐    ▄ ▐█▌ ██M╫█▌ ╓     ▄▄µ
#                 ▄▄  ▐██   ▐▄ ▓█  ██Γ █▀⌐.▄   ║█▌  ╓▄
#                 ▀█▓▓▄██    ▀▄ ▓▌ ██┐▐█ ▄▀    ▓█▌▄▓██
#                   `▀▀███▄ A`╙▄╝└▓███"▀▄▀`ⁿµ,███▀▀"   .
#  -██████▄▄,,   ╓     ╙████▄▄▄█▄ⁿ⌐   ═▄█▄▄,████▀     ▄   ,,╓▄▄█████W
#        `╙▀▀██, ╓ ╙╗.'""▀█▌▀▀█████████████▀▀██T"*.▄▀,, ,▄█▀▀▀Γ'
#         ╓▓██╙██▀▄▄ "▓▄ ██W  ██████▀█████,  ██▌▄▄M ▄▄█▀█▀▄█▓▄
# ¢█▄,     ██████▄,[▐█Γ ⌠███████▀███▌║███████████░ "█▌[,▄█▓████     ,▄▓▌
# ╙▀███▄▄,╙█▀▄║▀▀▀███▌ `███████████▓████████████D ▐███▀▀▀▀▄▀█▀,▄▄▓██▀▀
#    Γ T▀▀█▀▀▀█▄╗▌▄▌▀, ▓███▀▀██████████████▀▀████ ┌▀▀▄▄▌Φ█▀▀▀██▀Γ T
#           .▄ "%,,▓▄▄▓█████████████████▓█████████▄▄█╓,/^,,=
#            `"Γ "  └██▓███████████████████████████Γ  ^ ╙▀
#          ,,    ,▄▓▄█▌  ▐██▓████▓█████████▓██▌` ▀█▓▄▒,    ,,
#         █████▓███████▓▄██████▀██████▓█▀██████▄▄███████▓█████⌐
#            ╓▓█▀╙" ▌ "▓██████▄▓████▀████▄███████▀ ║⌐╙▀▀██▄
#          Φ███     ¡╓K█`╘⌐▀████████████████▀╙╡ ▓▀╗╡     ▀██▌
#                ,ΦΓ╟ ▄▓╖▓▄µ ╠▀███▌  ▐████║ ,▄▓▄▀▄,╣7▀,
#               `" ╓█M▀ ▓███╓,▄█▀██▓▄██▀╢▌,,▓███ ╙▀▓▌ ▀
#               ▄▄▄██"▄▓█" ▄▌ ▓  ╓▓███=  ▀ ╙█=`▀█▓ ▀█▓▄▄
#              ▄█▌└█████▀▄▄▌e`▌   ║███   ╘M%▄█▄▐▀██▓█▄ █▄
#            ▄▓█╨  ▀████▐█▀ ▄▄Γ   ▄██▌    ▀▄ ╙██▓████"  ██▄
#           ╓██      "└╓▓█w      ▄█▌╙██▄   .  ██▄'l      ▀█▄
#           ██       ,▄█▀       ╙██  ▐██       ╙██▄       ▓█
#                  ,▄██H                         ██▄▄
#                 ▓█▀                              ▀██⌐
#
# ----------------------------------------------------------------------#
__author__ = "Dih5"
# ----------------------------------------------------------------------#

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json

import subprocess
import psutil
import sys
from glob import glob

from .pyshell import Shell

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Some utilities
def remove_first_word(text):
    """Given a string, remove what is found before the first space"""
    return text.split(" ", 1)[1]


def human_bytes(num, suffix='B'):
    """ Convert a number to bytes to a human-readable form"""
    # taken from http://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def human_bytes_fraction(num, total, suffix='B'):
    """ Convert a number to bytes to a human-readable form"""
    # adapted from human_bytes
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(total) < 1024.0:
            return "%3.1f/%3.1f%s%s" % (num, total, unit, suffix)
        num /= 1024.0
        total /= 1024.0
    return "%.1f%.1f%s%s" % (num, total, 'Yi', suffix)


# Classes for the bot

class BotConfig:
    """Class representing a bot configuration"""

    def __init__(self, file_path):
        self.path = file_path
        with open(file_path, 'r') as f:
            self.config = json.load(f)
        self.token = self.config["token"]
        self.admin_list = self.config["admin_list"]
        # logger.info('Loaded bot:\n"%s"' % (json.dumps(self.config, indent=4, separators=(',',': '))))
        return


class AdminBot():
    """ A class defining the bot behaviour.
        The bot answers commands added with the add_command method using a callback function.
        Non command messages are treated depending on the mode the bot is set (with respect to the user).
        Modes are added with the add_chat_mode, and commands' callback may set them calling the set_chat_mode method.
    """

    def __init__(self, file_path):
        self.config = BotConfig(file_path)
        self.updater = Updater(token=self.config.token)
        self.dispatcher = self.updater.dispatcher
        self.registered_chat_modes = {}  # mode -> command
        self.set_modes = {}  # User -> mode
        self.commands = []

    def add_command(self, command_function, name):
        """Add a command of the given name, with a callback command_function(bot,update,adminbot)"""

        def covered(bot, update):
            logger.info("User %s (%s) called: %s" % (update.message.from_user.first_name,
                                                     update.message.from_user.id, update.message.text))
            if update.message.from_user.id not in self.config.admin_list:
                update.message.reply_text("Permission denied.\nFind your own tree!")
            else:
                command_function(bot, update, self)

        self.dispatcher.add_handler(CommandHandler(name, covered))
        self.commands.append(name)

    def add_chat_mode(self, command_function, mode):
        """Add a chat mode with a callback command_function(bot,update,adminbot)"""
        self.registered_chat_modes[mode] = command_function

    def set_chat_mode(self, user, mode):
        """ Set a user in the given chat mode"""
        self.set_modes[user] = mode

    def _chat_callback(self, bot, update):
        """ Calledback for messages (no commands), dispatches according to chat mode"""
        logger.info("User %s (%s) said: %s" % (update.message.from_user.first_name,
                                               update.message.from_user.id, update.message.text))
        if update.message.from_user.id not in self.config.admin_list:
            update.message.reply_text("Permission denied.\nFind your own tree!")
            return
        user = update.message.from_user.id
        if user not in self.set_modes:
            update.message.reply_text("User has not set a chat mode")
            return
        mode = self.set_modes[user]
        if mode not in self.registered_chat_modes:
            update.message.reply_text("Error: user in an unkown chat mode")
            return
        return self.registered_chat_modes[mode](bot, update, self)

    def _error_logger(bot, update, error):
        """ Log errors"""
        logger.warn('Update "%s" caused error "%s"' % (update, error))

    def start(self):
        """ Set up and start the bot"""
        self.updater.dispatcher.add_handler(MessageHandler([Filters.text], self._chat_callback))
        self.updater.dispatcher.add_error_handler(self._error_logger)
        self.updater.start_polling()
        self.updater.idle()


# Commands

def whoami(bot, update, adminbot):
    """Command to check privileges in the system"""
    user = update.message.from_user.id
    if user in adminbot.config.admin_list:
        update.message.reply_text('Thou art our master!\nWe are pleased to see thee.')
    else:
        update.message.reply_text("We don't know thee!")


def shell(bot, update, adminbot):
    """Command to execute a shell (bash, cmd, ...) command"""
    command = remove_first_word(update.message.text)
    output = subprocess.check_output(command, shell=True)  # Output is a byte sequence
    update.message.reply_text(output.decode("utf-8"))


def pyshell(bot, update, adminbot):
    """Command to manage the python shell"""
    global sh

    user = update.message.from_user.id
    adminbot.set_chat_mode(user, "pyshell")
    command = remove_first_word(update.message.text)

    if command == "start" or command == "":
        try:
            sh
            update.message.reply_text("Interpreter already active")
        except NameError:
            sh = Shell()
            update.message.reply_text("Interpreter started")
    elif command == "restart":
        sh = Shell()
        update.message.reply_text("Interpreter started")
    elif command == "debug":
        sh = Shell(echo=True)
        update.message.reply_text("Interpreter started")
    elif command == "stop":
        del (sh)
        update.message.reply_text("Interpreter stopped")
    elif command == "check":
        try:
            sh
            update.message.reply_text("Interpreter active")
        except NameError:
            update.message.reply_text("Interpreter not active")
    elif command == "plot":
        sh.push('plt.savefig("tmp.png")')
        update.message.reply_photo(photo=open('tmp.png', 'rb'))
    else:
        update.message.reply_text("Unknown argument: " + command)


def pyshell_msg(bot, update, adminbot):
    """Command to execute a python command in a shell"""
    # TODO: move sh to adminbot object
    global sh
    command = update.message.text
    try:
        sh
    except NameError:
        sh = Shell()
        update.message.reply_text("Interpreter automatically restarted")

    output = sh.push(command)
    if output == "":
        pass
        # update.message.reply_text("Yeah")
    else:
        update.message.reply_text(output)


def top(bot, update, adminbot):
    """Command to return CPU usage"""
    proc_list = list(filter(lambda x: x[1] > 0.1, [[proc.name(), proc.cpu_percent(
    ), proc.username()] for proc in psutil.process_iter()]))
    proc_list.sort(key=lambda p: p[2])
    output = '\n'.join(map(str, proc_list))
    if output == "":
        update.message.reply_text("No significant process found.")
    else:
        update.message.reply_text(output)


def disks(bot, update, adminbot):
    """Command to return disk usage"""
    mount_points = [x.mountpoint for x in psutil.disk_partitions()]
    usage = list(map(psutil.disk_usage, mount_points))
    usage_str = map(lambda x: human_bytes_fraction(x.used, x.total) + " (" + str(x.percent) + "%)", usage)
    update.message.reply_text("\n".join([a + ': ' + b for a, b in zip(mount_points, usage_str)]))


def setkb(bot, update, adminbot):
    """Command to set a keyboard with the commands known by the bot"""
    cmds = list(map(lambda x: "/" + x, adminbot.commands))
    rows = 3
    layout = [[], [], []]
    i = 0
    for cmd in cmds:
        layout[i].append(cmd)
        i += 1
        i %= rows
    kb = ReplyKeyboardMarkup(layout)
    update.message.reply_text("Here you go!", reply_markup=kb)


def main():
    """Set up a bot from a configuration file and start it"""

    if len(sys.argv) < 2:
        l = glob("*.json")
        if len(l) == 0:
            print("No json file found.", file=sys.stderr)
            exit(1)
        elif len(l) > 1:
            print("Multiple json files found. Specify which is to be used.", file=sys.stderr)
            exit(1)
        else:
            bot_file = l[0]
    else:
        bot_file = sys.argv[1]

    bot = AdminBot(bot_file)
    bot.add_command(whoami, "whoami")
    bot.add_command(shell, "shell")
    bot.add_command(top, "top")
    bot.add_command(disks, "disks")

    bot.add_command(pyshell, "pyshell")
    bot.add_chat_mode(pyshell_msg, "pyshell")

    bot.add_command(setkb, "setkb")

    bot.start()


if __name__ == '__main__':
    main()
