# -*- coding: utf-8 -*-

from timeit import default_timer

from flask import Flask, request, g
from flask.ext.cdnjs import JSCDN
from flask.ext.themes import setup_themes
from flask.ext.babel import Babel
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.debug import DebuggedApplication

from helper.extensions import cache
from helper.wrapper import render
import views

BPModules = (
    (views.RootBP, ''),
    (views.ExampleBP, '/_ex'),
)


def create_app():
    app = Flask('application')
    app.config.from_object('application.settings')

    configExtensions(app)
    configi18n(app)
    requestWrap(app)
    requestDispatch(app)
    requestErrors(app)

    return app


def configExtensions(app):
    JSCDN(app)
    setup_themes(app)
    cache.init_app(app)

    if app.debug:
        DebugToolbarExtension(app)
        DebuggedApplication(app, evalex=True)


def configi18n(app):
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        accept_languages = app.config.get('accept_languages', ['en_us', 'zh_cn'])
        default_language = app.config.get('babel_default_locale', ['en_us'])

        lang = request.accept_languages.best_match(default_language)

        for language in request.accept_languages:
            lang = language[0].replace('-', '_')
            if lang in accept_languages:
                break

        return lang


def requestWrap(app):
    @app.before_request
    def before_request():
        g.starttime = default_timer()

    @app.after_request
    def after_request(response):
        time = (default_timer() - g.starttime) * 1000   # ms
        time = (time * 1000 + 5) // 10 / 100            # roundup and keep the last 2 semi digit
        response.data = response.data.replace('<|pagerendertime|>', str(time) + ' ms')
        return response


def requestDispatch(app):
    for bp, url_prefix in BPModules:
        app.register_blueprint(bp, url_prefix=url_prefix)


def requestErrors(app):
    ## Error handlers
    # Handle 404 errors
    @app.errorhandler(404)
    def page_not_found(e):
        return render('blackhole/404.html'), 404

    # Handle 500 errors
    @app.errorhandler(500)
    def server_error(e):
        return render('blackhole/500.html'), 500
