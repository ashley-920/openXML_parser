import zipfile, xmltodict, json, dpath.util, os, re, sys, traceback
from modules.docx_extract_swf import flash as flash
#from swf.movie import SWF
import swf_util

#from lxml import etree
#import xml.etree.ElementTree as etree

flash_match=0
listview_match=0
des_path=''
dir_path=''


def load_des_path():    
    global des_path
    config_path=os.path.join(os.path.dirname(__file__), "config.txt")
    f=open(config_path,"r")
    path=f.read()
    path=path.split("=")
    des_path=path[-1]
    return des_path


def analysis_File(file_path):
    #print(file_path)
    #if zipfile.is_zipfile(file_path) and check_File_Type(get_File_Type(file_path)):  
    global des_path
    load_des_path()
    if zipfile.is_zipfile(file_path):
        extract_file(file_path)
        filetype=get_File_Type(file_path)
        print_File_info(file_path)
        printTitle("Dir Info")        
        file_list=get_file_dir(file_path)
        for filename in file_list:
            print ' *'+filename
        printContentTypeInfo(file_path)
        
        # printReport(file_path)
        if filetype == 'PPTX' or filetype == 'XLSX':
            check_vml_info(file_path)
        elif filetype == 'DOCX':
            check_doc_info(file_path)
        if getActiveXInfo(file_path) or flash_match >0:
            process_flash(file_path, des_path)
        printTitle("VBA Info")
        vba_result=check_VBA_info(file_path)
        if vba_result != None:
            print "This file contain VBA file. path: %s" % (vba_result)
            extract_vba_script(file_path)
        else:
            print "This file contain No VBA file"        
    else:
        print("File doesnt exsist or cannot be analysis")


def check_File_Type(file_type):
    suffix={"DOCX","PPTX","XLSX"}        
    if file_type in suffix:                      
        return True
    else:
        return False
    


def get_File_Type(file_path):
    file_list=get_file_dir(file_path)
    filetype='unknown'
    for filename in file_list:
        #print "************************"+filename
        if "word/document.xml" in filename:
            filetype = 'DOCX'
        elif "xl/workbook.xml" in filename:
            filetype = 'XLSX'
        elif "ppt/presentation.xml" in filename:
            filetype = 'PPTX'
    return filetype;
    

def print_File_info(file_path):
    printTitle("File info")
    file_type=get_File_Type(file_path)
    file_size=os.path.getsize(file_path)
    print "File Type: ",file_type
    print "File Path: ",file_path
    print "File size: %s KB" % (file_size)
    return {file_path, file_type, file_size}
 
def printReport(file_path):
    print_File_info(file_path)
    printTitle("Dir Info")
    file_list=get_file_dir(file_path)
    for filename in file_list:
        print filename
    printContentTypeInfo(file_path)
    getActiveXInfo(file_path)
    check_vml_info(file_path)

        #printContentTypeInfo()

def get_file_dir(file_path):    
    dfile=zipfile.ZipFile(file_path,'r')
    #file_dir_list=dfile.infolist()            
    return dfile.namelist()

def getActiveXInfo(file_path):    
    printTitle("ActiveX Info")    
    found=False
    dfile=zipfile.ZipFile(file_path,'r')
    file_dir_list=dfile.infolist()
    for item in file_dir_list:
        filename=item.filename
        if "activeX" in filename:
            if not found:
                found=True
                file_contain_activeX=True
            print "File: ",filename
    if not found: print("This File Contain No ActiveX related file")
    return found
       

def check_vml_info(file_path):
    #dir_name={"docx":"word","xlsx":"xl","pptx":"ppt"}
    global flash_match
    global listview_match
    printTitle("vml Info")
    vml_path_pattern=r"/drawings/vmlDrawing[(0-9)+].vml"
    real_vml_path=list()
    flash_string="ShockwaveFlash"
    listview_string="ListView"
    dfile=zipfile.ZipFile(file_path,'r')
    file_dir_list=dfile.infolist()
    for dir_path in file_dir_list:
        if re.search(vml_path_pattern,dir_path.filename)!=None:
            real_vml_path.append(dir_path.filename)
                #printFileContent(vml_path)            
    #print(real_vml_path)
    if len(real_vml_path)>0:
        for path in real_vml_path:
            content=parseFile(file_path,path)
            flash_result=re.findall(flash_string,json.dumps(content, indent=4))
            flash_match+=len(flash_result)
            print(path+" find "+str(len(flash_result))+" flash string match")
            listview_result=re.findall(listview_string,json.dumps(content, indent=4))
            listview_match+=len(listview_result)
            print(path+" find "+str(len(listview_result))+" ListView string match")
        print("Total flash match:"+str(flash_match))
        print("Total ListView match:"+str(listview_match))
    else:
        print("No vmlDrawing.xml file")

