import pandas as pd
import pyodbc
import getpass
import os
import csv
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

N_DAYS_AGO = int(os.getenv("N_DAYS_AGO"))
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_ADDRESS_TO_SENT = os.getenv("EMAIL_ADDRESS_TO_SENT").split(",")
sender_name = os.getenv("SENDER_NAME")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))
smtp_username = os.getenv("SMTP_USERNAME")
smtp_password = os.getenv("SMTP_PASSWORD")
server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
trusted_connection = os.getenv("SQL_TRUSTED_CONNECTION")

current_date = datetime.date.today()
date_n_days_ago = current_date - datetime.timedelta(days=N_DAYS_AGO)
current_date_formatted = str(date_n_days_ago).replace("-", "")
current_datetime = datetime.datetime.now()
datetime_n_days_ago = current_datetime - datetime.timedelta(days=N_DAYS_AGO)
custom_datetime = datetime_n_days_ago.strftime("%Y-%m-%d %H:%M:%S")
custom_datetime_formatted = custom_datetime.replace("-", "").replace(":", "").replace(" ", "_")
print(custom_datetime_formatted)

receiver_emails = EMAIL_ADDRESS_TO_SENT
bcc_emails = []
subject = "ALARMÍSTICA em Produção- Extração de dados diários com informação de envio de mensagens EDI"
body = "<p>Olá,</p>"
body += "<p>Junto envio informações de evidências de envio de mensagens EDI pela ALARMÍSTICA.</p>"

message = MIMEMultipart()
message["From"] = f"{sender_name} <{EMAIL_ADDRESS}>"
message["To"] = ", ".join(receiver_emails)
message["Bcc"] = ", ".join(bcc_emails) if bcc_emails else None
message["Subject"] = subject

windows_user = getpass.getuser()
print('passed ' + windows_user)

conn_str = f"DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection={trusted_connection};UID={windows_user}"
conn = pyodbc.connect(conn_str)

sql_query_a1 = """select direction Direção, messagetype TipoMensagem, max(UpdatedOn) UltimaData, count(*) ContadorMensagensHaUmDia
                    from TrafficMessageControl with (nolock) 
                    where UpdatedOn > getdate()-10
                    group by direction, messagetype
                    ORDER by 3
                """

df = pd.read_sql(sql_query_a1, conn)
try:
    conn.close()
    print("Database connection closed")
except Exception as e:
    print(f"An error occurred: {e}")
    raise

table_html = df.to_html(index=False)
body += f"<p>{table_html}</p>"
body += "<p>Atenção: a tabela está ordenada pela coluna 'UltimaData' e o contador de mensagens é apresenta a soma de mensagens desde a hora de envio do email até 1 dia para trás</p>"
body += "<p>Cumprimentos, </p>"
body += "<p>Nuno Franco</p>"

message.attach(MIMEText(body, "html"))

with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(EMAIL_ADDRESS, receiver_emails + bcc_emails, message.as_string())

print("Email sent successfully!")