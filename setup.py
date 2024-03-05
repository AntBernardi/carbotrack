from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='carbotrack',
      version="0.0.0",
      description="Predict insulin dose recommandation regarding carbs identified",
      author="AntBernardi, C4ND1CE, DaLiryc",
      author_email="",
      #url="https://github.com/AntBernardi/carbotrack.git",
      install_requires=requirements,
      packages=find_packages(),
      test_suite="tests",
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
