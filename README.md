# Gitlab-ci-runner

## How to use
* Export the path to your `PATH` variable
* run `run_ci` to run the ci on local
* If no `.gitlab-ci.yml` file is found where the command is run, it will search first on the parent dir, and the for each of this children

## Dependencies
* Python 3.5
* gitlab-runner

## Options
### stage

 You can run `run_ci --stage arg1 ... argn` to run only the matching name
