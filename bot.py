#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Create calendar events inline bot

import logging
import os

from telegram.ext import Updater, Job

from modules.commands import CommandsModule
from modules.inline import InlineModule
from packs.langpack import LangpackModule

from config import params

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def error(bot, update, err):
    logger.warn('Update "%s" caused error "%s"' % (update, err))


def load_modules(dispatcher, modules):
    for module in modules:
        for handler in module.get_handlers():
            dispatcher.add_handler(handler)

def load_langpack(dispatcher, packs):
    for langpack in packs:
        for handler2 in langpack.get_handlers2():
            dispatcher.add_handler(handler2)

def main():
    updater = Updater(params['token'])
    j = updater.job_queue

    dp = updater.dispatcher

    load_langpack(dp, [LangpackModule()])
    load_modules(dp, [CommandsModule(), InlineModule()])

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

    job_minute = Job(callback_test, 1.0)
    j.put(job_minute, next_t=0.0)

if __name__ == '__main__':
    main()
