openXML_parser
==============

This is an parser which can parse openXML file and detect malicious content.
NOTICE: It's still under development.

command:

-a [file_path]                          => analysis file
-pct [file_path]                        => print [Content_Types].xml
-pdir [file_path]                       => print unzip dir
-pvml [file_path]                       => print vmlDrawing.xml info
-pfc [file_path] [file_name]            => print file content
-g [file_path] [file_name] [tag_name]   => get specific value of specific tag from specific file
-e [file_path] [dest_dir_path]          => extrace swf files from the file path and extract actionsc
ript of the swf files to txt file
