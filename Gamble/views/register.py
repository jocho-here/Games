import os
from flask import Blueprint
from config import users
from utils import wrap_string_into_html

register = Blueprint('register', __name__)


@register.route('/등록/<username>', methods=['GET'])
def register(username):
    registered_hosts = {}

    if os.path.exists('user_hosts.csv'):
        host_rows = [l.strip().strip(',') for l in open('user_hosts.csv', 'r').readlines()]
        registered_hosts = {host_rows[0][i]: host_rows[1][i] for i in range(len(host_rows[0]))}

    registered_hosts[username] = 
