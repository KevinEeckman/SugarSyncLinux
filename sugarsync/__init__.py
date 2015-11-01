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

    resources = {}

    def __init__(self, uri):
        self.uri = uri
        self._hasdata = False
        Resource.resources[uri]=self

    def _refresh(self):
        if not _session:
            pass
        return ET.fromstring(session.get(self.uri))

    def _initialize(self):
        if not self._hasdata:
            self._refresh()
            self._hasdata = True


class CollectionResource(Resource):
    def __init__(self, uri, parent=None):
        super().__init__(uri)
        self.parent=parent
        self._items = []

    def _refresh(self):
        xml = super()._refresh()
        for i in xml.iter('collection'):
            self._items.append(Folder(i.find('ref').text, i.find('displayName').text, self))
        for i in xml.iter('file'):
            self._items.append(File(i.find('ref').text,
                                    i.find('displayName').text,
                                    i.find('size').text,
                                    i.find('lastModified').text,
                                    self))

    @property
    def items(self):
        self._initialize()
        return self._items

    def __getitem__(self, index):
        self._initialize()
        return self._items[index]

    def __iter__(self):
        self._initialize()
        return iter(self._items)

    def __next__(self):
        self._initialize()
        return next(self._items)

    def show(self):
        ret = 'Collection:\n'
        for i in self.items:
            s = getattr(i,'show', None)
            if callable(s):
                ret = ret + '\t' + i.show()
            else:
                ret = ret + '\tFile\t' + i['displayName'] + '\n'
        return ret




class Folder(Resource):
    def __init__(self, uri, name, parent = None):
        super().__init__(uri)
        self.parent = parent
        self.name = name
        self._time_created=None
        self._contents = None

    def _refresh(self):
        xml = super()._refresh()
        self._time_created = dateutil.parser.parse(xml.find('timeCreated').text)
        self._contents = CollectionResource(xml.find('contents').text, self.parent)

    @property
    def time_created(self):
        self._initialize()
        return self._time_created

    @property
    def contents(self):
        self._initialize()
        return self._contents

    def show(self):
        return '\tFolder\t' + self.name +'\n'

    def recurse_print(self, prefix='/'):
        new_prefix = prefix + self.name + '/'
        print(new_prefix)
        for i in self.contents:
            i.recurse_print(new_prefix)


class File(Resource):
    def __init__(self, uri, name, size, last_modified, parent):
        super().__init__(uri)
        self.parent = parent
        self.size=size
        self.last_modified=last_modified
        self.name = name
        self._time_created = None
        self._size = None

    def _refresh(self):
        xml = super()._refresh()
        self._time_created = dateutil.parser.parse(xml.find('timeCreated').text)
        self._last_modified = dateutil.parser.parse(xml.find('lastModified').text)
        self._size = int(xml.find('size').text)

    @property
    def time_created(self):
        self._initialize()
        return self._time_created

    def show(self):
        return '\tFile\t' + self.name +'\t' + str(self.size) + '\n'

    def recurse_print(self, prefix = ''):
        print(prefix + self.name)

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
        self.workspaces = CollectionResource('/workspaces/contents')
        self.syncfolders = CollectionResource('/folders/contents')

    def login(self, login, password):
        global session
        session = Session(self.appname, self.version, self.appid, self.accesskeyid, self.prvaccesskey)
        return session.login(login, password)


