import binascii, re, os

def scan_file_url(file_path):
	f = open(file_path, 'rb')
	data = f.read()
	f.close()
	url=r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"	
	pattern=re.compile(url)
	rlt=pattern.findall(data)
	for link in rlt:
		print link
	return rlt

file_path="D:\open_xml\ListView.zip"
scan_file_url(file_path)