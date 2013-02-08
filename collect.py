#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os import listdir, system
from os.path import dirname, expanduser, join, realpath


CURRENT_DIR = dirname(realpath(__file__))
SCREENSHOTS_DIR = join(CURRENT_DIR, 'screenshots')


def get_iso_date(path):
    # "foo/Photo 13.11.2012 14 28 18.png" -> ("2012", "11", "13")
    return '-'.join(path.split(' ')[-4].split('.')[::-1])


def get_paths(dir_='~/Dropbox/homescreen'):
    dir_ = realpath(expanduser(dir_))
    for name in listdir(dir_):
        yield join(dir_, name)


def sort_paths(paths):
    return sorted(paths, key=get_iso_date)


def commit(path):
    iso_date = get_iso_date(path)
    system("""
    mv '%(src)s' '%(dst)s'
    convert '%(dst)s' -resize 75%% '%(latest)s'
    optipng '%(dst)s'
    optipng '%(latest)s'
    git add .
    git commit --message %(date)s
    """.strip().replace('\n', ' && ') % {
        'src': path,
        'dst': join(SCREENSHOTS_DIR, iso_date + '.png'),
        'latest': join(CURRENT_DIR, 'latest_480.png'),
        'date': iso_date,
    })


def _main():
    for path in sort_paths(get_paths()):
        commit(path)

if __name__ == '__main__':
    _main()
