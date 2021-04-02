from setuptools import setup,find_packages

setup(
    name='pi-vii_backend',
    version='1.0',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['Flask','python-dotenv','psycopg2-binary','flask-sqlalchemy','Flask-Migrate','PyJWT','flask-cors','qrcode','numpy','Pillow','requests']
)