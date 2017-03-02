import os
import re
from os.path import dirname, join, exists
from envparse import env


ENVIRON = os.environ


def read_env(filename='local.env'):
    env_file = join(dirname(__file__), filename)
    if not exists(env_file):
        raise IOError('Cant find: {}'.format(filename))

    with open(env_file) as f:
        content = f.read()

    for line in content.splitlines():
        m1 = re.match(r'\A([A-Za-z_0-9]+)=(.*)\Z', line)
        if m1:
            key, val = m1.group(1), m1.group(2)
            m2 = re.match(r"\A'(.*)'\Z", val)
            if m2:
                val = m2.group(1)
            m3 = re.match(r'\A"(.*)"\Z', val)
            if m3:
                val = re.sub(r'\\(.)', r'\1', m3.group(1))

            print key
            print str(val)
            os.environ.setdefault(key, str(val))

