import zipfile, xmltodict, json, dpath.util, os, re, sys, traceback

#from lxml import etree
#import xml.etree.ElementTree as etree

class Parser(object):   

    def __init__(self,dfile=None,file_path=None,file_type=None,file_dir_list=None,contain_activeX=False,contain_flash=False):
        self.dfile=dfile
        self.file_path=file_path
        self.file_type=file_type
        self.file_dir_list=file_dir_list
        self.file_contain_activeX=contain_activeX
        self.file_contain_flash=contain_flash


    def analysis_File(self,file_path):
        self.file_path=file_path
        print(file_path)
        if(zipfile.is_zipfile(self.file_path) and self.check_File_Type()):
            self.dfile=zipfile.ZipFile(self.file_path,'r')
            self.file_dir_list=self.dfile.infolist()
            self.printReport()
        else:
            print("This file can not be analysis")

    def check_File_Type(self):        
        suffix={"docx","pptx","xlsx","zip"}
        extension = os.path.splitext(self.file_path)[-1].lstrip('.')
        self.file_type=extension
        if extension in suffix:
            #print(extension)            
            return True
        else:
            return False

    def print_File_info(self):
        self.printTitle("File info")
        print("File Type:",self.file_type)
        print("File Path:",self.file_path)
 
    def printReport(self):
        self.print_File_info()
        self.printDir()
        self.printContentTypeInfo()
        self.printActiveXInfo()
        if(self.file_contain_activeX):
            self.print_vml_info()

        #self.printContentTypeInfo()

    def printDir(self):    
        self.printTitle("Dir Info")        
        self.dfile.printdir() 

    def printActiveXInfo(self):    
        self.printTitle("ActiveX Info")    
        found=False
        for item in self.file_dir_list:
            filename=item.filename
            if "activeX" in filename:
                if not found:
                    found=True
                    self.file_contain_activeX=True
                print("File:",filename)
        if not found: print("This File Contain No ActiveX related file")
        #print(self.file_contain_activeX)

    def print_vml_info(self):
        #dir_name={"docx":"word","xlsx":"xl","pptx":"ppt"}
        self.printTitle("vml Info")
        vml_path="/drawings/vmlDrawing1.vml"
        flash_string="ShockwaveFlash"
        listview_string="ListView"
        #print(vml_path)
        for dir_path in self.file_dir_list:
            if dir_path.filename.endswith(vml_path):
                vml_path=dir_path.filename
                #self.printFileContent(vml_path)
                break
        content=self.parseFile(self.file_path,vml_path)
        flash_result=re.findall(flash_string,json.dumps(content, indent=4))
        print("*vmlDrawing.xml find "+str(len(flash_result))+" flash string match")
        listview_result=re.findall(listview_string,json.dumps(content, indent=4))
        print("*vmlDrawing.xml find "+str(len(listview_result))+" ListView string match")


    def printFileContent(self,file_path,file_name):
        self.printTitle("Content of File:"+file_name)
        content=self.parseFile(file_path,file_name)
        print(json.dumps(content, indent=4))

    def printTitle(self,title):
        x=len(title)
        y=int((80-x)/2)
        line=""        
        for i in range(0,y):
            line+="="
        line+=title
        for i in range(0,y):
            line+="="
        print(line)
        #print("=============================%s================================"%title)

    def parseFile(self,file_path,file_name):
        try:
            remove_pattern=r"<!\[(\w+)\]>"
            remove_pattern2=r"<!\[(\w+\s\w+\s\w+\s\w+)\]>"
            self.file_path=file_path
            self.dfile=zipfile.ZipFile(self.file_path,'r')
            data= self.dfile.read(file_name)
            data=re.sub(remove_pattern,"", data.decode("utf-8"))
            data=re.sub(remove_pattern2,"", data)
            #print("data:",data)   
            dictionary=xmltodict.parse(data)  
            #self.dfile.close()
            return dictionary
        except:
            print("Read file Error")
            print(traceback.format_exc())
        else:
            pass
        finally:
            pass


    def printContentTypeInfo(self):
        self.printTitle("Content_Type.xml Summary")    
        content_type_file_path=r"[Content_Types].xml"
        activeX_contentType="application/vnd.ms-office.activeX+xml"
        activeX_extension="bin"
        activeX_List=list()
        exten_List=list()
        content=self.parseFile(self.file_path,content_type_file_path)    
        """
        check Override attri 
        #json=>content['Types']['Override'][0]['@PartName']    
        """
        print("[Check ActiveX related file type]:")
        print("files with Override type 'application/vnd.ms-office.activeX+xml':")
        for attri in content['Types']['Override']:
            if attri['@ContentType']==activeX_contentType:            
                activeX_List.append(attri['@PartName'])
        for item in activeX_List:
            print("*"+item)

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
            print("file contain ActiveX default file type")
        print("[Extension List]:")
        for item in exten_List:
            print("*"+item)

    def getValue(self,file_path,file_name,tag_name):
        test_dic={"a": {"b": {"c": [],"d": ["red","buggy","bumpers"]}}}
        content=self.parseFile(file_path,file_name)  
    #printFileContent(file_path,file_name)
        result=dpath.util.search(dict(content),"Types/Default")
    #result=dpath.util.search(test_dic,"[abcdefghijklmnopqrstuvwxyz]")
        self.printTitle("value of tag: \'"+tag_name+"\', in file: \'"+file_name+"\'")
        print(json.dumps(result, indent=4)) 
    #return result
    # for root, tag1 in content.items():
    #     if tag_name in tag1:
    #         print(json.dumps(tag1[tag_name], indent=4))
    #     #print(json.dumps(types, indent=4))
    #print(json.dumps(content['Types']['Override'][0]['@PartName'], indent=4))
           
    
    


if __name__ == '__main__':  # pragma: no cover
    import xmltodict
    from Parser import Parser

    file_path=r'C:\Users\Ash\Desktop\testFile.docx'     #no activeX
    file_path2=r'C:\Users\Ash\Desktop\file2.zip'        #malware activeX file
    file_path3=r"C:\Users\Ash\AppData\Roaming\Spotify"  #not zip file
    file_path4=r"C:\Users\Ash\Desktop\flash.pptx"       #pptx contain 1 flash
    file_name=r"file/ppt/activeX/activeX2.xml"
    file_name2=r"word/document.xml"
    file_name3=r"file/[Content_Types].xml"
    file_name4=r"[Content_Types].xml"
    """
    test start
    """
    file_parser=Parser()
    if len(sys.argv)>2:
        if sys.argv[1] == "-a":
            file_parser.analysis_File(sys.argv[2])
        else:
            if(sys.argv[1] == "-p") :
                if len(sys.argv) == 4:
                    file_parser.printFileContent(sys.argv[2], sys.argv[3])
                else:
                    print("-p [file_path] [file_name] => print file content")
            if(sys.argv[1] == "-g") :
                if len(sys.argv) == 5:
                    file_parser.getValue(sys.argv[2], sys.argv[3], sys.argv[4])
                else:
                    print("-g [file_path] [file_name] [tag_name] => get specific value of specific tag from specific file")

    else:
        print("-a [file_path] => analysis file")
        print("-p [file_path] [file_name] => print file content")
        print("-g [file_path] [file_name] [tag_name] => get specific value of specific tag from specific file")

    
    # file_parser.analysis_File(file_path4)    
    # file_parser.printFileContent(file_name4)            #print specific file's content
    # file_parser.getValue(file_name4,"Types/Default")    #get specific tag from specific file
    
    #print(file_parser.file_path)
    
    

        
            
    











