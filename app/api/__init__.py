# coding=utf-8
from flask import Blueprint

api = Blueprint('api', __name__)

# Import any endpoints here to make them available
# from . import dis_endpoint, dat_endpoint
from . import institution  # Instutuição de Ensino
from . import examination  # Concurso
from . import course       # Curso
from . import subject      # Área de Conhecimento
from . import question     # Pergunta
