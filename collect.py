#!/usr/bin/env python
# encoding: utf-8

from __future__ import absolute_import, division
from os import listdir, system
from os.path import dirname, expanduser, join, realpath


CURRENT_DIR = dirname(realpath(__file__))
ARCHIVE_DIR = join(CURRENT_DIR, 'archive')
LATEST_DIR = join(CURRENT_DIR, 'latest')
HOMESCREEN_DROPBOX_DIR = expanduser('~/Dropbox/homescreen')


def get_iso_date(path):
    # "foo/Photo 13.11.2012 14 28 18.png" -> ("2012", "11", "13")
    return '-'.join(path.split(' ')[-4].split('.')[::-1])


def get_paths(dir_):
    for name in listdir(dir_):
        if name.endswith('.png'):
            yield join(dir_, name)


def sort_paths(paths):
    return sorted(paths, key=get_iso_date)


def commit(src_path, dst_path, latest_path, latest_scale, commit_msg):
    system("""
    mv '%(src)s' '%(dst)s'
    convert '%(dst)s' -resize %(scale)s '%(latest)s'
    optipng '%(dst)s'
    optipng '%(latest)s'
    git add .
    git commit --message '%(msg)s'
    """.strip().replace('\n', ' && ') % {
        'src': src_path,
        'dst': dst_path,
        'scale': latest_scale,
        'latest': latest_path,
        'msg': commit_msg,
    })


def _main():
    for device, latest_suffix, latest_scale in [
        ('iPhone', '480', '75%'),
        ('iPad', '540', '35%'),
    ]:
        src_dir = join(HOMESCREEN_DROPBOX_DIR, device)
        dst_dir = join(ARCHIVE_DIR, device)
        latest_path = join(LATEST_DIR, '%s_%s.png' % (device, latest_suffix))

        for src_path in sort_paths(get_paths(src_dir)):
            iso_date = get_iso_date(src_path)
            dst_path = join(dst_dir, iso_date + '.png')
            commit_msg = '%s: %s' % (iso_date, device)
            commit(src_path, dst_path, latest_path, latest_scale, commit_msg)

if __name__ == '__main__':
    _main()
