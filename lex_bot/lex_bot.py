import sys
import os
import time

import boto3
import yaml

if len(sys.argv) == 1:
    print("Error: need to specify status, either deploy or delete")
    print("Usage: python lext_bot.py status")
    sys.exit(-1)

status = sys.argv[1]

rootdir = cwd = os.getcwd()
lex = boto3.client('lex-models')

def deploy_bot(rootdir):
    intent_folder = os.path.join(rootdir, "intent")
    intents = os.listdir(intent_folder)
    deploy_intents(intent_folder, intents)

    bot_folder = os.path.join(rootdir, "bot")
    bots = os.listdir(bot_folder)

    for bot in bots:
        with open(os.path.join(bot_folder,bot), 'r') as stream:
            try:
                botFile = yaml.full_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        try:
            botFile_aws = lex.get_bot(name=botFile["name"], versionOrAlias="$LATEST")
            botFile["checksum"] = botFile_aws["checksum"]
        except Exception as e:
            print(e)
        bla = lex.put_bot(**botFile)

def deploy_intents(intent_folder, intents):
    for intent in intents:
        with open(os.path.join(intent_folder,intent), 'r') as stream:
            try:
                intentFile = yaml.full_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        try:
            intentFile_aws = lex.get_intent(name=intentFile["name"], version="$LATEST")
            intentFile["checksum"] = intentFile_aws["checksum"]
        except Exception as e:
            print(e)
        lex.put_intent(**intentFile)

def delete_bot(rootdir):
    intent_folder = os.path.join(rootdir, "intent")
    intents = os.listdir(intent_folder)

    bot_folder = os.path.join(rootdir, "bot")
    bots = os.listdir(bot_folder)

    for bot in bots:
        with open(os.path.join(bot_folder,bot), 'r') as stream:
            try:
                botFile = yaml.full_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        try:
            response = lex.delete_bot(name=botFile["name"])
        except Exception as e:
            print(e)

    time.sleep(10)
    delete_intents(intent_folder, intents)

def delete_intents(intent_folder, intents):
    for intent in intents:
        with open(os.path.join(intent_folder,intent), 'r') as stream:
            try:
                intentFile = yaml.full_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
        try:
            lex.delete_intent(name=intentFile["name"])
        except Exception as e:
            print(e)

if status == 'deploy':
    deploy_bot(rootdir)
else:
    delete_bot(rootdir)

