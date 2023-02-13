#Init file for metrics
from flask import Blueprint

bp = Blueprint("metrics", __name__)

from web.metrics import metrics