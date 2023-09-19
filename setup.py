


import src.download_google_files as DGF

#https://drive.google.com/file/d/1ogNrsg9iwD9M6EFHsACM9FLj2BgqZxUE/view?usp=drive_link
#file_id = "https://drive.google.com/file/d/1ZwoBFt2SZisuqLyj8eitTGn6bhufMyQD/view?usp=drive_link"

file_id = '1ZwoBFt2SZisuqLyj8eitTGn6bhufMyQD'
destination = 'data/processed/ags2'
DGF.download_file_from_google_drive(file_id, destination)

#from setuptools import find_packages, setup

#setup(
#    name='src',
#    packages=find_packages(),
#    version='0.1.0',
#    description='Strategies for allocation surveillance cameras',
#    author='R. Tapia-McLung and R. López-Farías',
#    license='',
#)
