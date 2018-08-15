#!/usr/bin/env python

import socket
import sys
import ssl
import time



from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
urlText = []
attributes_url = []

Main_url_list = []


class MyHTMLParser(HTMLParser):
    #def handle_starttag(self, tag, attrs):
        #print "Start tag:", tag
        #for attr in attrs:
            #print "     attr:", attr
			
    def handle_starttag(self, tag, attrs):
        # Only parse the 'anchor' tag.
        if tag == "a":
           # Check the list of defined attributes.
            for name, value in attrs:
               # If href is defined, print it.
                if name == "href" and value.startswith("/fakebook/"):
                    print name, "=", value
                    attributes_url.append(value)


    #def handle_endtag(self, tag):
        #print "End tag  :", tag

    def handle_data(self, data):
        #print "Data     :", data
        
	if data != '\n':
            urlText.append(data)

    #def handle_comment(self, data):
        #print "Comment  :", data

    def handle_entityref(self, name):
        c = unichr(name2codepoint[name])
        #print "Named ent:", c

    def handle_charref(self, name):
        if name.startswith('x'):
            c = unichr(int(name[1:], 16))
        else:
            c = unichr(int(name))
        #print "Num ent  :", c

    #def handle_decl(self, data):
        #print "Decl     :", data

parser = MyHTMLParser()





def Send_GET_request(sock,URL,csrf_token,session_id_POST):
    Get_request = "GET " + URL + " HTTP/1.1\n"
    Get_request += "Host: cs5700sp17.ccs.neu.edu\n"
    Get_request += "Cookie: {0} {1}\n\n".format(csrf_token,session_id_POST[:-1])
	
    print(Get_request)
    sock.send(Get_request)
    data = sock.recv(12362)

    print(data)
    return data



def Create_main_queue(current_url):
	global Main_url_list
	
	Main_url_list = list(set(Main_url_list) | set(current_url))
	Main_url_list = [x for x in Main_url_list if len(x) > 10]
	

def Crawl(sock,parser,data,csrf_token,session_id_POST):
    print("==================== Start of crwling function ======================================\n\n")
    global urlText
    global attributes_url
    global Main_url_list
	
    attributes_url = []
    parser.feed(data)
    #print(attributes_url)
    Create_main_queue(attributes_url)
    print(Main_url_list)
    parser.close()
	
	#Get the flag if there
	#return condition to break recursion
    if len(Main_url_list) == 0:
		return
	
    print("==================== New GET request Start ======================================\n\n")
    data = Send_GET_request(sock,Main_url_list[0],csrf_token,session_id_POST)
    if data != 0:
        Main_url_list.pop(0)
		
    print("==================== New GET request End ======================================\n\n")
    Crawl(sock,parser,data,csrf_token,session_id_POST)
	
    return
    #attributes_url = []
    #parser.feed(data)
    #print(attributes_url)
	
	
    print("========================== End of crwling function ================================\n\n")
'''	
    Get_request = "GET " + attributes_url[1] + " HTTP/1.1\n"
    Get_request += "Host: cs5700sp17.ccs.neu.edu\n"
    Get_request += "Cookie: {0} {1}\n\n".format(csrf_token,session_id_POST[:-1])
	
    print(Get_request)
    sock.send(Get_request)
    data = sock.recv(12362)
    print(data)
    
	
    attributes_url = []
    parser.feed(data)
    print(attributes_url)
	
    print("==========================================================\n\n")
    parser.close()
	
    Get_request = "GET " + attributes_url[2] + " HTTP/1.1\n"
    Get_request += "Host: cs5700sp17.ccs.neu.edu\n"
    Get_request += "Cookie: {0} {1}\n\n".format(csrf_token,session_id_POST[:-1])
	
    print(Get_request)
	
    sock.send(Get_request)
    data = sock.recv(12362)
    print(data)
    print("==========================================================\n\n")
'''	

def StartCrawling(sock,server_address):
   # print(server_address)
    sock.connect(server_address)
    global urlText
    global attributes_url
	
    Get_request = """GET http://cs5700f16.ccs.neu.edu/ HTTP/1.0\n
\n"""

#    sock.send(Get_request)

 #   data = sock.recv(10256)
 #   print(data)


    Get_request = """GET http://cs5700f16.ccs.neu.edu/fakebook/ HTTP/1.0\n
\n"""
    #sock.send(Get_request)

    #data = sock.recv(10256)
    #print(data)

    Get_request = "GET http://cs5700sp17.ccs.neu.edu/accounts/login/ HTTP/1.1\n"
    Get_request += "Host: cs5700sp17.ccs.neu.edu\n"
    Get_request += "Connection: keep-alive\n\n"

    #print(Get_request)
    sock.send(Get_request)
    data = sock.recv(12362)

    #print(data)

    parser.feed(data)
    #print(urlText)
    headers = []
    headers = urlText[0].split('\n')
    parser.close()
    csrf_token = headers[7].split(' ')[1]
    session_id = headers[8].split(' ')[1][:-1]
	
    #print(csrf_token)
    #print(session_id)
	
    Cookie = "Cookie: " + csrf_token + " " + session_id + "\r\n"
    csrfmiddlewaretoken = "csrfmiddlewaretoken=" + csrf_token[10:]
    #print(Cookie)
    #content_length = len(csrfmiddlewaretoken[:-1] + "&username=001218078&password=A52VUCSQ&next=%2Ffakebook%2f")
	
    body = 'csrfmiddlewaretoken={0}&username=001218078&password=A52VUCSQ&next=%2fFacebook%2f'.format(csrf_token[10:-1])
    content_length = len(body)
	
    login = ["POST " + "/accounts/login/" + " HTTP/1.1",
             "Host: cs5700sp17.ccs.neu.edu",
             "Cookie: {0} {1}".format(csrf_token, session_id),
             "Connection: keep-alive",
             "Content-Type: application/x-www-form-urlencoded",
             "Content-Length: {0}".format(content_length)]
    space = "\r\n"
    newlogin = space.join(login)
    Post_message = newlogin + "\r\n\r\n" + body


	
    #print(Post_message)
    sock.send(Post_message)
    data1 = sock.recv(12345)

    #print(data1)
    
    urlText = []
    parser.feed(data1)
    #print(urlText)
    headers = urlText[0].split('\n')
    session_id_POST = headers[7].split(' ')[1]
    parser.close()
    #print(session_id_POST)
	
    Get_request = "GET http://cs5700sp17.ccs.neu.edu/fakebook/ HTTP/1.1\n"
    Get_request += "Host: cs5700sp17.ccs.neu.edu\n"
    Get_request += "Cookie: {0} {1}\n\n".format(csrf_token,session_id_POST[:-1])
	
    #print(Get_request)
    sock.send(Get_request)
    data = sock.recv(12362)

    #print(data)
    #parser.feed(data)
    #print(attributes_url)
	
    #parser.close()
	
	
    #get_friends = ["GET {0} HTTP/1.1".format(attributes_url[1]),
    #         "Host: cs5700sp17.ccs.neu.edu",
    #         "Cookie: {0} {1}\n".format(csrf_token,session_id_POST[:-1])]
    #space1 = "\n"
    #Get_request = space1.join(login)
    #Post_message = newget_freiend + "\r\n\r\n" + body
	

    print(data)
    
	
    Crawl(sock,parser,data,csrf_token,session_id_POST)

	

	
    sock.close()
	
	
	
def Main():

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    port = 80
    hostname = "cs5700f16.ccs.neu.edu"

    server_address = ( hostname , int(port))
    StartCrawling(sock,server_address)


#Trigger Main()
if __name__ == "__main__":
    Main()
