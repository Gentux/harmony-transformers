#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import os
import shutil
import sys
import urllib2


u"""
Build a carto project to generate tiles with.
"""


def build_carto_project(project_id, carto_project_dir_name, db_user, db_password):
    carto_project_template_dir_name = os.path.join(os.path.dirname(__file__), '..', 'data', 'carto_project_template')
    style_file_path = os.path.join(carto_project_template_dir_name, 'style.mss')
    shutil.copyfile(style_file_path, os.path.join(carto_project_dir_name, 'style.mss'))
    project_template_file_path = os.path.join(carto_project_template_dir_name, 'project.mml')
    with open(project_template_file_path, 'r') as project_template_file:
        project_template = project_template_file.read()
    with open(os.path.join(carto_project_dir_name, 'project.mml'), 'w') as output_file:
        output_file.write(project_template.format(
            db_password=db_password,
            db_user=db_user,
            project_id=project_id,
            ))
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('carto_project_dir_name')
    parser.add_argument('db_user')
    parser.add_argument('db_password')
    parser.add_argument('--callback-url')
    args = parser.parse_args()
    result = build_carto_project(args.project_id, args.carto_project_dir_name, args.db_user, args.db_password)
    if args.callback_url:
        urllib2.urlopen(args.callback_url)
    return result


if __name__ == '__main__':
    sys.exit(main())
