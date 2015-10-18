__author__ = 'kevin'
import requests
import xml.etree.ElementTree as ET
import dateutil.parser


class Workspace:
    pass

class Session:
    def __init__(self, appname, version, appid, accesskeyid, prvaccesskey):
        self.appname=appname
        self.version=version
        self.appid=appid
        self.accesskeyid=accesskeyid
        self.prvaccesskey=prvaccesskey
        self._refreshtokenurl='https://api.sugarsync.com/app-authorization'
        self._accesstokenurl='https://api.sugarsync.com/authorization'
        self._refreshtoken=None
        self._httpheaders = { 'user-agent': appname+'/'+version }
        self._accesstoken = None
        self._main_url= None
        self._accesstoken_expdate=None

    def _refresh_session(self):
        if 'Authorization' in self._httpheaders:
            del self._httpheaders['Authorization']
        accesstokenxml = ( "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
                        "<tokenAuthRequest>"
                        "<accessKeyId>"+self.accesskeyid+"</accessKeyId>"
                        "<privateAccessKey>"+self.prvaccesskey+"</privateAccessKey>"
                        "<refreshToken>"+self._refreshtoken+"</refreshToken>"
                        "</tokenAuthRequest>")
        r=requests.post(self._accesstokenurl, headers=self._httpheaders, data=accesstokenxml)
        self._httpheaders['Authorization']=r.headers['location']
        xml=ET.fromstring(r.content)
        self._accesstoken=r.headers['location']
        self._main_url=xml.find('user').text
        self._accesstoken_expdate=dateutil.parser.parse(xml.find('expiration').text)


    def login(self,login,password):
        refreshtokenxml = ("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
                    "<appAuthorization>"
                    "<username>"+login+"</username>"
                    "<password>"+password+"</password>"
                    "<application>"+self.appid+"</application>"
                    "<accessKeyId>"+self.accesskeyid+"</accessKeyId>"
                    "<privateAccessKey>"+self.prvaccesskey+"</privateAccessKey>"
                    "</appAuthorization>")
        r=requests.post(self._refreshtokenurl, headers=self._httpheaders, data=refreshtokenxml)
        self._refreshtoken=r.headers['location']
        self._refresh_session()
        return self._refreshtoken

    def get(self, relative_url):
        if()
        return requests.get(self._main_url+relative_url, headers=self._httpheaders).content


_session=None

class User:
    def __init__(self):
        self._nickname = None
        self._username = None
        self._quota = 0
        self._usage = 0

    def _refresh(self):
        if _session is None:
            pass
        global xml
        xml = ET.fromstring(session.get(''))
        self._nickname = xml.findall('./nickname')[0].text
        self._username = xml.findall('./username')[0].text
        self._quota = int(xml.findall('./quota/limit')[0].text)
        self._usage = int(xml.findall('./quota/usage')[0].text)

    def initialize(self):
        if not self._nickname:
            self._refresh()

    @property
    def nickname(self):
        self.initialize()
        return self._nickname

    @property
    def username(self):
        self.initialize()
        return self._username

    @property
    def quota(self):
        self.initialize()
        return self._quota

    @property
    def usage(self):
        self.initialize()
        return self.usage

    @property
    def usage_percent(self):
        self.initialize()
        return self._usage/self._quota*100


class SugarSync:
    def __init__(self, appname, version, appid, accesskeyid, prvaccesskey):
        self.appname=appname
        self.version=version
        self.appid=appid
        self.accesskeyid=accesskeyid
        self.prvaccesskey=prvaccesskey
        self.user=User()


    def login(self,login,password):
        global session
        session = Session(self.appname, self.version, self.appid, self.accesskeyid, self.prvaccesskey)
        return session.login(login, password)


