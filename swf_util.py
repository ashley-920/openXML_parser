import os, zipfile, subprocess as sub

file_path="C:\\Users\\Ash\\Desktop\\swf\\activeX1.swf"
des_text_path="C:\\Users\\Ash\\Desktop\\action_result.txt"
mod_dir= "\\prog\\swftools\\swfdump.exe"




def extract_actionscript(file_path,des_text_path):
	#print os.path.dirname(__file__)
	# print file_path
	# print des_text_path
	prog_swftools = os.path.dirname(__file__)+mod_dir
	#print prog_swftools
	# des_text_path=des_text_path.replace(" ", "_")
	test_command="\""+prog_swftools+"\" -a \""+file_path+"\" > \""+des_text_path+"\""
	# test_command="\""+prog_swftools+"\" -a \""+file_path+"\""

	# print test_command
	print 'ActionScript file location:'
	print  '*%s' % (des_text_path)
	sub.Popen(test_command,shell=True, stdout=sub.PIPE, stderr=sub.STDOUT)
	# os.system(str(test_command))

if __name__ == '__main__':
	extract_actionscript(file_path, des_text_path)