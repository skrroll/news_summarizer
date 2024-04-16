from feedsearch import search
from feedparser import parse
from email.message import EmailMessage
import smtplib
import os
import config
from datetime import datetime, timedelta
from time import time, mktime

def main():
    feeds = search('wyborcza.pl')
    urls = [f.url for f in feeds]
    
    print(urls)
    
    news_feed = parse(urls[0])
    entries = news_feed["entries"]
    
    email_texts = []
    
    yesterday = datetime.now() - timedelta(days=1)
    print(yesterday)

    for entry in entries[:config.max_emails]:
        if datetime.fromtimestamp(mktime(entry.published_parsed)) < yesterday:
            break
        
        print(entry["title"] + entry["published"])
        
        entry_text = ""
        entry_text += "<p><h4>" + entry["title"] + ": "
        entry_text += entry["published"] + "</h4>"
        entry_text += entry["summary"] + " <a href=" + entry["link"] + ">LINK</a></p><br/>"

        email_texts.append(entry_text)
    
    print(len(email_texts))    
    content = "<html><body>" + "".join(email_texts) + "</body></html>"
    
    msg = EmailMessage()
    
    msg.set_content(content, subtype="html")
    sender_password = os.environ.get("SENDER_PASSWORD")
    sender_email = os.environ.get("SENDER_EMAIL")
    receiver_email = os.environ.get("RECEIVER_EMAIL")
    
    msg['Subject'] = f'Wiadomosci Polska - {datetime.today().strftime('%Y-%m-%d')}'
    msg['From'] = sender_email
    msg['To'] = receiver_email
    
    print("Sending email to " + receiver_email)
    server = smtplib.SMTP_SSL('smtp.googlemail.com', 465)
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
        
main()