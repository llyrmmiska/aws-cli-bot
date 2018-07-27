import logging
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
from watson_developer_cloud import ConversationV1
from itertools import chain
import json
import re
import sys
import sys
import boto3
from botocore.exceptions import ClientError
# import boto3
# from botocore.exceptions import ClientError


ACCESS_KEY = 'AKIAIDJ35KSZQWM5FUUQ'
SECRET_KEY = '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'

client = boto3.client(
    'ec2',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name='ap-south-1',
)

class botohelper:
    def create(self):
        try:
            response = client.run_instances(InstanceType='t2.micro', ImageId='ami-d783a9b8', MinCount=1, MaxCount=1, DryRun=False)
            print(response['Instances'][0]['InstanceId'])
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise


    def start(self):
        try:
            response = client.start_instances(InstanceIds=['i-0dd7e0ce458c86c3a'],DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise


    def describe(self):
        try:
            response = client.describe_instances(DryRun=True)
            print(response['Reservations'][-1]['Instances'][-1]['InstanceID'])
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise
    '''def show(self):
        try:
            instances = client.instances.filter(Filters=[{'Name':'instance-state-name', 'Values':['running']}])
            for instance in instances:
                print(instance.id,instance.instance_type)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise'''
    def stop(self):
        try:
            response = client.stop_instances(InstanceIds =['i-0dd7e0ce458c86c3a'],DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise
    def terminate(self):
        try:
            response = client.terminate_instances(InstanceIds =['i-0dd7e0ce458c86c3a'],DryRun=False)
            print(response)
        except ClientError as e:
            print(e)
            if 'DryRunOperation' not in str(e):
                raise
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


def button(bot, update):
    query=update.callback_query.data
    global context

    '''conversation = ConversationV1(username='8c27f2a6-0f18-415a-ac5d-ffd80398478c',  # TODO
                                  password='OYaSeaOlukSi',  # TODO
                                  version='2018-02-16')'''

    conversation = ConversationV1(username='2ab30c26-4a2e-43f0-a6af-2049a497a7aa',  # TODO
                                  password='Dm4VRrgqPVux',  # TODO
                                  version='2018-02-16')


    # get response from watson
    response = conversation.message(
        #workspace_id='db32ebfa-5804-4867-a5fe-0e0932d69f7d',  # TODO
        workspace_id='cc6fa16c-f905-482d-997e-24e01df4f20a',
        input={'text': query},
        context=context)
    print(json.dumps(response, indent=2))
    context = response['context']
    x = str(response['intents'][-1]['intent'])
    if x == 'create_ec2':
        b.create()

    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text

    print(resp)
    update.callback_query.message.reply_text(resp)

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def message(bot, update):
    print('Received an update')
    global context

    '''conversation = ConversationV1(username='8c27f2a6-0f18-415a-ac5d-ffd80398478c',  # TODO
                                  password='OYaSeaOlukSi',  # TODO
                                  version='2018-02-16')'''

    conversation = ConversationV1(username='2ab30c26-4a2e-43f0-a6af-2049a497a7aa',  # TODO
                                  password='Dm4VRrgqPVux',  # TODO
                                  version='2018-02-16')

    # get response from watson
    response = conversation.message(
        #workspace_id='db32ebfa-5804-4867-a5fe-0e0932d69f7d',  # TODO
        workspace_id='cc6fa16c-f905-482d-997e-24e01df4f20a',
        input={'text': update.message.text},
        context=context)
    print(json.dumps(response, indent=2))
    context = response['context']
    if not response['intents']:
        pass
    else:
        x = str(response['intents'][-1]['intent'])
        print(response)
        print('yello')
        if x == 'create_ec2':
            b.create()
        elif x == 'start_instance':
            b.start()
        elif x == 'stop_instance':
            b.stop()
        elif x == 'terminate':
            b.terminate()
    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text

    update.message.reply_text(resp)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("474783069:AAFr6RItQBEPypzHfyhVINBfqrZ-Dup84R4")
    dp = updater.dispatcher
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('launch', start))
    updater.dispatcher.add_error_handler(error)
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()






