import os, sys
import string
import re

#import yara
import mmap
import shutil
import binascii, struct
import ctypes, ctypes.wintypes
import subprocess
import zipfile

#temp_path = 'D:\\tmp' # ram disk
des_dir=''
temp_path=''
swf_file_name=[]
filename=''

def mkdir_temp(tmp):
	global temp_path
	#print temp_path
	unzip = os.path.join(temp_path, tmp)
	# print unzip
	if not os.path.exists(unzip):
		os.mkdir(unzip)
	return unzip

def del_temp(tmp):
	global temp_path
	unzip = os.path.join(temp_path, tmp)
	if os.path.exists(unzip):
		shutil.rmtree(unzip, True)

def process_file(file_path, des_file_path):
	global des_dir
	global temp_path
	global filename	
	des_dir=des_file_path
	filename=os.path.basename(file_path)
	# filename=filename.replace(" ","_")
	temp_path=des_file_path+"\\"+filename
	mkdir_temp(temp_path)
	#size = os.path.getsize(file_path)
	#print "%s %d" % (file_path, size)	
	filetype = ''
	open(file_path,"rb")
	# print file_path
	# print temp_path
	dfile=zipfile.ZipFile(file_path)
	dfile.extractall(temp_path)
	for name in dfile.namelist():
		if name.endswith(".bin"):
			# print name
			name=name.replace("/","\\")			
			detect_swf(temp_path+"\\"+name)


	# if filetype != None and active == 1:
	# print "process_file"
	# 	# print file_path
	# fn = os.path.basename(file_path)
	# unzip = mkdir_temp(fn)
	# 	#print("unzip",unzip)
	# # testpw = ''.join(os.popen(prog_7z + ' e -y -o"' + unzip + '" "' + file_path + '"').readlines())

	# listfile = []
	# for root, dirs, files in os.walk(unzip):
	# 	for name in files:
	# 		if re.search(r'ActiveX\d+.bin', name, re.I) is not None:
	# 			listfile.append(os.path.join(root, name))
	# for i in listfile:
	# 	detect_swf(i)
	# del_temp(fn)
	return swf_file_name

def getOffsetInFile(pattern, fn):
	data = str.upper(binascii.hexlify(fn))

	offs = []
	if len(data) > 0:
		p = re.compile(pattern)
		for m in p.finditer(data):
			offs.append(m.start()/2)
		return offs

def extract_swf(bin_path, file_content, offset):
	global des_dir
	global filename
	# print "extract_swf"
	data = file_content
	i = 0
	for offs in offset:
		if data[offs:offs+3] == 'FWS' or data[offs:offs+3] == 'CWS':
			ver = struct.unpack("B", data[offs+3:offs+4])[0]
			if ver >=0 and ver <= 30:
			#if True:
			# print data[offs:offs+3]
				swf_len = struct.unpack('i', data[offs+4:offs+8])[0]
			# print swf_len
				# file_name=file_path[:file_path.rfind('\\')]
				bin_name=os.path.basename(bin_path)
				bin_name=bin_name.replace(" ","_")
				bin_name=bin_name.replace(".","_")
				newfile = "[%s]_%s_%s_%08X" % (filename,bin_name, data[offs:offs+3], offs)
				f = open(des_dir+"\\"+newfile, 'wb')
				f.write(data[offs:offs+swf_len])
				f.close()
	return des_dir+"\\"+newfile

def detect_swf(file_path):
	global swf_file_name
	f = open(file_path, 'rb')
	swf = f.read()
	f.close()
	found=False

	cws = getOffsetInFile(str.upper(binascii.hexlify('CWS')), swf)
	if cws:
		# print cws
		#print file_path
		name=extract_swf(file_path, swf, cws)
		swf_file_name.append(name)
		found=True

	fws = getOffsetInFile(str.upper(binascii.hexlify('FWS')), swf)
	if fws:
		# print fws
		#print file_path
		name=extract_swf(file_path, swf, fws)
		swf_file_name.append(name)
		found=True
	return found


def find_file(dir_name):
	FILE_ATTRIBUTE_DIRECTORY = 0x10
	INVALID_HANDLE_VALUE = -1

	BAN = (u'.', u'..')
	PATH = u''

	FindFirstFile = ctypes.windll.kernel32.FindFirstFileW
	FindNextFile  = ctypes.windll.kernel32.FindNextFileW
	FindClose     = ctypes.windll.kernel32.FindClose

	out  = ctypes.wintypes.WIN32_FIND_DATAW()
	fldr = FindFirstFile(os.path.join(dir_name, u'*'), ctypes.byref(out))

	while (fldr != INVALID_HANDLE_VALUE):
		if out.cFileName not in BAN:
			PATH = os.path.join(dir_name, out.cFileName)
			if (out.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY == FILE_ATTRIBUTE_DIRECTORY):
				find_file(PATH)
			else:
				process_file(PATH)

		if not FindNextFile(fldr, ctypes.byref(out)):
			break

	FindClose(fldr)



if __name__ == '__main__':
	if len(sys.argv) >= 2:
		process_file(sys.argv[1],sys.argv[2])
	else:
		print "Syntex : \n\t%s path" % sys.argv[0]

