from twilio.rest import Client

def send_SMS(my_sms):

    account_sid = 'AC90e3ad16d45e359e3ec4736138798bea'
    auth_token = 'f2a6cef38ab0df1d24249f964af2428f'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=my_sms,
                         from_='+13854744244',
                         to='+50683778693'
                     )

    print(message.sid)
