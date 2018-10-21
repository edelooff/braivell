"""Converter from YAML to PCGen module + LST format."""

import itertools
import os
import sys

import yaml

DATA_DIR = 'homebrew'


def generate_lst_file(filename, entries):
    with open(filename, 'w') as fp:
        for entry in entries:
            statements = itertools.chain([entry['name']], entry['properties'])
            print('\t'.join(statements), file=fp)


def make_campaign_directory(name):
    campaign_dir = os.path.normpath(os.path.join(DATA_DIR, name))
    if not os.path.commonprefix((DATA_DIR, campaign_dir)):
        raise ValueError('campaign name not suitable as directory name :(')
    if not os.path.isdir(campaign_dir):
        os.makedirs(campaign_dir)
    return campaign_dir


def main(filename):
    """Reads a YAML file and builds a campaign directory with contents."""
    with open(filename) as fp:
        data = yaml.safe_load(fp.read())

    campaign_dir = make_campaign_directory(data['name'])
    file_prefix = data['prefix']
    for type_name, content in data['campaign_content'].items():
        print(f'Creating LST file for {type_name} ..')
        filename = os.path.join(campaign_dir, f'{file_prefix}_{type_name}.lst')
        generate_lst_file(filename, content['entries'])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Provide a YAML file to convert to PCGen module.')
    main(sys.argv[1])
