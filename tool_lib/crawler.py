from lxml import html
import requests
import os

GLOBAL_AMCOMIC = 'https://www.amcomic.com'

def amcomic_crawler(chap_code='/chapter/9698', code_dir='./codes'):
    url = GLOBAL_AMCOMIC + chap_code
    print("populating from: {}".format(url))
    page = requests.get(url)
    print("successfully connected to url")
    tree = html.fromstring(page.content)

    # get title
    title = tree.xpath('//head/title/text()')[0].split('-')[0]
    dst = '{}.txt'.format(title)
    print("series title: {}".format(title))
    # check if title is already scraped
    if os.path.exists(os.path.join(code_dir,dst)):
        print("file already exists!")
    else:
        # abstract chapters
        chapters = tree.xpath('//li[@class="listItem"]/a')
        print("found {} chapters".format(len(chapters)))

        result = []
        for chapter in chapters:
            new_url = GLOBAL_AMCOMIC + chapter.attrib['href']
            result.append(new_url)

        with open(os.path.join(code_dir,dst), 'w') as filehandle:
            filehandle.writelines("%s\n" % chap for chap in result)