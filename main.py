import webapp2
import unirest
import tools
from google.appengine.api import mail
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment

class Main(webapp2.RequestHandler):

    def render_template(self, view_filename, template_dir=None, params=None):
        if params is None:
            params = {}
        view_dir = template_dir or 'views'
        jinja_env = tools.Config.config.get('template')
        template_env = jinja_env(tools.Config, view_dir).get_template(view_filename)
        self.response.write(template_env.render(params))

    def home(self):
        self.render_template('index.html')

    @tools.json_in
    def send_mail(self):
        name = self.request.json['name']
        from_email = self.request.json['email']
        body = self.request.json['message']
        output = {}

        if not mail.is_email_valid(from_email):
            output['message'] = 'Email Is Not Valid'
        else:
            mail.send_mail("mail@victor-com-ng.appspotmail.com", from_email, "Message from "+name+"  - WEBSITE", body)
            output['message'] = 'success'

        res = tools.json_out(output)
        self.response.content_type = 'application/json;charset=utf-8;'
        self.response.write(res)

    def get_route(self, start_point, end_point):
        url = "http://roadpreppers.com/api/Directions/GetRoutes/?StartingPoint={0}&EndPoint={1}".format(start_point, end_point);
        response = unirest.get(url)
        res = tools.json_out(response.body)
        self.response.content_type = 'application/json;charset=utf-8;'
        self.response.write(res);

    def verify(self, sentence):
        vs = vaderSentiment(sentence)
        res = tools.json_out(vs)
        self.response.content_type = 'application/json;charset=utf-8;'
        self.response.write(res)    

routes = [
    webapp2.Route(r'/', handler=Main, name='home', handler_method='home', methods=['GET']),
    webapp2.Route(r'/verify/<sentence>', handler=Main, name='verify', handler_method='verify', methods=['GET']),
    webapp2.Route(r'/get_route/<start_point>/<end_point>', handler=Main, name='getroute', handler_method='get_route', methods=['GET']),
    webapp2.Route(r'/send_mail', handler=Main, name='mail', handler_method='send_mail', methods=['POST']),
]

app = webapp2.WSGIApplication(routes=routes, config=tools.Config.config, debug=True)
