from lxml import html
import requests
import os
import numpy as np
import time
import urllib.request as urllib_request
import urllib.error as urllib_error
import urllib
import json
import re

GLOBAL_AMCOMIC = 'https://www.amcomic.com'
android_header = "Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36"

def filter_text(text):
    for ch in ['\\','/','?','.','!','$','<','>']:
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
        images = tree.xpath('//div[@class="comiclist"]/div/img')
        print("found {} pages".format(len(images)))
        if len(images) > 4:
            print("folder not found in {}, creating folder...".format(save_to))
            os.mkdir(save_to)
            print("downloading...")
            for i, page in enumerate(images):
                p_url = page.attrib['src']
                try:
                    urllib_request.urlretrieve(p_url, os.path.join(save_to, "pic_{:03d}.jpg".format(i)))
                except urllib_error.HTTPError:
                    pass
        print("save to: {}".format(save_dir))
        slp = np.random.uniform(2,5)
        print("sleeping for {:.4f} secs...".format(slp))
        time.sleep(slp)
    else:
        print("folder is found in {}. please delete the folder if you are interested to download it".format(save_to))
    print("="*10)
    

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
        if len(result) > len(folder): # here we need to download the files
            for index, item in enumerate(result):
                download_from_amcomic(item, dst)
            # save newfile
            with open(os.path.join(code_dir, codes), 'w') as filehandle:
                filehandle.writelines("%s\n" % chap for chap in result)

# mymhh downloader tools
def extract_links(url):
    page = urllib_request.urlopen(url).read()
    print("successfully connected to url")
    tree = html.fromstring(page)

    chapters = tree.xpath('//div[@id="chapter_indexes"]/ul/li/a')
    print("found {} chapters".format(len(chapters)))
    result = []
    for i, item in enumerate(chapters):
        code_ = item.attrib['href']
        result.append('https://www.mymhh.com'+code_)
    return result

def extract_images(url, save_dir, referrer):
    print("download from {}".format(url))
    opener = urllib_request.build_opener()
    opener.addheaders = [
        ('User-agent', 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36'),
        ('Referrer', referrer)]
    urllib_request.install_opener(opener)
    page = urllib_request.urlopen(url).read()
    print("successfully connected to url")
    tree = html.fromstring(page)

    print("="*10)
    # get title
    title = tree.xpath('//head/title/text()')[0]
    print("title: {}".format(title))
    save_to = os.path.join(save_dir, filter_text(title))
    if not os.path.exists(save_to): # file has not been processed before
        images = tree.xpath('//div[@id="cp_img"]/img')
        print("found {} pages".format(len(images)))
        if len(images) > 4:
            print("folder not found in {}, creating folder...".format(save_to))
            os.mkdir(save_to)
            print("downloading...")
            for i, page in enumerate(images):
                p_url = page.attrib['data-original']
                try:
                    opener = urllib_request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36')]
                    urllib_request.install_opener(opener)
                    urllib_request.urlretrieve(p_url, os.path.join(save_to, "pic_{:03d}.jpg".format(i)))
                except urllib_error.HTTPError:
                    pass
        print("save to: {}".format(save_dir))
        slp = np.random.uniform(2,5)
        print("sleeping for {:.4f} secs...".format(slp))
        time.sleep(slp)
    else:
        print("folder is found in {}. please delete the folder if you are interested to download it".format(save_to))
    print("="*10)


def mymhh_downloader(code_file='./mymhh/download_list.json', save_dir='./mymhh'):
    with open(code_file) as f:
        search_for = json.load(f)
    print("loaded json file {}".format(code_file))
    print("number of series to search for updates: {}".format(len(search_for)))

    # set up urllib
    opener = urllib_request.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36')]
    urllib_request.install_opener(opener)

    for k, v in search_for.items():
        print("working on: {}".format(k))
        print("website: {}".format(v))

        # make root directory
        dst = os.path.join(save_dir, k)
        if not os.path.exists(dst): # file has not been processed before
            print("folder not found in {}, creating folder...".format(save_dir))
            os.mkdir(dst)
        
        # extract links
        lst = extract_links(v)
        for i, link in enumerate(lst):
            extract_images(link, dst, v)

        

        