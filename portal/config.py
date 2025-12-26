#o Config e responsavel por configurar as variaveis de ambiente 
import os 
from dynaconf import FlaskDynaconf

HERE=os.path.dirname(os.path.abspath(__file__))

def configure(app):
    FlaskDynaconf(app,extensIon_list="EXTENSION",root_path=HERE)

 