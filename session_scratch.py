import bottle
from beaker.middleware import SessionMiddleware

session_opts = {
    'session.type':'memory',
    'session.auto':True,
    'session.cookie_expires':300
}
app = SessionMiddleware(bottle.app(), session_opts)

@bottle.route('/test')
def test():
    s = bottle.request.environ.get('beaker.session')
    s['test']= s.get('test',0) + 1
    s.save()
    return f'Test counter {s.get("test")}'

bottle.run(app=app)