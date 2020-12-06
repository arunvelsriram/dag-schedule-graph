from os import path
from setuptools import setup, find_packages

install_requires = [
    'apache-airflow>=1.10.4'
]

extras_require = {
    'dev': [
        'psycopg2',
        'pytest',
        'pytest-env',
        'ipython',
        'twine'
    ]
}

this_dir = path.abspath(path.dirname(__file__))
with open(path.join(this_dir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dag-schedule-graph',
    version='0.1.1',
    download_url='https://github.com/arunvelsriram/dag-schedule-graph/archive/v0.1.1.tar.gz',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url='https://github.com/arunvelsriram/dag-schedule-graph',
    license='MIT',
    author='Arunvel Sriram',
    author_email='arunvelsriram@gmail.com',
    description='Airflow plugin for visualising DAG schedules within 24 hour window of a day.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'airflow.plugins': [
            'DAGScheduleGraphPlugin = dag_schedule_graph:DAGScheduleGraphPlugin'
        ]
    }
)
