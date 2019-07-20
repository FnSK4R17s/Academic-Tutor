import os
import datetime
import re
import urllib.request
from bs4 import BeautifulSoup

def open_download(self, topic, buffer, filedir, link):
    link_save_path = "Links"

    def check_link(link):
        link = re.split("&", link)
        link = re.split("%", link[0])
        return link

    link = check_link(link)

    if link in buffer:
        return "none", False

    try:
        html = urllib.request.urlopen(link[0])
        soup = BeautifulSoup(html, features="lxml")
        data = soup.findAll(text=True)
        def visible(element):
            if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                return False
            elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                return False
            return True
        result = filter(visible, data)
        material = str(list(result))
        print(material)
        #print(list(result))
        found = True
        if not os.path.exists("{}/{}/{}".format(link_save_path, topic, filedir)):
            os.makedirs("{}/{}/{}".format(link_save_path, topic, filedir))
        filename = "{}.txt".format(filedir)
        with open("{}/{}/{}/{}".format(link_save_path, topic, filedir, filename), 'wb') as f:
            f.write(material.encode("utf-8"))
    except urllib.error.HTTPError:
        filename = 'none'
        found = False
    except urllib.error.URLError:
        filename = 'none'
        found = False
    except ConnectionResetError:
        filename = 'none'
        found = False
    
    return filename, found


