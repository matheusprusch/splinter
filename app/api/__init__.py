# coding=utf-8
from flask import Blueprint

api = Blueprint('api', __name__)

# Import any endpoints here to make them available
# from . import dis_endpoint, dat_endpoint
# This is necessary to be in the bottom. DO NOT MOVE IT
# If moved to the top it will generate a cyclic reference
from . import institution  # Instutuição de Ensino
from . import examination  # Concurso
from . import course       # Curso
from . import subject      # Área de Conhecimento
from . import question     # Pergunta
from . import user         # Usuário
from . import pretest      # Simulado
from . import practice     # Praticar
