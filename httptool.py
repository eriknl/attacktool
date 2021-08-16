import attacktool
import requests
requests.packages.urllib3.disable_warnings()

# Setup a session and proxy if tool proxy parameter is set
def init_http(**kwargs):
    if 'proxy' in kwargs:
        proxies = dict(
            http=kwargs['proxy'],
            https=kwargs['proxy']
        )
        attacktool.set_global('proxy', proxies)
    session = requests.session()
    attacktool.set_global('session', session)

# Run a HTTP get adding the typed command as part of the query as set in the url tool parameter
def execute_httpget(Command, **kwargs):
    url = '%s%s' % (kwargs['url'], Command)
    proxy = attacktool.get_global('proxy', None)
    session = attacktool.get_global('session', requests.session())
    r = session.get(url, proxies=proxy)
    print(r.text)