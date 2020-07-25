from lxml import html
import requests
import os

GLOBAL_AMCOMIC = 'https://www.amcomic.com'

def filter_text(text):
    for ch in ['\\','/','?','.','!','$']:
        if ch in text:
            text = text.replace(ch,"")
    return text

def amcomic_crawler(chap_code='/chapter/9698', code_dir='./codes'):
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
    if not os.path.exists(os.path.join(code_dir,dst)):
        result = []
        for chapter in chapters:
            new_url = GLOBAL_AMCOMIC + chapter.attrib['href']
            result.append(new_url)
            codes.append(int(chapter.attrib['href'].split('/')[-1]))

        with open(os.path.join(code_dir,dst), 'w') as filehandle:
            filehandle.writelines("%s\n" % chap for chap in result)
    else:
        for chapter in chapters:
            codes.append(int(chapter.attrib['href'].split('/')[-1]))
        print("file already exists!")

    return codes
        