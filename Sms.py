import os
from twilio.rest import Client

def send_SMS(my_sms):

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_ACCOUNT_SID']
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=my_sms,
                         from_='+13854744244',
                         to='+50683778693'
                     )

    print(message.sid)
