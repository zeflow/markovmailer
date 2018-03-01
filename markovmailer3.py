#!/usr/bin/python3
import os
import email
import os,re

DEBUG=False
def striphtml(data):
    p = re.compile('<.*?>',flags=re.S)
    return p.sub('', data)

def stripforwardedsegments(data):
    strippedmail=data
    # pass 1 - Normal Forwarded msg
    txt_mail_segments=re.split(r'^----- Forwarded by.*$',strippedmail,flags=re.M)
    if (len(txt_mail_segments))>0:
        strippedmail=txt_mail_segments[0]
    # pass 2 - IBM Notes awkward include mail msg
    txt_mail_segments=re.split(r'^.*---\d{0,2}-\d{0,2}-\d{0,4}\s\d{0,2}:\d{0,2}:\d{0,2}---.*$',strippedmail,flags=re.M)
    if (len(txt_mail_segments))>0:
        strippedmail=txt_mail_segments[0]
    #pass 3
    txt_mail_segments=re.split(r'^.*Begin Forwarded Message.*$',strippedmail,flags=re.M)
    if (len(txt_mail_segments))>0:
        strippedmail=txt_mail_segments[0]
    
    return strippedmail

def stripmailheaders(data):
    remove_text=True
    txt_mail=data
    if remove_text is True:
        txt_mail=re.sub(r'^To:\n\n(.*)$','',txt_mail,flags=re.M)
        txt_mail=re.sub(r'^Cc:\n\n(.*)$','',txt_mail,flags=re.M)        
        txt_mail=re.sub(r'.*\@(.*)$','',txt_mail,flags=re.M)        
    else:
        txt_mail=re.sub(r'^To:\n\n(.*)$',r'To: \1',txt_mail,flags=re.M)
        txt_mail=re.sub(r'^Cc:\n\n(.*)$',r'Cc: \1',txt_mail,flags=re.M)
    return txt_mail

mail_folder='mailexport'
for subdir, dirs, files in os.walk(mail_folder):
    for file in files:
        with open(os.path.join(mail_folder,file), encoding='utf-8') as fp:
            if DEBUG is True:
                print('[+] NEW MAIL %s' % (file) )
            text_file=fp.read()
            match=re.search("<html>(.*)</html>",text_file, flags=re.S)
            if match is not None:
                if DEBUG is True:
                    print('[+] HTML FOUND')
                # extract html and strip =\n
                html=match.group(1).replace('=\n','')
                # replace <br> with carriage return
                html=html.replace('<br>','')
                #strip html
                text=html
                text=striphtml(text)

                txt_mail=stripforwardedsegments(text)
                txt_mail=stripmailheaders(txt_mail)
                # delete footer et all
                txt_mail=re.sub(r'^Met vriendelijke groet.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'&nbsp;Met vriendelijke groet.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'^Kind regards.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'^Sent from my iPhone.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'^Sent with Good.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'^Onderwerp\:.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'^Uitnodiging\:.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'^See in cc.*','',txt_mail,flags=re.S|re.M)
                txt_mail=re.sub(r'^v\\\:\*.*','',txt_mail,flags=re.S|re.M)
		
		# remove all newlines and replace with space
                txt_mail=re.sub(r'\n',r' ',txt_mail,flags=re.S|re.M)
                # strip any double spaces
                txt_mail=re.sub(r'\s\s','',txt_mail,flags=re.S|re.M)
                # replace double dots
                #txt_mail=re.sub(r'(\.)+$','.',txt_mail,flags=re.S|re.M)
                # if . found create newline
                txt_mail=re.sub(r'\.$','.\n',txt_mail,flags=re.S|re.M)
                # if , found create newline
                #txt_mail=re.sub(r'\,\s*',',\n',txt_mail,flags=re.S|re.M)
                
                print(txt_mail.strip())
