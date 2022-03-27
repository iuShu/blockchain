import json
import os.path
import sys


class Configuration(object):

    def __init__(self):
        self.root = sys.path[1]
        self.repo = dict()
        self.load_conf()
        self.repo['headers'] = {'json': {'content-type': 'application/json'}}

    def load_conf(self):
        def find_conf(path):
            for d in os.listdir(path):
                cur = f'{path}/{d}'
                if d.startswith('.'):
                    continue
                elif os.path.isfile(cur) and cur.endswith('.json'):
                    files.append(cur)
                elif os.path.isdir(cur):
                    find_conf(cur)

        temp = dict()
        files = []
        find_conf(self.root)
        # [print(f) for f in files]
        for f in files:
            with open(f, 'r', encoding='utf-8') as fp:
                values = json.load(fp)
                vals = dict()
                for v in values:
                    vals[v['name']] = v
                temp[os.path.split(f)[1].split('.')[0]] = vals
        self.repo = temp

    @staticmethod
    def jsonapi(method: str) -> dict:
        jsonrpc = dict()
        jsonrpc['id'] = 5
        jsonrpc['jsonrpc'] = '2.0'
        jsonrpc['method'] = method
        jsonrpc['params'] = []
        return jsonrpc

    def header(self, name='json') -> dict:
        hd = self.repo['headers']
        if hd:
            return hd[name]

    def network(self, name: str = 'ropsten') -> str:
        nw = self.repo['networks']
        if nw:
            return nw[name]['url']

    def account(self, name: str) -> str:
        ac = self.repo['accounts']
        if ac:
            return ac[name]['address']

    def all_accounts(self) -> list:
        ac = self.repo['accounts']
        if ac:
            return [ac[k]['address'] for k in ac.keys()]


conf = Configuration()

if __name__ == '__main__':
    print(conf.repo)
    print(conf.header())
    print(conf.network('ropsten'))
    print(conf.account('billionaire2'))
    print(conf.all_accounts())