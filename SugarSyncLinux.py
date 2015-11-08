import sugarsync
import gui
import argparse


_config = {
    'ApplicationName': 'SugarSyncLinux',
    'Version': '0.1',
    'ApplicationID': '/sc/6694606/634_287355388',
    'AccessKeyID': 'NjY5NDYwNjE0NDQ0NTUzOTMzMTc',
    'PrivateAccessKey': 'YmM2MzU2NWY4NTE2NGUxZmI5ODM4MTgyMTg3ZDUwNDY',
    'RefreshTokenURL': 'https://api.sugarsync.com/app-authorization',
    'AccessTokenURL': 'https://api.sugarsync.com/authorization',
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


    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--login", help="your SugarSync login")
    parser.add_argument("-p", "--password", help="your SugarSync password")
    args = parser.parse_args()

    if (args.login and args.password):

        s.login(_config['Login'], _config['Password'])
        #s.syncfolders.contents
        #print(s.syncfolders.items[1].contents.show())
        #s.syncfolders.items[1].recurse_print()

        window = gui.MainWindow() # Implicitly creates tk.Tk object
        window.master.title(_config['ApplicationName'] + ' ' + _config['Version'])
        window.display_tree(s.syncfolders)
        window.master.mainloop()

    else:
        print("login/pwd required. See --help")

if __name__== "__main__":
    main()


