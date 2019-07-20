import os
import datetime
import re
import requests
from bs4 import BeautifulSoup
from Search.check_youtube import youtube_url_validation
from Search.youtube import yt_down
from Search.sd_algorithm import SDAlgorithm
from tqdm import tqdm


def open_download(self, topic, buffer, filedir, link):
    link_save_path = "Links"
    destination = "{}/{}/{}".format(link_save_path, topic, filedir)
    
    def check_link(link):
        link = re.split("&", link)
        link = re.split("%", link[0])
        return link[0]

    link = check_link(link)
    print(link)

    m = youtube_url_validation(link)
    if m:
        suffix = m.group(6)
        print('OK {}'.format(link))
        print(m.groups())
        print(suffix)
        link = "http://www.youtube.com/watch?v={}".format(suffix)
        if link in buffer:
            return "none", link, False
        vid_name, found = yt_down(link, destination)
        return vid_name, link, found

    if link in buffer:
        return "none", link, False

    #if link is pdf
    if (".pdf" in link) or (".PDF" in link):
        filename = "{}.pdf".format(filedir)
        r = requests.get(link, stream=True)
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open("{}/{}".format(destination,filename), "wb") as pdf:
            for chunk in tqdm(r.iter_content(chunk_size=1024)):
                # writing one chunk at a time to pdf file
                if chunk:
                    pdf.write(chunk)
        found = True
        return filename, link, found

    #if link is png
    if (".png" in link) or (".PNG" in link):
        filename = "{}.png".format(filedir)
        r = requests.get(link)
        if not os.path.exists(destination):
            os.makedirs(destination)
        with open("{}/{}".format(destination, filename), 'wb') as f:
            f.write(r.content)
        found = True
        return filename, link, found

    try:
        sd = SDAlgorithm()
        sd.url = link
        sd.destination = destination
        sd.filename = filedir
        sd.analyze_page()
        print("debug!")
        filename = "{}.txt".format(filedir)
        print("debug!")
        found = True
        print("debug!")
        return filename, link, found
    except Exception as error:
        print(error)
        filename = 'none'
        found = False

    return filename, link, found
