import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "razerockztech@gmail.com"
password = "Scooby@77G"

class MailService:

    def sendEmail(receiver_email, subject, username, keyWord, extraPass):
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = receiver_email

            if keyWord == "register":
                bodyWord = "Your account has been registered successfully"
            elif keyWord == "update":
                bodyWord = "Your account has been updated successfully" 
            elif keyWord == "delete":
                bodyWord = "Your account has been deleted successfully"
            elif keyWord == "passchange":
                bodyWord = "Your existing password details: " + extraPass 


            # Create the plain-text and HTML version of your message
            text = """\
            Dear %s,
            %s.""" % (username, bodyWord)
            html = """\
            <html>
            <body>
                <p>Dear %s,
                <p></p>
                <br>
                %s.<br>
                </p>
            </body>
            </html>
            """ % (username, bodyWord)

            # Turn these into plain/html MIMEText objects
            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            message.attach(part1)
            message.attach(part2)

            # Create secure connection with server and send email
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )

        except Exception as error:
            print (error)