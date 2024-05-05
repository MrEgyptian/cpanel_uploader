#!/bin/env python3
# Ver: 0.1
# By : @MrEgyptian
# GitHub :Github.com/MrEgyptian
# Website : https://www.MrEgyptian.codes
# Contact : Me@MrEgyptian.com
########################################################################
#
from pygments import highlight, lexers, formatters
import requests,json
import colorama
import base64
from requests.auth import HTTPBasicAuth
from configparser import ConfigParser as cp
parser=cp()
red=colorama.Fore.RED
green=colorama.Fore.GREEN
blue=colorama.Fore.BLUE
yellow=colorama.Fore.YELLOW

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
  self.url = f"https://{hostname}:{port}/json-api/cpanel";
  self.session=requests.Session()
  self.auth=HTTPBasicAuth(username,password)
  r=self.session.get(self.url,auth=self.auth,json=params)
  if(r.status_code==403):
   raise invalidCreds
  if(r.status_code==200):
   pass
 def getFile(self,name):
  f=open(name,'r')
  content=f.read()
  f.close()
  return name,content
 def upload(self,path,rootDir="public_html",dir=""):
  fileName,fileContent=self.getFile(path)
  self.uploadFile(fileName,fileContent,rootDir=rootDir,dir=dir)
  pass
 def uploadFile(self,fileName,fileContent,rootDir="public_html",dir="ze"):
  params={
  "api.version":"2",
  "cpanel_jsonapi_module":"Fileman",
  "cpanel_jsonapi_func":"uploadfiles",
  "dir":f"{rootDir}/{dir}",
  }
  f={
  "file":[fileName,fileContent]
  }

  r=self.session.post(self.url,auth=self.auth,data=params,files=f)
  status=r.status_code
  obj=r.json()['cpanelresult']['data']
  json_str=json.dumps(obj,indent=4)
  hi= highlight(json_str,
    lexers.JsonLexer(),
    formatters.TerminalFormatter()
    )
  print(green,r.status_code,hi)
  pass
def rmComment(stringo):
 stringo=str(stringo).strip('\n')
 if(str(stringo).startswith('#')):
  pass
 else:
  return str(stringo).split(':')
def readList(list_name):
 f=open(list_name)
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
    api=CPanelAPI(hostname=host,port=int(port),username=user,password=password)
    print(f'{green}Logged in Successfully')
    return api
   except Exception as e:
    print('{red} Error While Logging in ',e)
   return False
def get_file_input(disp_text,error_text='invalid file name : '):
 global red
 print(disp_text,end='')
 file=input()
 try:
  x=open(file)
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
 listFile=get_file_input(f'{green}CPanels >{yellow} ')
 uploadFile=get_file_input(f'{green}UPLOAD FILE >{yellow} ')
 cpanel_list=readList(listFile) 
 print(f'Reading list {blue}[{green}{listFile}{blue}]')
 for item in cpanel_list:
  try:
   host,port,user,password=item
   print(f"{yellow}Connecting to {blue}https://{host}:{port}")
   api=login(*item)
   if(api!=False):
    print(f"{yellow}Uploading {blue}{uploadFile}")
    api.upload(uploadFile)
  except Exception as e:
   print(f'invalid syntax in {":".join(item)}',e)
  #api=CPanelAPI()
 #api.uploadFile('kaka.html',"<center>PePe</center>")

