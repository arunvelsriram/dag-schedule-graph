from setuptools import setup, find_packages

install_requires = [
    'apache-airflow>=1.10.4'
]

extras_require = {
    'dev': [
        'psycopg2',
        'pytest',
        'pytest-env',
        'ipython'
    ]
}

setup(
    name='dag-schedule-graph',
    version='0.1.0',
    download_url='https://github.com/arunvelsriram/dag-schedule-graph/archive/v0.1.0.tar.gz',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url='https://github.com/arunvelsriram/dag-schedule-graph',
    license='MIT',
    author='Arunvel Sriram',
    author_email='arunvelsriram@gmail.com',
    description='Airflow plugin for visualising DAG schedules within 24 hour window of a day.',
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'airflow.plugins': [
            'DAGScheduleGraphPlugin = dag_schedule_graph:DAGScheduleGraphPlugin'
        ]
    }
)
