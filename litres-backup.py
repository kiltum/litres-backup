#!/usr/bin/env python

# litres.ru backup tool
# (c) 2016 multik@multik.org

import sys
import getopt
import requests
from tqdm import tqdm # pip install tqdm
import xml.etree.ElementTree as ET
import rfc6266 # pip install rfc6266
import time


debug = 0
sid = ""


def help():
    print "litres.ru backup tool"
    print "-d for debug"
    print "-u for user"
    print "-p for password"
    print "-f for format (default fb2.zip), look at https://github.com/kiltum/litres-backup"
    print "ATTN: No any check. Download to current directory"


def main(argv):
    global debug
    global sid
    user = ""
    password = ""
    form = "fb2.zip"
    try:
        opts, args = getopt.getopt(argv, "dlu:p:f:")
    except getopt.GetoptError:
        help()
        sys.exit(0)

    for opt, arg in opts:
        if opt in ("-l"):
            to_list = 1
        elif opt in ("-d"):
            debug = 1
        elif opt in ("-u"):
            user = arg
        elif opt in ("-p"):
            password = arg
        elif opt in ("-f"):
            form = arg

    if password == "" or user == "":
        print "User/Password cannot be empty"
        help()
        sys.exit(0)
    if debug == 1:
        print "User = ",user, "Password = ", password
    r = requests.post("http://robot.litres.ru/pages/catalit_authorise/",
                      data={'login': user, 'pwd': password})
    if debug == 1:
        print "Responce ", r.status_code, r.reason
        print "Responce text ",r.text

    root = ET.fromstring(r.text)
    #root = tree.getroot()
    if root.tag == "catalit-authorization-failed":
        print "Authorization failed"
        sys.exit(1)

    sid = root.attrib['sid']
    print "Welcome, ", root.attrib['login'], "(", root.attrib['mail'],")"
    print "Asking litres.ru for list of books"

    r = requests.post("http://robot.litres.ru/pages/catalit_browser/", data={'sid': sid, 'my': "1", 'limit': "0,1000"})

    if debug == 1:
        print "Responce ", r.status_code, r.reason
        print "Responce text ",r.text

    root = ET.fromstring(r.content)
    
    count_total = root.attrib['records']
    print "Total books: ", count_total

    if debug == 1:
        print root.tag, root.attrib

    count = 1

    for child in root:
        #print(child.tag, child.attrib)
        if debug == 1:
            print child.tag, child.attrib

        
        hub_id=child.attrib['hub_id']
        file_size = 0

        for elem in child.iter():
            if debug == 1:
                print elem.tag, elem.attrib, elem.text
            if elem.tag == 'file' and elem.attrib['type'] == form :
                file_size = elem.attrib['size']
        print form, file_size

        #sys.exit(0)
        
        r = requests.post("http://robot.litres.ru/pages/catalit_download_book/", 
                          data = {'sid': sid, 'art' : hub_id, 'type': form }, stream=True)

        if debug == 1:
            print "Responce ", r.status_code, r.reason

        filename= rfc6266.parse_requests_response(r).filename_unsafe

        print "(",count,"/",count_total,")",filename

        with open(filename, "wb") as handle:
            for data in tqdm(r.iter_content(), unit='b', total=int(file_size)):
                handle.write(data)
        time.sleep(1) # do not DDoS litres.
        count = count + 1


if __name__ == "__main__":
    main(sys.argv[1:])
