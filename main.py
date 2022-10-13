#!/bin/env python3
# Ver: 0.1
# By : @MrEgyptian
# GitHub :Github.com/MrEgyptian
# Website : https://www.MrEgyptian.codes
# Contact : Me@MrEgyptian.com
########################################################################
#
#
# https://jossjt1.websitewelcome.com:2083/
# fortest8471
# ForTest#@ForTest#@
# 

#https://hostname.example.com:2087/cpsess##########/json-api/cpanel?cpanel_jsonapi_user=user&cpanel_jsonapi_apiversion=2&cpanel_jsonapi_module=Ftp&cpanel_jsonapi_func=listftp

import requests
import base64
from requests.auth import HTTPBasicAuth
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
  url = f"https://{hostname}:{port}/json-api/cpanel";
  #auth = HTTPBasicAuth(
  #base64.b64encode(username.encode()).decode()
  #, base64.b64encode(password.encode()).decode()
  #)
  #https://hostname.example.com:2087/cpsess##########/json-api/cpanel?
  #cpanel_jsonapi_user=user&cpanel_jsonapi_apiversion=2&
  #cpanel_jsonapi_module=Fileman&cpanel_jsonapi_func=listfiles&checkleaf=1&dir=%2Fhome%2Fuser&filelist=1&filepath=filelist-A&needmime=1&showdotfiles=1&types=dir%20%7C%20file
  #cpanel_jsonapi_user=user&cpanel_jsonapi_apiversion=2&cpanel_jsonapi_module=Module&cpanel_jsonapi_func=function&parameter="value"
  auth=HTTPBasicAuth(username,password)
  r=requests.get(url,auth=auth,json=params)
  print(r.status_code,r.json())
  pass
CPanelAPI()
