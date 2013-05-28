# -*- coding:utf-8 -*-

from flask import Blueprint, current_app, url_for


def canMinimized(ext, minified):
    if ext == 'js' or ext == 'css':
        return minified
    else:
        return False


def cdnjs_find_resource(filename):
    config = current_app.config

    lib = ext = ''
    try:
        (lib, ext) = filename.rsplit('.', 1)
    except:
        lib = filename

    if canMinimized(ext, config['JS_USE_MINIFIED']):
        filename = '%s.min.%s' % (lib, ext)

    if not config['JS_USE_CDN']:
        return url_for('jscdn.static', filename=filename)
    else:
        baseurl = config['CDN_BASEURL']

        if baseurl.startswith('//') and config['CDN_PREFER_SSL']:
            baseurl = 'https:%s' % baseurl
        return baseurl + filename


class JSCDN(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('JS_USE_MINIFIED', True)
        app.config.setdefault('JS_USE_CDN', True)
        app.config.setdefault('CDN_PREFER_SSL', True)
        app.config.setdefault('CDN_BASEURL', '//cdnjs.cloudflare.com/ajax/libs/')

        blueprint = Blueprint(
            'jscdn',
            __name__,
            template_folder='templates',
            static_folder='static',
            static_url_path=app.static_url_path + '/cdn')

        app.register_blueprint(blueprint)

        app.jinja_env.filters['cdn_find_resource'] = cdnjs_find_resource
