import smtplib
from Emailer import Emailer

try:
    myMailer = Emailer("HEIG_PFAM@outlook.com", "danielpaiva@hotmail.fr", "Fin du script", "Le script a fini de s'executer !")
except smtplib.SMTP.Error as e:
    print(e)
# Works !!!
myMailer.send()
