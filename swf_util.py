import os

file_path="C:\\Users\\Ash\\Desktop\\swf\\activeX1.swf"
des_text_path="C:\\Users\\Ash\\Desktop\\action_result.txt"
mod_dir= "\\prog\\swftools\\swfdump.exe"


#print prog_swftools

def extract_actionscript(file_path,des_text_path):
	#print os.path.dirname(__file__)
	prog_swftools = os.path.dirname(__file__)+mod_dir
	#print prog_swftools
	test_command=prog_swftools+" -a "+file_path+" > "+des_text_path
	print 'actionscript file location: %s' % (des_text_path)
	os.popen(test_command)

if __name__ == '__main__':
	extract_actionscript(file_path, des_text_path)