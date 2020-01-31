import sh
import os
import sys
import yaml
import argparse


from functools import reduce


CI_NAME = '.gitlab-ci.yml'

parser = argparse.ArgumentParser()

parser.add_argument('location')
parser.add_argument('--stage', nargs='+', type=str)

args = parser.parse_args()

ci_file = os.path.join(args.location, CI_NAME)

location = args.location


def aj(*args):
    return os.path.abspath(reduce(os.path.join, args))


def search_near_gitlab_ci(location):
    folder_to_search = ['..', *os.listdir()]

    for folder in folder_to_search:
        if os.path.exists(aj(location, folder, CI_NAME)):
            return True, aj(location, folder)

    return False, ''


def run_ci(location, ci_file, stage_to_run):
    print('Running ci on {} with file {}'.format(location, ci_file))

    command_to_skip = ['image', 'before_script', 'stages']

    with open(ci_file, 'r') as file:
        y = yaml.load(file, Loader=yaml.FullLoader)

        if stage_to_run == '__all__':
            stage_to_run = y.keys()

        print('Stage found:\n\t* \033[92;1m{}\033[0m'.format('\n\t\033[0;1m* \033[92m'.join(filter(lambda x: x not in command_to_skip, stage_to_run))))

        for command in stage_to_run:
            if command not in command_to_skip:
                output = sh.gitlab_runner.bake(_cwd=location, _out=sys.stdout, _err=sys.stderr).exec.shell.bake(command)()
                print(output)


if not os.path.exists(ci_file):
    print('\033[91mNo .gitlab-ci.yml found, searching near yml...\033[0m')

    is_present, location = search_near_gitlab_ci(location)

    if not is_present:
        sys.exit(1)

    print('\033[92;1mFound {} here {}, continuing ...\033[0m'.format(CI_NAME, location))

    ci_file = aj(location, CI_NAME)

stages = args.stage
if not stages:
    stages = '__all__'

run_ci(location, ci_file, stages)
