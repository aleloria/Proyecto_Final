import os
from twilio.rest import Client

#Funcion para enviar el SMS
def send_SMS(my_sms):
    # Datos de la cuenta
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)
    #Funcion que envia el sms
    message = client.messages \
                    .create(
                         body=my_sms,
                         from_='+13854744244',
                         to='+50683778693'
                     )

    print(message.sid)
