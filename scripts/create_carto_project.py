#!/usr/bin/env python
# -*- coding: utf-8 -*-


u"""
Build a carto project to generate tiles with.
"""


import argparse
import os
import shutil
import subprocess
import sys
import urllib2


job_name = os.path.splitext(os.path.basename(__file__))[0]


def build_carto_project(project_id, carto_project_dir_name, db_user, db_password, carto_script_file_path):
    carto_project_template_dir_name = os.path.join(os.path.dirname(__file__), '..', 'data', 'carto_project_template')
    style_file_path = os.path.join(carto_project_template_dir_name, 'style.mss')
    shutil.copyfile(style_file_path, os.path.join(carto_project_dir_name, 'style.mss'))
    project_template_file_path = os.path.join(carto_project_template_dir_name, 'project.mml')
    with open(project_template_file_path, 'r') as project_template_file:
        project_template = project_template_file.read()
    project_mml_file_path = os.path.join(carto_project_dir_name, 'project.mml')
    with open(project_mml_file_path, 'w') as project_mml_file:
        project_mml_file.write(project_template.format(
            db_password=db_password,
            db_user=db_user,
            project_id=project_id,
            ))
    project_xml_file_path = os.path.join(carto_project_dir_name, 'project.xml')
    with open(project_xml_file_path, 'w') as project_xml_file:
        process = subprocess.Popen([carto_script_file_path, project_mml_file_path], stdout=project_xml_file)
        process.wait()
    return process.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('carto_project_dir_name')
    parser.add_argument('carto_script_file_path')
    parser.add_argument('db_user')
    parser.add_argument('db_password')
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    assert os.path.isdir(args.process_infos_dir_name)
    assert os.path.isdir(args.carto_project_dir_name)
    assert os.path.isfile(args.carto_script_file_path)

    result = build_carto_project(
        args.project_id, args.carto_project_dir_name, args.db_user, args.db_password, args.carto_script_file_path,
        )

    if args.callback_url is not None:
        return_code_file_path = os.path.join(args.process_infos_dir_name, u'{0}.returncode'.format(job_name))
        with open(return_code_file_path, 'w') as return_code_file:
            return_code_file.write(str(result or 0))
        lock_file_path = os.path.join(args.process_infos_dir_name, u'{0}.lock'.format(job_name))
        os.unlink(lock_file_path)
        urllib2.urlopen(args.callback_url)

    return result


if __name__ == '__main__':
    sys.exit(main())
