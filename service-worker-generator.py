import os
from hashlib import sha224
import json
import time

files = ['/index.html', '/static/rpi-logo.ico', '/static/rpi-logo.png']


def revision_generator(file_path, l=21):
    revision = sha224(str(file_path + str(time.time())
                          ).encode('utf-8')).hexdigest()
    if len(revision) > l:
        return revision[:l]
    else:
        return revision


def make_json():
    results = []
    for file in files:
        results.append({
            'revision': revision_generator(file),
            'url': file
        })

    return results


if __name__ == '__main__':
    here = os.getcwd()
    res = make_json()
    json_array = json.dumps(res)

    with open(here + '/static/precache-manifest.js', 'w') as precache_manifest:
        precache_manifest.write(
            f'self.__precacheManifest=(self.__precacheManifest || []).concat({json_array});'
        )

    with open(here + '/static/service-worker.js', 'w') as service_worker:
        service_worker.write('\
importScripts(\"https://storage.googleapis.com/workbox-cdn/releases/4.3.1/workbox-sw.js\"); \n\
importScripts(\"/static/precache-manifest.js\");\n\
self.addEventListener(\'message\', (event) => {\n\
    if (event.data && event.data.type === \'SKIP_WAITING\') {\n\
        self.skipWaiting();\n\
    }\n\
});\n\
workbox.core.clientsClaim();\n\
self.__precacheManifest = [].concat(self.__precacheManifest || []);\n\
workbox.precaching.precacheAndRoute(self.__precacheManifest, {});\n\
workbox.routing.registerNavigationRoute(workbox.precaching.getCacheKeyForURL(\"/index.html\"), {\n\
    blacklist: [/^\\/_/,/\\/[^\\/?]+\\.[^\\/]+$/],\n\
});\
')