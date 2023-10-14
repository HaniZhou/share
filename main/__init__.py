from flask import (Blueprint, )

view = Blueprint('view', __name__)

from .view import *
# 需要导入子包，运行；
#
