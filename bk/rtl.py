import os, sys, binascii

from struct import *
from ctypes import *


try:
	nt = windll.ntdll
except:
	logging.error("you must be running windows to use windows ntdll...")
	sys.exit()

#http://www.literatecode.com/wzip
#http://msdn.microsoft.com/en-us/library/windows/hardware/ff552191(v=vs.85).aspx
#http://msdn.microsoft.com/en-us/library/windows/hardware/ff552127(v=vs.85).aspx
#http://undocumented.ntinternals.net/UserMode/Undocumented%20Functions/Compression/RtlCompressBuffer.html
#http://bbs.csdn.net/topics/370125621
#http://www.winehq.org/pipermail/wine-patches/2002-September/003297.html
#	
# RtlCompressBuffer
# http://undocumented.ntinternals.net/UserMode/Undocumented%20Functions/Compression/RtlCompressBuffer.html
# NTSYSAPI 
# NTSTATUS
# NTAPI
# RtlCompressBuffer(
#  IN ULONG                CompressionFormat,
#  IN PVOID                SourceBuffer,
#  IN ULONG                SourceBufferLength,
#  OUT PVOID               DestinationBuffer,
#  IN ULONG                DestinationBufferLength,
#  IN ULONG                Unknown,
#  OUT PULONG              pDestinationSize,
#  IN PVOID                WorkspaceBuffer );

COMPRESSION_FORMAT_LZNT1    		= 0x0002

COMPRESSION_ENGINE_STANDARD			= 0x0000 # Standart compression
COMPRESSION_ENGINE_MAXIMUM			= 0x0100 # Maximum (slowest but better)

STATUS_SUCCESS 									= 0x00000000
STATUS_INVALID_PARAMETER				= 0xC000000D
STATUS_UNSUPPORTED_COMPRESSION	= 0xC000025F
STATUS_BAD_COMPRESSION_BUFFER		= 0xC0000242

#NTSTATUS RtlGetCompressionWorkSpaceSize(
#  _In_   USHORT CompressionFormatAndEngine,
#  _Out_  PULONG CompressBufferWorkSpaceSize,
#  _Out_  PULONG CompressFragmentWorkSpaceSize
#);

STATUS_BUFFER_ALL_ZEROS					= 0x00000117
STATUS_NOT_SUPPORTED						= 0xC00000BB
STATUS_BUFFER_TOO_SMALL					= 0xC0000023



#NTSTATUS RtlDecompressBuffer(
#  _In_   USHORT CompressionFormat,
#  _Out_  PUCHAR UncompressedBuffer,
#  _In_   ULONG UncompressedBufferSize,
#  _In_   PUCHAR CompressedBuffer,
#  _In_   ULONG CompressedBufferSize,
#  _Out_  PULONG FinalUncompressedSize
#);

def rtldecompress(path):
	f = open(path, 'rb')
	data = f.read()
	f.close()
	
	BuffSize = c_ulong(0)
	FragSize = c_ulong(0)
	
	compressed = create_string_buffer(data)
	uncompressed = create_string_buffer(0xFFFF)
	final_size = c_ulong(0)
	comp_size = len(data)
	uncomp_size = len(data) << 6

	nt.RtlDecompressBuffer(0x102, uncompressed, uncomp_size, compressed, comp_size, byref(final_size))
	
	f = open(path+".de", "wb")
	f.write(uncompressed[0:final_size.value-1])
	f.close()
	
#	if (nt.RtlGetCompressionWorkSpaceSize(COMPRESSION_FORMAT_LZNT1, byref(BuffSize), byref(FragSize)) == STATUS_SUCCESS):
	
#	compressed = create_string_buffer(data)
#	uncompressed = create_string_buffer(0xFFFF)
#	final_size = c_ulong(0)
#	comp_size = unpack("!H", len(data))[0]
#	uncomp_size = unpack("!H", len(data) << 6)[0]
#
#	if nt.RtlDecompressBuffer(
#		     2,                # COMPRESSION_FORMAT_LZNT1
#		     uncompressed,     # UncompressedBuffer
#		     uncomp_size,      # UncompressedBufferSize
#		     compressed,       # CompressedBuffer
#		     comp_size,        # CompressedBufferSize
#		     byref(final_size) # FinalUncompressedSize
#		     ):
#		return uncompressed[0:final_size.value]

#NTSTATUS RtlCompressBuffer(
#  _In_   USHORT CompressionFormatAndEngine,
#  _In_   PUCHAR UncompressedBuffer,
#  _In_   ULONG UncompressedBufferSize,
#  _Out_  PUCHAR CompressedBuffer,
#  _In_   ULONG CompressedBufferSize,
#  _In_   ULONG UncompressedChunkSize,
#  _Out_  PULONG FinalCompressedSize,
#  _In_   PVOID WorkSpace
#);
	
def rtlcompress(path):
	f = open(path, 'rb')
	data = f.read()
	f.close()
	
	BuffSize = c_ulong(0)
	FragSize = c_ulong(0)
	
	src = create_string_buffer(data)
	#print type(src), sizeof(src), repr(src.raw)
	dst = create_string_buffer(0xFFFF)
	#print type(dst), sizeof(dst), repr(dst.raw)
	
	#if (nt.RtlGetCompressionWorkSpaceSize(COMPRESSION_FORMAT_LZNT1, byref(BuffSize), byref(FragSize)) == STATUS_SUCCESS):
	tmpSpace = create_string_buffer(0xFFFF)
	FragSize = 0xFFFF
	dst_size = len(dst)
	src_size = len(src)
	
	#print "%08X" % (COMPRESSION_FORMAT_LZNT1 | COMPRESSION_ENGINE_MAXIMUM)
	res = nt.RtlCompressBuffer(0x2, src, src_size, dst, dst_size, FragSize, byref(BuffSize), tmpSpace)
	
	#print repr(dst.raw[:BuffSize.value])

	f = open(path+".en", 'wb')
	f.write(dst.raw[:BuffSize.value])
	f.close()
	
if __name__ == '__main__':
	if len(sys.argv) >= 3:

		if (sys.argv[1] == 'd'):
			rtldecompress(sys.argv[2])
		elif (sys.argv[1] == 'e'):
			rtlcompress(sys.argv[2])
			
	else:
		print "Syntex : \n\t%s d/e file" % sys.argv[0]