def check_doc_info(file_path):
    global flash_match
    printTitle("document.xml Info")
    doc_path=r"word/document.xml"
    flash_string="ShockwaveFlash"
    content=parseFile(file_path,doc_path)
    flash_result=re.findall(flash_string,json.dumps(content, indent=4))
    flash_match+=len(flash_result)
    print(doc_path+" find "+str(len(flash_result))+" flash string match")


def check_VBA_info(file_path):    
    vba_file='vbaProject.bin'
    found=None
    file_list=get_file_dir(file_path)
    for filename in file_list:
        if filename.endswith(vba_file):
            found=filename
            break    
    return found

def printFileContent(file_path,file_name):
    printTitle("Content of File:"+file_name)
    content=parseFile(file_path,file_name)
    print(json.dumps(content, indent=4))

def printTitle(title):
    x=len(title)
    y=int((80-x)/2)
    line=""        
    for i in range(0,y):
        line+="="
    line+=title
    for i in range(0,y):
        line+="="
    print(line)
       

def parseFile(file_path,file_name):
    try:
        remove_pattern=r"<!\[(\w+)\]>"
        remove_pattern2=r"<!\[(\w+\s\w+\s\w+\s\w+)\]>"
        file_path=file_path
        dfile=zipfile.ZipFile(file_path,'r')
        data= dfile.read(file_name)
        data=re.sub(remove_pattern,"", data.decode("utf-8"))
        data=re.sub(remove_pattern2,"", data)
            #print("data:",data)   
        dictionary=xmltodict.parse(data)  
            #dfile.close()
        return dictionary
    except:
        print("Read file Error")
        print(traceback.format_exc())
    else:
        pass
    finally:
        pass


def printContentTypeInfo(file_path):
    printTitle("Content_Type.xml Summary")    
    content_type_file_path=r"[Content_Types].xml"
    activeX_contentType="application/vnd.ms-office.activeX+xml"
    activeX_extension="bin"
    activeX_List=list()
    exten_List=list()
    content=parseFile(file_path,content_type_file_path)    
    """
    check Override attri 
    #json=>content['Types']['Override'][0]['@PartName']    
    """
    print("[Check ActiveX related file type]:")
    print(" files with Override type 'application/vnd.ms-office.activeX+xml':")
    for attri in content['Types']['Override']:
        if attri['@ContentType']==activeX_contentType:            
            activeX_List.append(attri['@PartName'])
    for item in activeX_List:
        print(" *"+item)

    """
    check Default attri
    #json=>content['Types']['Default'][0]['@Extension']    
    """
    flag=False
    for attri in content['Types']['Default']:
        if attri['@ContentType']==activeX_contentType:            
            flag=True
        exten_List.append(attri['@Extension'])
    if flag:
        print(" file contain ActiveX default file type")
    print("[Extension List]:")
    for item in exten_List:
        print(" *"+item)

def getValue(file_path,file_name,tag_name):
    content=parseFile(file_path,file_name)   
    result=dpath.util.search(dict(content),tag_name)
    printTitle("value of tag: \'"+tag_name+"\', in file: \'"+file_name+"\'")
    print(json.dumps(result, indent=4)) 


def process_flash(file_path, des_file_path):
    #flash.process_file(file_path, des_file_path)
    global des_path
    if des_file_path == None:
        des_file_path=load_des_path()
    # print des_file_path
    printTitle("Process flash")    
    file_name=os.path.basename(file_path)
    #print file_name
    if zipfile.is_zipfile(file_path):
        if check_File_Type(get_File_Type(file_path)):
            name=flash.process_file(file_path,des_file_path)            
            if len(name)<1:
                print "Cannot find swf in bin file"
            else: 
                print 'Extract %s swf file to:' % (len(name)) 
                for swf in name:
                    print '*%s' % (swf)
                    swf_util.extract_actionscript(swf,swf+".txt")
    elif flash.detect_swf(file_path):
        swf_util.extract_actionscript(file_path,des_file_path+"\\"+file_name+".txt")
    else:
        print "This file cannot be process"   

    #swf_util.extract_actionscript("D:\\tmp\\flash2.pptx_FWS_00000C08","D:\\open_xml\\flash2.txt")
    # _file = open(r'C:\Users\Ash\Desktop\swf\twist.swf', 'rb')
    # print SWF(_file)
def extract_file(file_path):
    global des_path
    global dir_path
    if des_path==None:
        des_path=load_des_path()
    file_name=os.path.basename(file_path) 
    # des_path=os.path.join(os.path.dirname(file_path),file_name+"_files")
    dir_path=os.path.join(des_path,file_name+"_files")
    if not os.path.exists(des_path) or not os.path.isdir(des_path):
            os.makedirs(dir_path)
    #print des_dir;
    if zipfile.is_zipfile(file_path):
        dfile=zipfile.ZipFile(file_path,'r')        
        dfile.extractall(dir_path)
        print "Extract "+file_name+" to: "+dir_path+" Successfully"
    return dir_path


