#! /usr/bin/python3

'''
Генерация баш скрипта для чистки дубликатов файлов
на входе список каталогов, отсортированных по приоритетам (от высшего к низшему)
и результат работы утилиты fdupes
'''

import sys
import logging
import argparse
from pathlib import Path

def chooseOneFile(filelist,dir_priority):
    """
    выбор одного файла из группы дубликатов, который оставляем
    """
    logger.debug("choose one file from list")
    logger.debug(str(filelist))
    onefile = None
    minpriority = 1000000
    for f in filelist:
        d = str(Path(f).parent)
        p = dir_priority[d]
        logger.debug("file: {}, dir: {}, priority: {}".format(f,d,p))
        if p < minpriority:
            minpriority = p
            onefile = f
    logger.debug("choose: {}".format(onefile))
    return onefile

def genDeduplicateScript(dupesfile,dirsfile):
    """
    генерация скрипта удаления дублей
    """
    logger.info("generate deduplicate script, dupesfile: {}, dirsfile: {}".format(dupesfile,dirsfile))
    dir_priority = dict()
    logger.info("read directories file")
    with open(dirsfile) as df:
        n = 1
        for s in df:
            dirname = str(Path(s.rstrip()))
            dir_priority[dirname] = n
            n += 1
    logger.info("read duplicates file")
    with open(dupesfile) as f:
        dupes = list()
        for s in f:
            fl = s.rstrip()
            if fl == "":
                one = chooseOneFile(dupes,dir_priority)
                for d in dupes:
                    if d == one:
                        print("# ---> {}".format(one))
                    else:
                        print("rm '{}'".format(d))
                print()
                dupes = list()
            else:
                dupes.append(fl)
    return 

def genFolderList(dupesfile):
    """
    выбор одного файла из группы дубликатов, который оставляем
    """
    logger.info("generate folder list")
    dirs = list()
    with open(dupesfile) as f:
        for s in f:
            dirs.append(str(Path(s.rstrip()).parent))
    for d in sorted(set(dirs)):
        print(d)
    return
#======================================================================================

logging.basicConfig(level=logging.INFO,format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

logger.info("start")
logger.info("parse arguments")
parser = argparse.ArgumentParser(description="Генерация скрипта удаления дубликатов файлов")
parser.add_argument("--file","-f",required=True,
        help="файл дубликатов (выход fdupes)")
parser.add_argument("--directories","-d",required=False,
        help="список директорий в порядке приоритета")
parser.add_argument("--gen-directories","-n",action="store_true",required=False,
        help="сгенерировать список каталогов")
parser.add_argument("--debug", action="store_true", default=False,
        help="отладочное логирование")
args = parser.parse_args();
if (args.debug):
    logger.setLevel(logging.DEBUG)
if (args.gen_directories):
    genFolderList(args.file)
else:
    if (args.directories is None):
        logger.fatal("directories option is required")
        sys.exit(1)
    genDeduplicateScript(args.file,args.directories)

logger.info("finish")

