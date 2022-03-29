import json
import os.path
import sys


class Configuration(object):

    def __init__(self):
        self.root = sys.path[1]
        self.repo = dict()
        self.load_conf()
        self.repo['headers'] = {'json': {'content-type': 'application/json'}}
        self.cur_network = self.repo['networks']['ropsten']
        self.cur_header = self.repo['headers']['json']
        print('[env] current network: ropsten', self.cur_network['url'])

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

    def secret(self, name: str) -> str:
        ac = self.repo['accounts']
        if ac:
            return ac[name]['secret']

    def all_accounts(self, with_secret=False) -> list:
        ac = self.repo['accounts']
        if ac:
            if with_secret:
                return [[ac[k]['address'] for k in ac.keys()], [ac[k]['secret'] for k in ac.keys()]]
            return [ac[k]['address'] for k in ac.keys()]

    def set_network(self, name: str) -> dict:
        nw = self.repo['networks']
        if name not in nw.keys():
            raise EnvironmentError('no such network ' + name)
        self.cur_network = nw[name]
        print('[env] current network:', name, self.cur_network['url'])
        return self.cur_network

    def set_header(self, name: str) -> dict:
        hd = self.repo['headers']
        if name not in hd.keys():
            raise EnvironmentError('no such header ' + name)
        self.cur_header = hd[name]
        return self.cur_header


conf = Configuration()

if __name__ == '__main__':
    print(conf.repo)
    print(conf.header())
    print(conf.network('ropsten'))
    print(conf.account('billionaire2'))
    print(conf.all_accounts())
    print(conf.all_accounts(with_secret=True))
