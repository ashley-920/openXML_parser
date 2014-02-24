# cws2swf, based on http://zefonseca.com/cws2fws/ http://zefonseca.com/cws2fws/release/cws2fws
# python version: rawe 01.09.2010
# uncompresses a flash (cws -> fws)
#
# cws format: [3 byte signature (CWS)] [5 byte header] [rest: gzipped]
# swf format: [3 byte signature (FWS)] [5 byte header] [rest: unzipped]
# todo: replace cws with fws and uncompress the gzipped part... simple, huh?
 
import zlib
import sys
 
def cws2fws(cws, fws):
    input_file = open(cws,"rb")
    signature = input_file.read(3)
    if not signature == "CWS":
        print "no cws provided!"
        return
    header = input_file.read(5)
    content_compressed = input_file.read()
    input_file.close()
 
    print "decompressing..."
    content_uncompressed = zlib.decompress(content_compressed)
 
    output_file = open(fws,"wb")
    output_file.write("FWS")
    output_file.write(header)
    output_file.write(content_uncompressed)
    output_file.close()
    print "done"
 
argc = len(sys.argv)
if argc == 1:
    print "usage: cws2fws cws fws"
if argc == 2:
    cws2fws(sys.argv[1], sys.argv[1]+".swf")
if argc == 3:
    cws2fws(sys.argv[1], sys.argv[2])
