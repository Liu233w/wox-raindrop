#encoding=utf8
from woxex import WoxEx, WoxAPI, Log, load_module

with load_module():
    from urllib.parse import quote
    from os import environ
    import requests
    import webbrowser

class Main(WoxEx):

    # set the environment variable to raindrop test token, or just replace the following line
    TEST_TOKEN = environ.get('RAINDROP_TOKEN') or ''

    def request(self, url, params=None):

        headers = {'Authorization': 'Bearer ' + self.TEST_TOKEN}

        if self.proxy and self.proxy.get("enabled") and self.proxy.get("server"):
            proxies = {
                "http":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port")),
                "https":"http://{}:{}".format(self.proxy.get("server"),self.proxy.get("port"))}
            return requests.get(url,proxies = proxies, params=params, headers=headers)
        else:
            return requests.get(url, params=params, headers=headers)

    def query(self,key):

        # Log.info('token: ' + self.TEST_TOKEN)

        r = self.request('https://api.raindrop.io/rest/v1/raindrops/0', params={
            'search': key, 'perpage': 10}).json()

        results = [
            {
                'Title': 'Show in Raindrop.io about ' + key,
                'IcoPath': 'Images/pic.png',
                "JsonRPCAction": {
                    "Method": "openUrl",
                    "parameters": ['https://app.raindrop.io/my/0/' + quote(key)],
                    "dontHideAfterAction": False 
                }
            }
        ]
        for item in r['items']:
            results.append({
                'Title': item['title'],
                "SubTitle": 'Open ' + item['link'],
                "IcoPath": item['cover'],
                "JsonRPCAction": {
                    "Method": "openUrl",
                    "parameters": [item['link']],
                    "dontHideAfterAction": False 
                }
            })

        return results

    def openUrl(self, url):
        webbrowser.open(url)
        WoxAPI.change_query(url)

if __name__ == "__main__":
    Main()