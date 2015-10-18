import math
import tkinter
import requests
import xml.etree.ElementTree as ET
import dateutil.parser
import sugarsync


_config = {
    'ApplicationName': 'SugarSyncLinux',
    'Version': '0.1',
    'ApplicationID': '/sc/6694606/634_287355388',
    'AccessKeyID': 'NjY5NDYwNjE0NDQ0NTUzOTMzMTc',
    'PrivateAccessKey': 'YmM2MzU2NWY4NTE2NGUxZmI5ODM4MTgyMTg3ZDUwNDY',
    'RefreshTokenURL': 'https://api.sugarsync.com/app-authorization',
    'AccessTokenURL': 'https://api.sugarsync.com/authorization',
    'Login': 'kevin.eeckman@gmail.com',
    'Password': 'F14Tomcat;'
}

_session = {}

_httpheaders = {
    'user-agent': _config['ApplicationName']+'/'+_config['Version']
}


def getrefreshtoken():
    '''
    Get (non-expiring) refresh token from user authentication data
    :return:
    '''
    refreshtokenxml = ("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
                    "<appAuthorization>"
                    "<username>"+_config['Login']+"</username>"
                    "<password>"+_config['Password']+"</password>"
                    "<application>"+_config['ApplicationID']+"</application>"
                    "<accessKeyId>"+_config['AccessKeyID']+"</accessKeyId>"
                    "<privateAccessKey>"+_config['PrivateAccessKey']+"</privateAccessKey>"
                    "</appAuthorization>")
    r=requests.post(_config['RefreshTokenURL'], headers=_httpheaders, data=refreshtokenxml)
    _config['RefreshToken']=r.headers['location']
    return r


def getaccesstoken():
    '''
    Get (expiring) access token from refresh token
    :return:
    '''
    accesstokenxml = ( "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
                    "<tokenAuthRequest>"
                    "<accessKeyId>"+_config['AccessKeyID']+"</accessKeyId>"
                    "<privateAccessKey>"+_config['PrivateAccessKey']+"</privateAccessKey>"
                    "<refreshToken>"+_config['RefreshToken']+"</refreshToken>"
                    "</tokenAuthRequest>")
    r=requests.post(_config['AccessTokenURL'], headers=_httpheaders, data=accesstokenxml)
    _httpheaders['Authorization']=r.headers['location']
    xml=ET.fromstring(r.content)
    _session['AccessToken']=r.headers['location']
    _session['URL']=xml.find('user').text
    _session['TokenExpDate']=dateutil.parser.parse(xml.find('expiration').text)
    return r

def getuserinfo():
    r=requests.get(_session['URL'], headers=_httpheaders)
    xml=ET.fromstring(r.content)
    _session['Workspaces']=xml.find('workspaces').text
    _session['Syncfolders']=xml.find('syncfolders').text
    return r

def main():
    print("Welcome to SugarSync Linux")
    global s
    #refresh=getrefreshtoken()
    #access=getaccesstoken()

    s = sugarsync.SugarSync(
        _config['ApplicationName'],
        _config['Version'],
        _config['ApplicationID'],
        _config['AccessKeyID'],
        _config['PrivateAccessKey']
    )

    s.login(_config['Login'], _config['Password'])
    s.workspace_collection.workspaces



if __name__== "__main__":
    main()


