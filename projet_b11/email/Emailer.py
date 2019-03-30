import smtplib

class Emailer:

    SERVER = "smtp.office365.com"
    PORT = 587

    def __init__(self, FROM, TO, SUBJECT, TEXT):
        self.FROM = FROM
        self.TO = TO
        self.TEXT = "Subject: {}\n\n{}".format(SUBJECT, TEXT)

    def send(self):
        server = smtplib.SMTP(self.SERVER, self.PORT)
        server.starttls()
        server.login("HEIG_PFAM@outlook.com", "pfamHEIGb_11")
        server.sendmail(self.FROM, self.TO, self.TEXT)
        server.quit()
