from setuptools import find_packages,setup
from typing import List


HYPHEN_DOT = ".e -"

def get_requirements(file_path:str) ->List[str]:
    '''
      this fn will return the list of  requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements = file_obj.readline()
        requirements = [req.strip() for req in requirements if req.strip()]  # Remove newline characters and empty lines


        if HYPHEN_DOT in requirements:
            requirements.remove(HYPHEN_DOT)

    return requirements

setup(
  name='ml-project',
  version='0.0.1',
  author='sanoj c sam',
  author_email = 'sanojcsam123@gmail.com',
  packages= find_packages(),
  install_requires = get_requirements('requirements.txt')
)