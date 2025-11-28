from setuptools import setup 


setup(
    name = "portal_emprego" ,
    author= "Mauro Zacarias ",
    version="0.1.0",
    packages=["portal"],
    license = "apache" ,
    install_requires=["flask","Flask-SQLAlchemy","PyMySQL", "dynaconf","flask-bootstrap"]
) 