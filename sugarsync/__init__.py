import requests
import xml.etree.ElementTree as ET
import datetime
import dateutil.parser

__author__ = 'kevin'


class Workspace:
    pass


class Session:
    def __init__(self, appname, version, appid, accesskeyid, prvaccesskey):
        self.appname = appname
        self.version = version
        self.appid = appid
        self.accesskeyid = accesskeyid
        self.prvaccesskey = prvaccesskey
        self._refreshtokenurl = 'https://api.sugarsync.com/app-authorization'
        self._accesstokenurl = 'https://api.sugarsync.com/authorization'
        self._refreshtoken = None
        self._httpheaders = {'user-agent': appname+'/'+version}
        self._accesstoken = None
        self._main_url = None
        self._accesstoken_expdate = None

    def _refresh_session(self):
        if 'Authorization' in self._httpheaders:
            del self._httpheaders['Authorization']
        accesstokenxml = ("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
                          "<tokenAuthRequest>"
                          "<accessKeyId>"+self.accesskeyid+"</accessKeyId>"
                          "<privateAccessKey>"+self.prvaccesskey+"</privateAccessKey>"
                          "<refreshToken>"+self._refreshtoken+"</refreshToken>"
                          "</tokenAuthRequest>")
        r = requests.post(self._accesstokenurl, headers=self._httpheaders, data=accesstokenxml)
        self._httpheaders['Authorization'] = r.headers['location']
        xml = ET.fromstring(r.content)
        self._accesstoken = r.headers['location']
        self._main_url = xml.find('user').text
        self._accesstoken_expdate = dateutil.parser.parse(xml.find('expiration').text)

    def login(self, login, password):
        refreshtokenxml = ("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>"
                           "<appAuthorization>"
                           "<username>"+login+"</username>"
                           "<password>"+password+"</password>"
                           "<application>"+self.appid+"</application>"
                           "<accessKeyId>"+self.accesskeyid+"</accessKeyId>"
                           "<privateAccessKey>"+self.prvaccesskey+"</privateAccessKey>"
                           "</appAuthorization>")
        r = requests.post(self._refreshtokenurl, headers=self._httpheaders, data=refreshtokenxml)
        self._refreshtoken = r.headers['location']
        return self._refreshtoken

    def _build_url(self, main_url, url):
        if url.startswith('http'):
            return url
        return main_url+url

    def get(self, url):
        if not self._accesstoken_expdate or self._accesstoken_expdate < datetime.datetime.now(datetime.timezone.utc):
            print('Requesting new access token...')
            self._refresh_session()
        u=self._build_url(self._main_url, url)
        print('Retrieving content from '+u)
        return requests.get(u, headers=self._httpheaders).content


_session = None


class Resource:
    def __init__(self, url):
        self._url = url
        self._hasdata = False

    def _refresh(self):
        if not _session:
            pass
        return ET.fromstring(session.get(self._url))

    def _initialize(self):
        if not self._hasdata:
            self._refresh()
            self._hasdata = True


class CollectionResource(Resource):
    def __init__(self, url, type=None):
        super().__init__(url)
        self._contents = []
        self._type = type

    def _refresh(self):
        xml = super()._refresh()
        items = xml.findall('./collection')
        for i in items:
            w = {'type': i.attrib['type'],
                 'displayName': i.find('displayName').text,
                 'ref': i.find('ref').text,
                 'contents': i.find('contents').text}
            obj=None
            if (w['type'] == 'syncFolder') or (w['type'] == 'folder'):
                obj=Folder(w['displayName'], w['ref'], w['contents'], w['type'])
            else:
                obj=w
            self._contents.append(obj)

    @property
    def type(self):
        self._initialize()
        return self._type

    @property
    def contents(self):
        self._initialize()
        return self._contents

    def show(self):
        print('Collection: '+self.type)
        for i in self.contents:
            s = getattr(i,'show', None)
            if callable(s):
                print('\t' + s())
            else:
                print('\t' + i['displayName'])


class WorkspaceCollection(CollectionResource):
    def __init__(self):
        super().__init__('/workspaces/contents', 'WorkspaceCollection')


class SyncFolderCollection(CollectionResource):
    def __init__(self):
        super().__init__('/folders/contents', 'SyncFolderCollection')


class Folder(Resource):
    def __init__(self, name, ref, contents, type):
        super().__init__(ref)
        self.name = name
        self.type=type
        self._collection = CollectionResource(contents, type)
        self._time_created=None

    def _refresh(self):
        xml = super()._refresh()
        self._time_created = dateutil.parser.parse(xml.find('timeCreated').text)

    @property
    def time_created(self):
        self._initialize()
        return self._time_created

    @property
    def contents(self):
        self._collection._initialize()
        return self._collection.contents

    def show(self):
        print(self.type + '\t\t' + self.name)


class User(Resource):
    def __init__(self):
        super().__init__('')
        self._nickname = None
        self._username = None
        self._quota = 0
        self._usage = 0

    def _refresh(self):
        xml = super()._refresh()
        self._nickname = xml.findall('./nickname')[0].text
        self._username = xml.findall('./username')[0].text
        self._quota = int(xml.findall('./quota/limit')[0].text)
        self._usage = int(xml.findall('./quota/usage')[0].text)

    @property
    def nickname(self):
        self._initialize()
        return self._nickname

    @property
    def username(self):
        self._initialize()
        return self._username

    @property
    def quota(self):
        self._initialize()
        return self._quota

    @property
    def usage(self):
        self._initialize()
        return self._usage

    @property
    def usage_percent(self):
        self._initialize()
        return self._usage/self._quota*100


class SugarSync:
    def __init__(self, appname, version, appid, accesskeyid, prvaccesskey):
        self.appname = appname
        self.version = version
        self.appid = appid
        self.accesskeyid = accesskeyid
        self.prvaccesskey = prvaccesskey
        self.user = User()
        self.workspace_collection = WorkspaceCollection()
        self.syncfolders = SyncFolderCollection()

    def login(self, login, password):
        global session
        session = Session(self.appname, self.version, self.appid, self.accesskeyid, self.prvaccesskey)
        return session.login(login, password)


