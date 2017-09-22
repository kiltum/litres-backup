#!/usr/bin/env python

"""
Very simple tool for backup litres.ru catalog
(c) 2017 kiltum@kiltum.tech
pep8 --ignore=W191,E501 litres-backup.py
for work:
pip install tqdm
pip install rfc6266
"""

import sys
import argparse
import requests
from tqdm import tqdm
import xml.etree.ElementTree as ET
import rfc6266
import time

FORMATS = ['fb2.zip', 'html', 'html.zip', 'txt', 'txt.zip', 'rtf.zip', 'a4.pdf', 'a6.pdf', 'mobi.prc', 'epub', 'ios.epub']
URL = "http://robot.litres.ru/pages/"


def main(argv):
	parser = argparse.ArgumentParser(description='litres.ru backup tool')
	parser.add_argument("-u", "--user", help="Username")
	parser.add_argument("-p", "--password", help="Password")
	parser.add_argument("-f", "--format", default="ios.epub", help="Downloading format. 'list' for available")
	parser.add_argument("-d", "--debug", action="store_true", help="Add debug output")
	parser.add_argument("-v", "--verbosedebug", action="store_true", help="You really want to see what happens?")
	args = parser.parse_args()

	if args.format == 'list':
		for f in FORMATS:
			print f
		exit(0)
	else:
		if args.format not in FORMATS:
			print "I dont know this format: " + args.format
			exit(1)

	if str(args.user) == 'None' or str(args.password) == 'None':
		print "I cant work without username and passwords"
		exit(1)

	if args.debug:
		print "Will ask for downloading " + args.format
		print "Try to login to site as " + args.user

	r = requests.post(URL + "catalit_authorise/", data={'login': args.user, 'pwd': args.password})
	if args.debug:
		print "Responce : ", r.status_code, r.reason
		print "Responce text : " + r.text

	root = ET.fromstring(r.text)

	if root.tag == "catalit-authorization-failed":
		print "Authorization failed"
		exit(1)

	sid = root.attrib['sid']
	if args.debug:
		print "Welcome, ", root.attrib['login'], "(", root.attrib['mail'], ")"
		print "Asking litres.ru for list of books (can take a some time)"

	r = requests.post(URL + "catalit_browser/", data={'sid': sid, 'my': "1", 'limit': "0,1000"})

	if args.verbosedebug:
		print "Responce ", r.status_code, r.reason
		print "Responce text ", r.text

	root = ET.fromstring(r.content)

	count_total = root.attrib['records']
	if args.debug:
		print "Total books: ", count_total

	if args.verbosedebug:
		print root.tag, root.attrib

	count = 1

	for child in root:
		if args.verbosedebug:
			print child.tag, child.attrib
		hub_id = child.attrib['hub_id']
		file_size = 0

		for elem in child.iter():
			if elem.tag == 'file' and elem.attrib['type'] == args.format:
				file_size = elem.attrib['size']
			if args.verbosedebug:
				print elem.tag, elem.attrib, elem.text, file_size

		r = requests.post(URL + "catalit_download_book/", data={'sid': sid, 'art': hub_id, 'type': args.format}, stream=True)

		if args.debug:
			print "Responce ", r.status_code, r.reason

		filename = rfc6266.parse_requests_response(r).filename_unsafe
		print "(", count, "/", count_total, ")", filename
		with open(filename, "wb") as handle:
			for data in tqdm(r.iter_content(), unit='b', total=int(file_size)):
				handle.write(data)
		time.sleep(1)  # do not DDoS litres.
		count = count + 1


if __name__ == "__main__":
	main(sys.argv[1:])
