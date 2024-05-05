#!/bin/env python3
# Ver: 0.1.1
# By : @MrEgyptian
# GitHub :Github.com/MrEgyptian
# Website : https://www.MrEgyptian.codes
# Contact : Me@MrEgyptian.com
########################################################################
#
from pygments import highlight, lexers, formatters
import requests,json,sys
import colorama
import base64,re
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser as cp
parser=cp()
red=colorama.Fore.RED
green=colorama.Fore.GREEN
blue=colorama.Fore.BLUE
yellow=colorama.Fore.YELLOW
cyan=colorama.Fore.CYAN
class invalidCreds(Exception):
 '''Invalid Username or Password'''
class CPanelAPI:
 def __init__(self,hostname='jossjt1.websitewelcome.com',
  port=2083,
  username='fortest8471',
  password='ForTest#@ForTest#@'
  ):
  params={
  "api.version":"1",
  "cpanel_jsonapi_module":"Fileman",
  "cpanel_jsonapi_func":"listfiles"
  }
  self.url = f"{hostname}:{port}/json-api/cpanel";
  self.session=requests.Session()
  self.user=username
  self.auth=HTTPBasicAuth(username,password)
  r=self.session.get(self.url,auth=self.auth,json=params)
  if(r.status_code==403):
   raise invalidCreds
  if(r.status_code==200):
   pass
 def getFile(self,name):
  f=open(name,'r',encoding='utf-8')
  content=f.read()
  f.close()
  return name,content
 def upload(self,path,rootDir="public_html",dir=""):
  fileName,fileContent=self.getFile(path)
  #Adding return Value to handle Exceptions ^^
  return self.uploadFile(fileName,fileContent,rootDir=rootDir,dir=dir)
 def delFile(self,filePath,rootDir='public_html',dir=''):
  #After testing 'overwrite' parameter it wasn't stable so i used Fileop API
  params={
    "api.version":"2",
    "cpanel_jsonapi_module":"Fileman",
    "cpanel_jsonapi_func":"fileop",
    "op":'trash',
    "sourcefiles":f"{rootDir}/{dir}/{filePath}"
    }
  r2=self.session.post(self.url,auth=self.auth,data=params)
  res=r2.json()['cpanelresult']['event']['result']
  #Returns :)
  if(res==1):
   return res
  else:
   return r2.json()['cpanelresult']['error'] #The Expected errors are OS Errors
 def getDomains(self,):
  params={
    "cpanel_jsonapi_module":"DomainLookup",
    "cpanel_jsonapi_func":"getbasedomains",
    "api.version":"2",
  }
  #domain_url=self.url.replace('cpanel','get_domain_info')
  r=self.session.post(self.url,auth=self.auth,data=params)
  return r.json()['cpanelresult']['data']
 def uploadFile(self,fileName,fileContent,rootDir="public_html",dir="ze"):
  uploadParams={
  "api.version":"2",
  "cpanel_jsonapi_module":"Fileman",
  "cpanel_jsonapi_func":"uploadfiles",
  "dir":f"{rootDir}/{dir}",
  }
  f={
  "file":[fileName,fileContent]
  }

  r=self.session.post(self.url,auth=self.auth,data=uploadParams,files=f)
  status=r.status_code
  obj=r.json()['cpanelresult']['data']
  json_str=json.dumps(obj,indent=4)
  hi= highlight(json_str,
    lexers.JsonLexer(),
    formatters.TerminalFormatter()
    )
  print(green,r.status_code,hi)
  return obj[0]['uploads'][0]['reason']
def rmComment(stringo):
 stringo=str(stringo).strip('\n')
 if(str(stringo).startswith('#')):
  pass
 else:
  #return str(stringo).split(':')
  return str(stringo)
def readList(list_name):
 f=open(list_name,encoding='utf-8')
 lines=f.readlines()
 f.close()
 lines=map(rmComment,lines)
 lines=[line for line in lines if line!=None]
 lines=list(lines)
 return lines
