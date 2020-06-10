import socket, json, csv, smtplib, ssl, Sms
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import DataFrame
import numpy as np

#values = {'Temp':[], 'Int Luminica':[]}

def create_logfile():
    filename = "logfile.csv"
    csv = open(filename, 'w')
    csv.write("Timestamp,Temperature,Light Intensity  \n")
    csv.close

def data_format(info):
    info[0] = ((info[0] * 4)/10.23)-50
    info[1] = (info[1] * 100)/750
    #values['Temp'].append(info[0])
    #values['Int Luminica'].append(info[1])
    guardarInfo(info)

def show_data():
    y1 = values['Temp']
    y2 = values['Int Luminica']
    x = [i for i in range(len(y1))]
    plt.plot(x,y1)
    plt.plot(x,y2)
    plt.legend(['Temp', 'Int Luminica'])
    plt.show()

def guardarInfo(datos):
    with open('logfile.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        my_row = [str(datetime.datetime.now()),datos[0], datos[1]]
        writer.writerow(my_row)

def send_mail():

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ecadb.mail@gmail.com"  # Enter your address
    receiver_email = "aleloria@gmail.com"  # Enter receiver address
    password = 'prueba_eca'
    message = """
    Subject: Temperature Warning!!!!\n\n
    The system temperature has a recent increase.
    Check or send technical support to verify.
    
    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


#create_logfile()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
print(host)

# Bind the socket to the port
server_address = ('192.168.0.101', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(48)
            if data:
                my_data = json.loads(data)
                print(my_data)
                data_format(my_data)
                send_mail()
                Sms.send_SMS("Temperature Warning!!!! The system temperature has a recent increase. Check or send technical support to verify.")

            elif not data:
                print('no data from', client_address)
                break

    finally:
        # Clean up the connection
        connection.close()