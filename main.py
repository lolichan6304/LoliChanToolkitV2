import argparse
import sys
import os
import glob
import time

import numpy as np
from PIL import Image
import cv2

import lxml
import requests

import tool_lib.osfunc as osfunc
import tool_lib.tool as tool
import tool_lib.crawler as crawler

def build(
        **kwargs
    ):
    to_build = ['./database', './local', './temp_folder', './temp_folder/input', './temp_folder/output', './codes']
    print("building directory structure")
    for i in to_build:
        osfunc.create_directory_structure(i)

def merge_tool(
        database='./database',
        compiled='./local',
        MAX=40000,
        **kwargs
    ):
    assert os.path.isdir(database) and os.path.isdir(compiled), "invalid directory provided"
    print("merge tool initialized")
    osfunc.copy_directory_structure(fro=database, to=compiled)
    print("begin merging")
    tool.merge_tool(database, compiled, MAX)

def split_tool(
        database='./temp_folder/input',
        compiled='./temp_folder/output',
        MAX=10000,
        **kwargs
    ):
    assert os.path.isdir(database) and os.path.isdir(compiled), "invalid directory provided"
    print("split tool initialized")
    osfunc.copy_directory_structure(fro=database, to=compiled)
    print("begin splitting")
    tool.split_tool(database, compiled, MAX)

## amcomic crawlers
def amcomic_crawler(
    code=9698,
    code_dir='./codes',
    **kwargs
    ):
    chap = '/chapter/{}'.format(code)
    chap = '/chapter/{}'.format('17154-10580308')
    res = crawler.amcomic_crawler(chap, code_dir)

def amcomic_hunt(
    fro=9000,
    to=9500,
    code_dir='./codes',
    **kwargs
    ):
    to_hunt = list(range(fro,to))
    while (len(to_hunt)>0):
        print('number of codes left... {}'.format(len(to_hunt)))
        curr = to_hunt.pop()
        chap = '/chapter/{}'.format(curr)
        res = crawler.amcomic_crawler(chap, code_dir)
        for i in res:
            if i in to_hunt:
                to_hunt.remove(i)

        slp = np.random.uniform(2,5)
        print("sleeping for {:.4f} secs...".format(slp))
        time.sleep(slp)

def execute_cmdline(argv):
    prog = argv[0]
    parser = argparse.ArgumentParser(
        prog        = prog,
        description = 'Welcome to LoliChanToolkitV2',
        epilog      = 'type "{} <command> -h" for more information.'.format(prog)
    )

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    def add_command(cmd, desc, example=None):
        epilog = 'Example: %s %s' % (prog, example) if example is not None else None
        return subparsers.add_parser(cmd, description=desc, help=desc, epilog=epilog)

    p = add_command('build', 'build and prepare directory', '')

    p = add_command('merge_tool', 'merge toons from database to compiled folder', '')
    
    p.add_argument('--database', help='directory of database',              default='./database')
    p.add_argument('--compiled', help='directory of compiled folder',       default='./local')
    p.add_argument('--MAX',      help='max height of webtoon to be merged', default=40000,        type=int)

    p = add_command('split_tool', 'split toons from database to compiled folder', '')
    
    p.add_argument('--database', help='directory of database',              default='./temp_folder/input')
    p.add_argument('--compiled', help='directory of compiled folder',       default='./temp_folder/output')
    p.add_argument('--MAX',      help='max height of webtoon to be merged', default=10000,        type=int)

    p = add_command('amcomic_crawler', 'crawler for amcomic that pulls chapter url', '')

    p.add_argument('--code',     help='chapter code to populate from',      default=9698,         type=int)
    p.add_argument('--code_dir', help='directory of compiled folder',       default='./codes')

    p = add_command('amcomic_hunt', 'crawler for amcomic that hunts for chapter url', '')

    p.add_argument('--fro',      help='chapter code to populate from',      default=13000,         type=int)
    p.add_argument('--to',       help='chapter code to populate from',      default=17000,         type=int)
    p.add_argument('--code_dir', help='directory of compiled folder',       default='./codes')

    args = parser.parse_args(argv[1:] if len(argv) > 1 else ['h'])
    func = globals()[args.command]
    del args.command
    func(**vars(args))

if __name__ == "__main__":
    execute_cmdline(sys.argv)