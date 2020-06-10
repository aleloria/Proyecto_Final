import socket, json, csv, smtplib, ssl, Sms, os
import matplotlib.pyplot as plt
import datetime

# Crea el archivo csv para acumular la info recibida
def create_logfile():
    filename = "logfile.csv"
    csv = open(filename, 'w')
    csv.write("Timestamp,Temperature,Light Intensity  \n")
    csv.close

# Se le da formato a los datos recibidos del microcontrolador
def data_format(info):
    info[0] = ((info[0] * 4)/10.23)-50
    info[1] = (info[1] * 100)/750
    print(info)
    #values['Temp'].append(info[0])
    #values['Int Luminica'].append(info[1])
    if info[0] > 30 or info[1] == 0:  #Si los valores recibidos cumplen con algunos de esto valores, se envia el e-mail y el sms
        send_mail()
        Sms.send_SMS("Temperature Warning!!!! The system temperature has a recent increase. Check or send technical support to verify.")
    guardarInfo(info)

# Escribe los datos en el archivo csv
def guardarInfo(datos):
    with open('logfile.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        my_row = [str(datetime.datetime.now()),datos[0], datos[1]]
        writer.writerow(my_row)

# Envia el e-mail
def send_mail():
    # Datos para el envio del e-mail
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "ecadb.mail@gmail.com"  # Enter your address
    receiver_email = "aleloria@gmail.com"  # Enter receiver address
    password = os.environ['GMAIL_PASSWORD_TEST']
    message = """
    Subject: Temperature Warning!!!!\n\n
    The system temperature has a recent increase.
    Check or send technical support to verify.
    
    This message is sent from Python."""
    # Funcion que envia el e-mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

#create_logfile()

# Creacion del socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname(socket.gethostname())
print(host)

# Enlaza el socket a la IP y puerto indicado
server_address = ('192.168.0.101', 10000)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)

# Escucha por un conexion entrante
sock.listen(1)

while True:
    # Espera por una conexion
    print('waiting for a connection')
    connection, client_address = sock.accept()
    try:
        print('connection from', client_address)

        # Recive la informacion
        while True:
            data = connection.recv(48)
            if data:
                my_data = json.loads(data)
                data_format(my_data)

            elif not data:
                print('no data from', client_address)
                break
    finally:
        # Limpia la conexion
        connection.close()