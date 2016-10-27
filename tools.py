import os
import jinja2
from webapp2_extras import json


class Config:

    def jinja_env(self, view_dir):
        template_dir = self.views_dir[view_dir]
        return jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                                  extensions=['jinja2.ext.autoescape'],
                                  autoescape=True)

    current_dir = os.path.dirname(__file__)
    views_dir = {'views': '%s/static/' % current_dir}

    config = {
        'template': jinja_env
    }


def json_in(handler):
    def json_decode(self, *args, **kwargs):
        try:
            self.request.json = json.decode(self.request.body)
        except ValueError:
            self.abort(400, 'Invalid client json')
        else:
            return handler(self, *args, **kwargs)

    return json_decode


def json_out(data):
    return json.encode(data)
