from setuptools import setup, find_packages

install_requires = [
    'apache-airflow>=1.10.4',
    'croniter>=0.3.36'
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
    name='dag-timeline',
    version='0.1.0',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    url='',
    license='',
    author='Arunvel Sriram',
    author_email='arunvelsriram@gmail.com',
    description='Airflow plugin to show DAG schedules in a timeline',
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        'airflow.plugins': [
            'DAGTimelinePlugin = dag_timeline:DAGTimelinePlugin'
        ]
    }
)
