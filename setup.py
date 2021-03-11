from setuptools import setup,find_packages

setup(
    name='pi-vi_backend',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['redis','flask-mail','rq','Flask','python-dotenv','psycopg2-binary','flask-sqlalchemy','Flask-Migrate','PyJWT','flask-cors', 'flask-wtf']
)