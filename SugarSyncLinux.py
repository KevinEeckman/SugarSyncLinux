import sugarsync
import gui


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

def main():
    global s

    s = sugarsync.SugarSync(
        _config['ApplicationName'],
        _config['Version'],
        _config['ApplicationID'],
        _config['AccessKeyID'],
        _config['PrivateAccessKey']
    )

    s.login(_config['Login'], _config['Password'])
    #s.syncfolders.contents
    #print(s.syncfolders.items[1].contents.show())
    #s.syncfolders.items[1].recurse_print()

    window = gui.Window() # Implicitly creates tk.Tk object
    window.master.title(_config['ApplicationName'] + ' ' + _config['Version'])
    window.display_tree(s.syncfolders)
    window.master.mainloop()

if __name__== "__main__":
    main()


