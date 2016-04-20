import webapp2
import jinja2
import os

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


class Main(webapp2.RequestHandler):

    def render_template(self, view_filename, template_dir=None, params=None):
        if params is None:
            params = {}
        view_dir = template_dir or 'views'
        jinja_env = Config.config.get('template')
        template_env = jinja_env(Config, view_dir).get_template(view_filename)
        self.response.write(template_env.render(params))

    def home(self):
        self.render_template('index.html')


routes = [
    webapp2.Route(r'/', handler=Main, name='home', handler_method='home', ),
]

app = webapp2.WSGIApplication(routes=routes, config=Config.config, debug=True)