def login(host,port,user,password):
   global green,blue,red,yellow
   try:
    print(f"{yellow}Logging in as {blue}{user}")
    #host=host.replace('http://','')
    #host=host.replace('https://','')
    api=CPanelAPI(hostname=host,port=int(port),username=user,password=password)
    print(f'{green}Logged in Successfully')
    return api
   except Exception as e:
    print(f'{red} Error While Logging in ',e)
   return False

def save_domain(domain,domain_list='domains.txt'):
 f=open(domain_list,'a+',encoding='utf-8')
 f.write(domain)
 f.close()
 return True

def get_file_input(disp_text,error_text='invalid file name : '):
 global red
 print(disp_text,end='')
 file=input()
 try:
  x=open(file,encoding='utf-8')
  x.close()
  return file
 except:
  print(red,error_text,file)
  return get_file_input(disp_text,error_text=error_text)
if __name__=='__main__':
 # Some Testing creds
 # https://jossjt1.websitewelcome.com:2083/
 # fortest8471
 # ForTest#@ForTest#@
 #
 colorama.init()
 parser.read('config.ini')
 credsPattern = parser.get('lists','pattern')
 hostPattern='https?://[a-zA-Z0-9_.]+'
 portPattern='\d+'
 userPattern='[a-zA-Z0-9_.]+'
 passPattern='.*'
 credsRegex=credsPattern.replace('host',f'({hostPattern})')
 credsRegex=credsRegex.replace('|',r'\|')
 credsRegex=credsRegex.replace('port',f'({portPattern})')
 credsRegex=credsRegex.replace('user',f'({userPattern})')
 credsRegex=credsRegex.replace('password',f'({passPattern})')
 listPrompt=parser.getboolean('lists','list_prompt')
 if(listPrompt):
  listFile=get_file_input(f'{green}CPanels >{yellow} ')
  uploadFile=get_file_input(f'{green}UPLOAD FILE >{yellow} ')
  domainsFile=get_file_input(f'{green}output >{yellow} ')
 else:
  listFile=parser.get('list_prompt','list_file')
  uploadFile=parser.get('list_prompt','upload_file')
  domainsFile=parser.get('list_prompt','domains_file')
 cpanel_list=readList(listFile)
 #print(cpanel_list)
 print(f'Reading list {blue}[{green}{listFile}{blue}]')
 for item in cpanel_list:
  try:
   match=re.match(credsRegex,item)
   #print(item)
   #print(credsRegex)
   host=match.group(1)
   port=match.group(2)
   user=match.group(3)
   password=match.group(4)
   #host,port,user,password=item
   print(f"{yellow}Connecting to {blue}{host}:{port}")
   #API Login
   api=login(host,port,user,password)
   if(api!=False):
    #after Login
    domains=api.getDomains()
    domain=domains[0]['domain']
    print(f"{yellow}Uploading {blue}{uploadFile}")
    upload_res=api.upload(uploadFile)
    save_domain("http://"+domain+'/'+uploadFile+'\n',domainsFile)
    if('already exists' in upload_res):
      # Upload Handler
      print(f'{red} The file is already exists.')
      #
      print(f'{cyan}Deleting the old file: {green}{uploadFile}')
      delRes=api.delFile(uploadFile)
      #Del Result
      if(delRes==1):
       print(f'{cyan}File Deleted.')
       print(f'{yellow}Uploading The File again..')
       upload_res=api.upload(uploadFile)
       print(green,upload_res.replace(uploadFile,cyan+uploadFile+green))
       #End Of code :)
      else:
       #If File Not Exists
       pass
      print(f'{green}GoodBye{yellow}.')
    else:
       #
       #Deleting file error (You can raise an exception here )
       #
       print(f"Failed while deleting file error Code:{delRes}")
    print(f'{green}Uploaded to',yellow,"http://"+domain+'/'+uploadFile)
  except Exception as e:
   #print(f'invalid syntax in {":".join(item)}',e)
   exc_type, exc_obj, exc_tb = sys.exc_info()
   print(exc_tb.tb_lineno)
  #api=CPanelAPI()
 #api.uploadFile('kaka.html',"<center>PePe</center>")