def extract_vba_script(file_path):
    vba_path=check_VBA_info(file_path);
    if vba_path!= None:
        #print vba_path
        ex_path=extract_file(file_path)
        vba_path=ex_path+'\\'+vba_path.replace('/','\\')
        #print vba_path
        officeMalscanner_path = os.path.join(os.path.dirname(__file__), '\prog\OfficeMalScanner\officeMalscanner.exe')
        #print officeMalscanner_path;
        command='.'+officeMalscanner_path+" "+vba_path+" info"
        #print command
        content = ''.join(os.popen(command).readlines())
        print content

    


if __name__ == '__main__':  # pragma: no cover

    # file_path=r'C:\Users\Ash\Desktop\testFile.docx'     #no activeX
    # file_path2=r'C:\Users\Ash\Desktop\file2.zip'        #malware activeX file
    # file_path3=r"C:\Users\Ash\AppData\Roaming\Spotify"  #not zip file
    # file_path4=r"C:\Users\Ash\Desktop\flash.pptx"       #pptx contain 1 flash
    # file_name=r"file/ppt/activeX/activeX2.xml"
    # file_name2=r"word/document.xml"
    # file_name3=r"file/[Content_Types].xml"
    # file_name4=r"[Content_Types].xml"
    print "\n+------------------------------------------+\n",
    print "|           Open_xml Parser v1.0           |\n",
    #print "|                                          |\n",
    print "+------------------------------------------+\n",
    if len(sys.argv)>2:
        if sys.argv[1] == "-a":
            if len(sys.argv) == 3:
                analysis_File(sys.argv[2])
            else:
                print("-a [file_path]                          => analysis file")
        elif(sys.argv[1] == "-pfc") :
            if len(sys.argv) == 4:
                printFileContent(sys.argv[2], sys.argv[3])
            else:
                print("-pfc [file_path] [file_name]            => print file content")
        elif(sys.argv[1] == "-g") :
            if len(sys.argv) == 5:
                getValue(sys.argv[2], sys.argv[3], sys.argv[4])
            else:
                print("-g [file_path] [file_name] [tag_name]   => get specific value of specific tag from specific file")
        elif(sys.argv[1] == "-pct") :
            if len(sys.argv) == 3:
                printContentTypeInfo(sys.argv[2])
            else:
                print("-pct [file_path]                        => print [Content_Types].xml")
        elif(sys.argv[1] == "-pdir") :
            if len(sys.argv) == 3:
                name_list=get_file_dir(sys.argv[2])
                for name in name_list:
                    print name;  
            else:
                print("-pdir [file_path]                       => print unzip dir")
        elif(sys.argv[1] == "-pvml") :
            if len(sys.argv) == 3:
                check_vml_info(sys.argv[2])
            else:
                print("-pvml [file_path]                       => print vmlDrawing.xml info")
        elif(sys.argv[1] == "-e") :
            if len(sys.argv) == 4 :                
                process_flash(sys.argv[2],sys.argv[3])                   
            elif len(sys.argv)==3:
                process_flash(sys.argv[2],None)
            else:
                print("-e [file_path] [dest_dir_path (optional)]          => extrace swf files from the file path and extract actionscript of the swf files to txt file")
        else:
            print("-a [file_path]                          => analysis file")
            print("-pct [file_path]                        => print [Content_Types].xml")
            print("-pdir [file_path]                       => print unzip dir")
            print("-pvml [file_path]                       => print vmlDrawing.xml info")
            print("-pfc [file_path] [file_name]            => print file content")
            print("-g [file_path] [file_name] [tag_name]   => get specific value of specific tag from specific file")
            print("-e [file_path] [dest_dir_path (optional)]          => extrace swf files from the file path and extract actionscript of the swf files to txt file")
    else:
        print("-a [file_path]                          => analysis file")
        print("-pct [file_path]                        => print [Content_Types].xml")
        print("-pdir [file_path]                       => print unzip dir")
        print("-pvml [file_path]                       => print vmlDrawing.xml info")
        print("-pfc [file_path] [file_name]            => print file content")
        print("-g [file_path] [file_name] [tag_name]   => get specific value of specific tag from specific file")
        print("-e [file_path] [dest_dir_path (optional)]          => extrace swf files from the file path and extract actionscript of the swf files to txt file")
    #process_flash("D:\\open_xml\\flash2.pptx","D:\\tmp")
    
    # file_parser.analysis_File(file_path4)    
    # file_parser.printFileContent(file_name4)            #print specific file's content
    # file_parser.getValue(file_name4,"Types/Default")    #get specific tag from specific file
    
    #print(file_parser.file_path)
    
    

        
            
    











