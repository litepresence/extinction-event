VERSION = 'Arisen Network Monitor'

# litepresence2018

# WTFPL

# you will need to install matplotlib to plot
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

# standard python libraries
import numpy as np
import warnings
import requests
import zlib
import json
import time
import sys
import os

# USER CONTROLS
#=====================================

# download basemap, name it arisen_basemap.png
# https://imgur.com/h8dohLd.png

# change DIRECTORY location of arisen.py and arisen_basemap.png
# be sure to begin and end with forward slash:

DIRECTORY = '/home/username/etc/etc/'

# do you wish to log, plot, and geolocate?
LOG = True 
GEO = True
PLOT = True
PAUSE = 3000
#=====================================

# create a directory to handle historical images
if not os.path.exists(DIRECTORY + 'HISTORY/'):
    os.makedirs(DIRECTORY + 'HISTORY/')

sys.stdout.write('\x1b]2;' + VERSION + '\x07')


locations = [
            'dwebs.io',
            'dbrowser.io',
            'dpack.io',
            'distdns.io',
            'dpress.io',
            'dstatus.io',
            'dmemo.io',
            'go.dwebuniversity.com',
            'signup.dpays.io',
            'dpayid.io',
            'dsite.io',
            'dsocial.io',
            'dvideo.io',
            'bex.network',
            'arisen.network',
            'afood.network',
            'atelecom.network',
            'aswipe.io',
            'aexchange.io',
            'agov.network',
            'avote.network',
            'arisenexplorer.com',
            'arisen.tools',
            'arisen.church',
            'abible.io',
            ]

warnings.filterwarnings("ignore", category=cbook.mplDeprecation)

def logo():

    print("\033c")
    a= b'x\x9cm\xd2;\x0e\xc40\x08\x04\xd0>\xa7H?\x02\xfa9\r7\xc8\xfd\xbb5\xd6\x82\xbfT\x16z\x19\x9b\xd8\xcf\xbb\x95\x8a\x01_\x14\x8c\x9a\xddg5\xf6mez0\xc5\x8ez\xa8\xae\x8c7\xd4\x13gV\xfb\x81\xa2\xee*\xc4p\xc5${\xf4ly\xe5K\xb1\xfc\x94\xf3H\xe9p0\x9d\x99f\\1\xbb\xa5\xc9\xc1\xa4v\xf5\x11\xc6\x83\xbd\xfc\xff\xfc6\xa9\xc6\xa4J3;Y\xb8LD_\xe2\xca\xdaU\r\xd8\xf1\x9d\xc5af\xd8\xee>\xcf\xb1\xb2\x90\xc2\xfeD\xd0\x90\xb8\x07\x04}a?$\xe9\x97\xa2'
    print(zlib.decompress(a).decode())

def race_append(doc='', text=''):  # Concurrent Append to File Operation

    # probably overkill for this app... nonetheless:
    if LOG:
        text = '\n' + str(time.ctime()) + ' ' + str(text) + '\n'
        i = 0
        while True:
            time.sleep(0.05 * i ** 2)
            i += 1
            if i > 10:
                break
            try:
                with open(doc, 'a+') as f:
                    f.write(text)
                    f.close()
                    break
            except Exception as e:
                msg = str(type(e).__name__) + str(e.args)
                msg += ' race_append()'
                print(msg)
                try:
                    f.close()
                except:
                    pass
                continue
            finally:
                try:
                    f.close()
                except:
                    pass

def test_nodes(): # ping and geolocate seed nodes

    print('')
    now = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
    print(now)
    race_append(doc='arisen.txt',text='')
    race_append(doc='arisen.txt',text=now)
    print('pinging and geolocating Arisen nodes...')
    print('')
    print('(IP, PING, GEOLOCATION)')
    nodes = []
    for i in locations:

        # test response time
        cmd='ping -c 1 ' + i
        a=os.popen(cmd).read()
        try:
            ping = int(a.split('time=')[1].split(' ms')[0])
        except:
            ping = 0
        
        ret = {}
        if GEO:
            # geolocate 
            geolocate = 'http://ip-api.com/json/'
            ip = i

            # some ips are not recognized by ip-api.com; substitute ipinfo.info manually:
            if ip == '':
                ip = ''
            geolocate += ip

            # make geolocation request and format response
            req = requests.get(geolocate, headers={})
            ret = json.loads(req.text)
            entriesToRemove =    ('isp','regionName','org','countryCode','timezone','region','as','status','zip')
            for k in entriesToRemove:
                ret.pop(k, None)
            ret['ip'] = ret.pop('query')
        ret = (i, ping, ret)
        # append to log file
        race_append(doc='arisen.txt',text=str((i, ping, ret)))
        print(ret)
        nodes.append(ret)

    return nodes

def plot_nodes(nodes):

        try:
            plt.close()
        except:
            pass
        imageFile = cbook.get_sample_data(DIRECTORY + 'arisen_basemap.png')
        img = plt.imread(imageFile)
        fig, ax = plt.subplots(figsize=(12,24))
        #plt.xticks(np.arange(-180,180,30))
        #plt.yticks(np.arange(-90,90,30))
        plt.xticks([])
        plt.yticks([])
        ax.imshow(img, extent=[-180, 180, -90, 90])
        fig.tight_layout()
        plt.pause(0.1)
        # PLOT SEED NODES
        xs = []
        ys = []
        for i in range(len(nodes)):
            if float(nodes[i][1]) > 0:
                try:
                    x = float(nodes[i][2]['lon'])
                    y = float(nodes[i][2]['lat'])
                    xs.append(x)
                    ys.append(y)
                except:
                    print('skipping', nodes[i])
                    pass
        plt.plot(xs,ys,color='aqua', marker='o', markersize=6, alpha=1.0)   

        utc = str(time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())) + ' UTC'

        plt.text(0, -60, utc, alpha=0.5, color='w', size=15)           

        location = DIRECTORY + 'arisen_nodemap.png'

        plt.savefig(location, 
            dpi=100,
            bbox_inches='tight',
            pad_inches = 0)

        # SAVE HISTORY
        if 1:
            location = DIRECTORY + 'HISTORY/arisen_nodemap_' + str(int(time.time())) + '.png'
         
            plt.savefig(location, 
                dpi=100,
                bbox_inches='tight',
                pad_inches = 0)

        for i in range(PAUSE):
            plt.pause(0.1)


def main():

    logo()

    nodes = test_nodes()

    if GEO and PLOT:
        plot_nodes(nodes)
    
if __name__ == "__main__":

    while 1:
        main()
