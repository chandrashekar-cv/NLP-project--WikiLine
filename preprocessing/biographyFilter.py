
import os,re
import xml.etree.cElementTree as ET


class netagger:
    def __init__(self,nerModelPath,outputPath,indexer):
        #self.netag = NERTagger(nerModelPath)
        self.outputPath = outputPath
        self.indexer=indexer
        self.cat_re = re.compile('^__Category:(.*?)__$')
        self.url_re = re.compile('<doc .* url="(.*)" title.*>',)
        self.id_re = re.compile('<doc id="([0-9]*)" .*>')

    '''    def classifyDoc(self,title):
        data = self.netag.tag(title.split())
        
        for row in data:
            for tag in row:
                if not(tag[1]=="PERSON"):
                    return False
        return True
    
    '''    
    def parseFiles(self,path):
        files = os.listdir(path)
        for file in files:
            if not(file=="desktop.ini"):
                if(os.path.isdir(path+file)):
                    self.parseFiles(path+file)
                else:
                    if(not path.endswith("/")):
                        path+="/"
                    self.get_content(open(path+file,'r',encoding="ISO-8859-1"))
                    
            
    
    def get_content(self,file):
        lines = file.readlines()
        docStart= False
        firstLine = False
        live_cat_found = False
        articleContent=""
        url=""
        docIndex =""
        categories=[]
        for line in lines:
            line=line.strip()
            if(not docStart and re.match("^<doc.*>$",line)):
                docStart= True
                firstLine=True
                m = self.url_re.match(line)
                url=m.group(1)
                m = self.id_re.match(line)
                docIndex = m.group(1)
                continue
            
            if(docStart and firstLine):
                title = line
                firstLine=False
            '''    if not(self.classifyDoc(title)):
                    docStart=False
            '''    
            if(docStart and re.match("^</doc.*>$", line)):
                docStart=False
                if live_cat_found:
                    self.printToFile(articleContent,categories,title,url,docIndex)
                articleContent=""
                categories=[]
                live_cat_found = False
                url=""
                docIndex=""
            elif(docStart):
                m = self.cat_re.match(line)
                if m is not None:
                    category = m.group(1).strip()
                    if category == "Living people" or re.match("^.* death[s]$", category):
                        live_cat_found = True
                    categories.append(category)
                else:
                    articleContent+= line
        
    def printToFile(self,content,categories,title,url,docIndex):
        root = ET.Element("DOC")
        
        ET.SubElement(root,"DOC-ID").text = title
        ET.SubElement(root,"TEXT").text = content
        cat_list= ET.Element("CATEGORIES")
        for name in categories:
            ET.SubElement(cat_list,"CATEGORY").text=name
        
        root.append(cat_list)
        ET.SubElement(root,"URL").text=url
        ET.SubElement(root,"DOC-INDEX").text=docIndex
        
        filename=re.sub('[*]|\?|/|<|>|:|"|\|',"_",title)
        print(str(tagger.indexer))
        with open(self.outputPath+filename+".xml", mode='wb') as outputfile:
            outputfile.write(ET.tostring(root, encoding="ISO-8859-1", method="xml"))
        self.indexer+=1

tagger = netagger('english.all.3class.distsim.crf.ser.gz','output/',1)
tagger.parseFiles('F:/pythonWorkspace/wikiextractor/src/extracted/')
print(str(tagger.indexer))    