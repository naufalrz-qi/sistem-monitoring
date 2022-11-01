from flask import request, Blueprint, redirect, url_for 

site_guru = Blueprint('site_guru', __name__, url_prefix='/guru')