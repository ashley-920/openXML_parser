#coding=utf-8

import sys, os, struct, binascii, mmap, re
import zlib
import struct

def embed_swf_detection(path):
	count = 0
	embed_swf = {'CWS': [], 'FWS': []}
	
	#print "swf : "  + path
	with open(path, 'r+b') as f:
		map=mmap.mmap(f.fileno(), 0)
		offs = []
		
		p = re.compile('(FWS|CWS)')
		for m in p.finditer(map):
			offs.append(m.start())
		
		offs.append(map.size())
		
		for l in range(len(offs) - 1):
			msg = map[offs[l]:offs[l+1]]
			if p.findall(msg)[0] == 'CWS':
				swf_len = struct.unpack('i', map[offs[l]+4:offs[l]+8])[0]
				if binascii.hexlify(map[offs[l]+8:offs[l]+8+1]) == '78':
					try:
						#Zip algorithms:
						#compression extreme: 78DA 
						#compression standard: 789C
						#compression faible: 785E
						#有時間在把正確的 zlib 資料大小正確的解出來 . 
						d = zlib.decompress(map[offs[l]+8:])
						if len(d)+8 == swf_len:
							embed_swf['CWS'].append((offs[l], swf_len))
					except:
						{}
			elif p.findall(msg)[0] == 'FWS':
				swf_len = struct.unpack('i', map[offs[l]+4:offs[l]+8])[0]
				if swf_len <= offs[l+1]:
						embed_swf['FWS'].append((offs[l], swf_len))

	map.close()
	f.close()
	
	return embed_swf

if __name__ == '__main__':
	if len(sys.argv) >= 2:
		print(embed_swf_detection(sys.argv[1]))
	else:
		print("Syntex : \n\t%s filename" % sys.argv[0])
		