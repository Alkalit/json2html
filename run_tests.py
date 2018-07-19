import os.path

run_tests_command = "python -m unittest discover"

os.chdir('..')
os.system(run_tests_command)
