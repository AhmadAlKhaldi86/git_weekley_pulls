import os
import smtplib, ssl
from email.message import EmailMessage
from decouple import config
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

SMTP_USR  = config('SMTP_USR')
SMTP_PASS = config('SMTP_PASS')
SMTP_SRV  = 'smtp.gmail.com'
SMTP_PORT = 587

def FormEmail(subject, receiver, content):
  msg            = EmailMessage()
  msg['Subject'] = subject
  msg['From']    = SMTP_USR
  msg['To']      = receiver
  # msg.set_content(content)
  
  # I propaply can externalize the html template files incase we are sending diff emails.
  html = f'''
  <!DOCTYPE html>
  <html>
      <body>
          <div style="background-color:#eee;padding:10px 20px; width:800px">
              <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">Weekley Github Pull Requests</h2>
          </div>

          <div>
            <h3 style="background-color:#eee; width:80px">Summary</h3>
            <p style="width:1500px">{content}</p>
          </div>
           <br>
           <br>

        <img src="https://dummyimage.com/200x100/000/ffffff&text=GitHub+Pulls" style="height: 100px;">
      </body>
  </html>
  '''
  msg.set_content(html,subtype='html')
  return msg

def SendMail(subject,receiver,content):
  msg     = FormEmail(subject, receiver, content)
  context = ssl.create_default_context()
  # with smtplib.SMTP(SMTP_SRV, SMTP_PORT) as smtp:
  #   smtp.starttls(context=context)
  #   smtp.login(SMTP_USR,SMTP_PASS)
  #   smtp.send_message(msg)
  
  emailStatus = {
    'success': True,
    'msg'   : f'Email was sent to {receiver}'
  }

  try:
    smtp = smtplib.SMTP(SMTP_SRV, SMTP_PORT)
    smtp.starttls(context=context)
    smtp.login(SMTP_USR,SMTP_PASS)
    smtp.send_message(msg)
  except Exception as e:
    emailStatus['success'] = False
    emailStatus['msg']    = f'Failed to send email {e}'
  finally:
    return emailStatus

    
    