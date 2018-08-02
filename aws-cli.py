import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from watson_developer_cloud import ConversationV1
from itertools import chain
import json
import sys
import boto3
from botocore.exceptions import ClientError
client = None
class botohelper:
    def create(self,ima,abcd):
        try:
            response = client.run_instances(InstanceType='t2.micro', ImageId=ima, MinCount=1, MaxCount=abcd, DryRun=False)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise

    def start(self,fgh):
        try:
            response = client.start_instances(InstanceIds=[fgh], DryRun=False)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise

    def describe(self):
        try:
            response = client.describe_instances(DryRun=False)
            global arr
            arr = []
            for res in response['Reservations']:
                for ins in res['Instances']:
                    ins_id = ins['InstanceId']
                    state = ins['State']['Name']
                    arr.append((ins_id, state))
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise

    def stop(self, lol1):
        try:
            response = client.stop_instances(InstanceIds=[lol1], DryRun=False)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise

    def terminate(self, lol):
        try:
            response = client.terminate_instances(InstanceIds =[lol], DryRun=False)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise
    def printinst(bot, update,l):
        update.message.reply_text(l)
b = botohelper()
context = None
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

def start(bot, update):
    keyboard = [[InlineKeyboardButton("Create EC2 instance", callback_data="Create ec2 instance")],
                 [InlineKeyboardButton("Start/Stop EC2 instance", callback_data="Start/Stop ec2 instance")],
                [InlineKeyboardButton("Check number of EC2 instances", callback_data="Instance count")],
                [InlineKeyboardButton("Terminate EC2 instance", callback_data="Terminate ec2")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

def message(bot, update):
    print('Received an update')
    global context
    conversation = ConversationV1(username='USERNAME',  # TODO
                                  password='PWD',  # TODO
                                  version='2018-02-16')
    response = conversation.message(
        workspace_id='workspace_ID',
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))
    context = response['context']
    if not response['intents']:
        pass
    else:
        global y
        try:
            if response['intents'][-1]['intent'] == 'greetings' and response['entities'][-1]['entity'] == 'yes':
                global skey
                global akey
                skey = response['context']['secret_key']
                akey = response['context']['access_key']
                global client
                client = boto3.client(
                                    'ec2',
                                    aws_access_key_id=akey,
                                    aws_secret_access_key=skey,
                                    region_name='ap-south-1',
                                )
                global abcdef
                abcdef = update.message.chat.id
            try:
                if response['context']['no_of_instances'] is not None:
                    y = response['context']['no_of_instances']
            except KeyError:
                pass
            try:
                if response['intents'][-1]['intent'] == 'start_instance':
                    global tree
                    tree = response['context']['ec2']
            except KeyError:
                pass
            try:
                if response['context']['os'] is not None:
                    version=response['context']['os']
                    print('OS version : ', version)
                    if version=='windows':
                        imageid='ami-ae1627c1'
                    else:
                        imageid='ami-d783a9b8'
            except KeyError:
                pass
            try:
                if response['intents'][-1]['intent']=="terminate":
                    global unicorn
                    unicorn = response['context']['instance']
            except KeyError:
                pass
            try:
                if response['intents'][-1]['intent']=="stop_instance":
                    global unicorn1
                    unicorn1 = response['context']['ec2id']
            except KeyError:
                pass
        except IndexError:
            pass
        except NameError:
            pass

        x = str(response['intents'][-1]['intent'])
        try:
            if x == 'create_ec2':
                try:
                    if y:
                        b.create(ima=imageid, abcd=y)
                except NameError:
                    print(NameError)
                    pass
            elif x == 'start_instance':
                b.describe()
                showa(bot, update)
                b.start(tree)
            elif x == 'stop_instance':
                b.describe()
                showa(bot, update)
                b.stop(unicorn1)
            elif x == 'terminate':
                b.describe()
                showa(bot, update)
                b.terminate(unicorn)
            elif x=='describe_instance':
                b.describe()
                showa(bot,update)
        except NameError:
            print(NameError)
    resp = ''
    for text in response['output']['text']:
        resp += text
    update.message.reply_text(resp)

def showa(bot,update):
    for i in range(len(arr)):
        bla, bee = arr[i][0], arr[i][1]
        if(bee!='terminated'):
            bot.send_message(chat_id=abcdef, text=bla + ' : ' + bee)


def main():
    global updater
    updater = Updater("BOT_TOKEN")
    global dp
    dp = updater.dispatcher
    updater.dispatcher.add_handler(CommandHandler('launch', start))
    updater.dispatcher.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.text, message))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()





