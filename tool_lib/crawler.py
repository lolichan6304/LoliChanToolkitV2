from lxml import html
import requests
import os
import numpy as np
import time
import urllib.request as urllib_request

GLOBAL_AMCOMIC = 'https://www.amcomic.com'

def filter_text(text):
    for ch in ['\\','/','?','.','!','$']:
        if ch in text:
            text = text.replace(ch,"")
    return text

def amcomic_crawler(chap_code='/chapter/9698', code_dir='./codes', save=True):
    url = GLOBAL_AMCOMIC + chap_code
    print("populating from: {}".format(url))
    page = requests.get(url)
    print("successfully connected to url")
    tree = html.fromstring(page.content)

    # get title
    title = tree.xpath('//head/title/text()')[0].split('-')[0]
    dst = '{}.txt'.format(filter_text(title))
    print("series title: {}".format(filter_text(title)))
    # abstract chapters
    chapters = tree.xpath('//li[@class="listItem"]/a')
    print("found {} chapters".format(len(chapters)))

    codes = []
    result = []
    if not os.path.exists(os.path.join(code_dir,dst)):
        for chapter in chapters:
            new_url = GLOBAL_AMCOMIC + chapter.attrib['href']
            result.append(new_url)
            codes.append(int(chapter.attrib['href'].split('/')[-1]))

        if save:
            with open(os.path.join(code_dir,dst), 'w') as filehandle:
                filehandle.writelines("%s\n" % chap for chap in result)
    else:
        for chapter in chapters:
            codes.append(int(chapter.attrib['href'].split('/')[-1]))
        print("file already exists!")

    return codes, result

def download_from_amcomic(url, save_dir):
    print("download from {}".format(url))
    page = requests.get(url)
    print("successfully connected to url")
    tree = html.fromstring(page.content)

    print("="*10)
    # get title
    title = tree.xpath('//head/title/text()')[0]
    print("title: {}".format(title))
    save_to = os.path.join(save_dir, filter_text(title))
    if not os.path.exists(save_to): # file has not been processed before
        print("folder not found in {}, creating folder...".format(save_to))
        os.mkdir(save_to)
    images = tree.xpath('//div[@class="comiclist"]/div/img')
    print("found {} pages".format(len(images)))
    if len(images) > 4:
        print("downloading...")
        for i, page in enumerate(images):
            p_url = page.attrib['src']
            urllib_request.urlretrieve(p_url, os.path.join(save_to, "pic_{:03d}.jpg".format(i)))

    print("="*10)
    print("save to: {}".format(save_dir))
    slp = np.random.uniform(2,5)
    print("sleeping for {:.4f} secs...".format(slp))
    time.sleep(slp)

def amcomic_downloader(code_dir='./check_updates', save_dir='./amcomic'):
    opener = urllib_request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    urllib_request.install_opener(opener)
    
    for codes in os.listdir(code_dir):
        print("checking {}".format(codes))
        with open(os.path.join(code_dir,codes), 'r') as filehandle:
            urls = [l.strip('\n\r') for l in filehandle.readlines()]
        print("number of chapters: {}".format(len(urls)))

        dst = os.path.join(save_dir, codes[:-4])
        if not os.path.exists(dst): # file has not been processed before
            print("folder not found in {}, creating folder...".format(save_dir))
            os.mkdir(dst)
        folder = sorted(os.listdir(dst))
        print("found {} folders".format(len(folder)))
        code = '/chapter/{}'.format(urls[0].split('/')[-1])
        _, result = amcomic_crawler(code, '', False)
        #print("currently there are {} chapters".format(len(result)))
        if len(result) > len(folder): # here we need to download the files
            for index in range(len(folder), len(result)):
                download_from_amcomic(result[index], dst)
            # save newfile
            with open(codes, 'w') as filehandle:
                filehandle.writelines("%s\n" % chap for chap in result)

        