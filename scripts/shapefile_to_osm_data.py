#!/usr/bin/python
# -*- coding: utf-8 -*-


u"""
Simple script wrapper updating lock file and calling callback URL.
"""


import argparse
import subprocess
import sys
import urllib2
import os


job_name = os.path.splitext(os.path.basename(__file__))[0]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project_id')
    parser.add_argument('process_infos_dir_name')
    parser.add_argument('ogr2osm_script_file_path')
    parser.add_argument('shapefile_input_file_path')
    parser.add_argument('osm_data_output_file_path')
    parser.add_argument('--callback-url')
    args = parser.parse_args()

    assert os.path.isdir(args.process_infos_dir_name)
    assert os.path.isfile(args.ogr2osm_script_file_path)
    assert os.path.isfile(args.shapefile_input_file_path)

    process = subprocess.Popen(
        [
            'python',
            args.ogr2osm_script_file_path,
            args.shapefile_input_file_path,
            '--output', args.osm_data_output_file_path,
            ],
        )
    process.wait()

    if args.callback_url is not None:
        return_code_file_path = os.path.join(args.process_infos_dir_name, u'{0}.returncode'.format(job_name))
        with open(return_code_file_path, 'w') as return_code_file:
            return_code_file.write(str(process.returncode))
        lock_file_path = os.path.join(args.process_infos_dir_name, u'{0}.lock'.format(job_name))
        os.unlink(lock_file_path)
        urllib2.urlopen(args.callback_url)

    return 0


if __name__ == '__main__':
    sys.exit(main())
