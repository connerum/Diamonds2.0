import requests
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse, Body, Message, Redirect
from twilio.twiml.voice_response import Play, VoiceResponse
from twilio.rest import Client
from collections import Counter
import random
#Client Access:xeSv5omFfYVT0tIeJFtFzNZgVIaqA72afMae0Aoqb7YhzVjTaDlbK9mDmtNcuu4E
#Client Secret:UFPBaLhnQdlNQQHi4ATk0Huh_1ZrFXSu47HgsVuatv1Q3eN_SNkDjWo1bRVZRTnPgk37RfKbmdTJbFwUkgFiCw
#Client ID: Uf3rZpiOkF1CWznU_Z3LO9sGcB1PmZgP6L-BN6LKidGpKrTxC-1wOiXyoT0MFbeY


app = Flask(__name__)
ACCOUNT_SID = "ACb5537084e51524aa6cbb9b4ccdf0c9fc"
AUTH_TOKEN = "4136e7983784112fd765705d55a023e6"
client = Client(ACCOUNT_SID, AUTH_TOKEN)
dice = (u"\U0001F3B2")
diamond = (u"\uE035")
stack = (u"\U0001F4B5")
gift = (u"\uE112")
bag = (u"\U0001F4B0")
list = [dice, diamond, stack, gift, bag]



@app.route("/", methods=['GET', 'POST'])
def sms_reply():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    if 'deposit' in incoming_msg:
        textMsg = msg.body("Reply CASH for Cashapp Deposit\nReply BTC for Bitcoin Deposit")
    if 'cash' in incoming_msg:
        textMsg = resp.message("Please Deposit to the Following Cash App:\n$DiamondGameDepo")
        msg.media("https://iris-bobcat-9147.twil.io/assets/CashApp.jpg")
    if 'btc' in incoming_msg:
        textMsg = resp.message("Please Deposit to the Following Bitcoin Address:\n\nbc1q03trgeefyf34c7jsjcn3alpv0lq023jyzvqjad")
        msg.media("https://iris-bobcat-9147.twil.io/assets/download.png")
    if 'bal' in incoming_msg:
        incoming_sender = request.values.get('From')
        textMsg = msg.body(balance(incoming_sender))
    if ('bet'+":") in incoming_msg:
        betAmt = incoming_msg.split(":")
        if isinstance(float(betAmt[1]), float):
            textMsg = (random.choice(list) + " " +  random.choice(list) + " " + random.choice(list) + " " + random.choice(list) + " " + random.choice(list))
            msg.body(textMsg + '\n' + winLoss(textMsg, betAmt))
        else:
            msg.body('Please enter a valid bet amount!')

    return str(resp)

def winLoss(textMsg, betAmt):
    resp = MessagingResponse()
    msg = resp.message()
    result = textMsg.split(" ")
    total = Counter(result)
    count1 = total['\ue035']
    count2 = total['💰']
    count3 = total['💵']
    count4 = total['🎲']
    count5 = total['\ue112']
    winMsg = ''
    if int(count1) >= 5 or int(count2) >= 5 or int(count3) >= 5 or int(count4) >= 5 or int(count5) >= 5:
        print("50x")
        winMsg = ('50X' + '\n' + str(50*float(betAmt[1])))
    elif int(count1) == 4 or int(count2) == 4 or int(count3) == 4 or int(count4) == 4 or int(count5) == 4:
        print('5X')
        winMsg = ('5X' + '\n' + str(5*float(betAmt[1])))
    elif (int(count1) == 3 or int(count2) == 3 or int(count3) == 3 or int(count4) == 3 or int(count5) == 3) and (int(count1) == 2 or int(count2) == 2 or int(count3) == 2 or int(count4) == 2 or int(count5) == 2):
        print('4X')
        winMsg = ('4X' + '\n' + str(4*float(betAmt[1])))
    elif int(count1) == 3 or int(count2) == 3 or int(count3) == 3 or int(count4) == 3 or int(count5) == 3:
        print('3X')
        winMsg = ('3X' + '\n' + str(3*float(betAmt[1])))
    elif int(count1) + int(count2) == 4 or int(count1) + int(count3) == 4 or int(count1) + int(count4) == 4 or int(count1) + int(count5) == 4 or int(count2) + int(count3) == 4 or int(count2) + int(count4) == 4 or int(count2) + int(count5) == 4 or int(count3) + int(count4) == 4 or int(count3) + int(count5) == 4 or int(count4) + int(count5) == 4:
        print('2X')
        winMsg = ('2X' + '\n' + str(2*float(betAmt[1])))
    elif int(count1) == 2 or int(count2) == 2 or int(count3) == 2 or int(count4) == 2 or int(count5) == 2:
        print('0.10X')
        winAmt = 0.1*float(betAmt[1])
        winMsg = ('0.10X' + '\n' + str(round(winAmt, 2)))
    else:
        print('0X')
        winMsg = ('0X' + '\n' + str(0*float(betAmt[1])))
    print(betAmt[1])
    return winMsg
    print(count1)
    print(count2)
    print(count3)
    print(count4)
    print(count5)

def balance(incoming_sender):
    phoneBal = incoming_sender
    file = open("bal.txt", "r")
    for line in file:
        fields = line.split(":")
        number = fields[0]
        bal = fields[1]
        if phoneBal in fields[0]:
            print(bal)
    return bal

if __name__ == "__main__":
    app.run(debug=True)
