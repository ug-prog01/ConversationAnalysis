# AUTHOR: KARTHIK PEDDI
"""This program is used to send an email to the people who participated in conversation
regarding the insights gathered from the discussion"""
"""To use this file independently the transcript of the conversation with tags must be
present in 'conv_with_tags.txt' file and the username and password of sender
should be updated along with the body"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage


#Use the below lines if this file is used independently
"""
username = ''  # Email Address of the account from which you want to send an email
password = ''  # Password

print("Enter the mail ids of the people who took part in the conversation, seperated by a space:")
email_list = input().split(" ")
"""

def send_email(username,password,email_list,to_add_in_mail):
    html = "<b>The transcript of the conversation is:</b><br><br>"
    f=open("conv_with_tags4.txt","r")
    conv=f.read()
    f.close()
    conv=conv.replace('\n','<br><b>')
    conv=conv.replace(':',':</b>')
    
    
    def send_mail(username, password, to_addrs, msg):
        server = smtplib.SMTP('smtp-mail.outlook.com', '587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)
        server.sendmail(username, to_addrs, msg.as_string())
        server.quit()
        
    for to_addrs in email_list:
        msg = MIMEMultipart()
        msg['Subject'] = "Insights from your Recent Meeting"
        msg['From'] = username
        msg['To'] = to_addrs

        no_negative=0
        try:
            topics_discussed = MIMEImage(open("topic_word_cloud.png", "rb").read())
            topics_discussed.add_header('Content-ID', 'image1')
            topics_discussed.add_header('Content-Disposition', 'attachment',filename="topic_word_cloud.png")
            msg.attach(topics_discussed)
        except:
            pass
    
        try:
            positive_word_cloud = MIMEImage(open("positive_word_cloud.png", "rb").read())
            positive_word_cloud.add_header('Content-ID', 'image2')
            positive_word_cloud.add_header('Content-Disposition', 'attachment',filename="positive_word_cloud.png")
            msg.attach(positive_word_cloud)
        except:
            pass
        
        try:
            negative_word_cloud = MIMEImage(open("negative_word_cloud.png", "rb").read())
            negative_word_cloud.add_header('Content-ID', 'image3')
            negative_word_cloud.add_header('Content-Disposition', 'attachment',filename="negative_word_cloud.png")
            msg.attach(negative_word_cloud)
        except:
            no_negative=1
    
        try:
            positivity_comparison = MIMEApplication(open("positivity_comparison.html", "rb").read())
            positivity_comparison.add_header('Content-ID', 'html1')
            positivity_comparison.add_header('Content-Disposition', 'attachment', filename="positivity_comparison.html")
            msg.attach(positivity_comparison)
        except Exception as e:
            pass

        try:
            positivity_comparison = MIMEImage(open("positivity_comparison.png", "rb").read())
            positivity_comparison.add_header('Content-ID', 'image4')
            positivity_comparison.add_header('Content-Disposition', 'attachment', filename="positivity_comparison.png")
            msg.attach(positivity_comparison)
        except Exception as e:
            pass

        try:
            confidence = MIMEImage(open("Conf.png", "rb").read())
            confidence.add_header('Content-ID', 'image5')
            confidence.add_header('Content-Disposition', 'attachment', filename="Conf.png")
            msg.attach(confidence)
        except Exception as e:
            pass

        try:
            talk_time = MIMEImage(open("Time.png", "rb").read())
            talk_time.add_header('Content-ID', 'image6')
            talk_time.add_header('Content-Disposition', 'attachment', filename="Time.png")
            msg.attach(talk_time)
        except Exception as e:
            pass

        try:
            mod = MIMEImage(open("modulation.png", "rb").read())
            mod.add_header('Content-ID', 'image7')
            mod.add_header('Content-Disposition', 'attachment', filename="modulation.png")
            msg.attach(mod)
        except Exception as e:
            pass

        if no_negative==0:
            pics='<br><b>The topic word cloud of the topics discussed in this conversation are:</b><br>' \
                  +'<p><img src="cid:image1"></p>'+'<br><b>The positive word cloud of the conversation is:</b><br>'\
                  +'<p><img src="cid:image2"></p>'+'<br><b>The negative word cloud of the conversation is:</b><br>'\
                  +'<p><img src="cid:image3"></p>'+'<br><b>The line plot comparing dialogue positvity is:</b><br>'\
                  +'<p><img src="cid:image4"></p>'+'<br><b>The confidence comparison of each speaker is:</b><br>'\
                  +'<p><img src="cid:image5"></p>'+'<br><b>The talk time of each speaker is:</b><br>'\
                  +'<p><img src="cid:image6"></p>'+'<br><b>The modulation of the audio file is:</b><br>'\
                  +'<p><img src="cid:image7"></p>'
        else:
           pics='<br><b>The topic word cloud of the topics discussed in this conversation are:</b><br>' \
                 +'<p><img src="cid:image1"></p>'+'<br><b>The positive word cloud of the conversation is:</b><br>'\
                 +'<p><img src="cid:image2"></p>'+'<br><b>The line plot comparing dialogue positvity is:</b><br>'\
                 +'<p><img src="cid:image4"></p>'+'<br><b>The confidence comparison of each speaker is:</b><br>'\
                  +'<p><img src="cid:image5"></p>'+'<br><b>The talk time of each speaker is:</b><br>'\
                  +'<p><img src="cid:image6"></p>'+'<br><b>The modulation of the audio file is:</b><br>'\
                  +'<p><img src="cid:image7"></p>'
        with open('action.txt') as action:
            data = action.read()
        data = '<br><b>The Action Items are:</b><br>' + data
        html=html+conv+pics+to_add_in_mail+data
        body = MIMEText(html,'html', 'utf-8')
        msg.attach(body)
        
        try:
            send_mail(username, password, to_addrs, msg)
        except Exception as e:
            print("Exception occured\n")
            print(e)
    return 0
