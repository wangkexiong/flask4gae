# -*- coding:utf-8 -*-

from flask import Blueprint

from application.helper.wrapper import render


RootBP = Blueprint('RootBP', __name__)


@RootBP.route('/_ah/warmup')
def warmup():
    '''
    App Engine frequently needs to load application code into a fresh instance.
    This happens when you redeploy the application, when the load pattern has
    increased beyond the capacity of the current instances, or simply due to
    maintenance or repairs of the underlying infrastructure or physical hardware.

    Loading new application code on a fresh instance can result in
    loading requests. Loading requests can result in increased request latency
    for your users, but you can avoid this latency using warmup requests.
    Warmup requests load application code into a new instance before any live
    requests reach that instance.

    App Engine attempts to detect when your application needs a new instance,
    and (assuming that warmup requests are enabled for your application)
    initiates a warmup request to initialize the new instance.
    However, these detection attempts do not work in every case.
    As a result, you may encounter loading requests, even if warmup requests
    are enabled in your app. For example, if your app is serving no traffic,
    the first request to the app will always be a loading request,
    not a warmup request.

    Warmup requests use instance hours like any other request to your App Engine
    application. In most cases, you won't notice an increase in instance hours,
    since your application is simply initializing in a warmup reques
    t instead of a loading request.
    Your instance hour usage will likely increase if you decide to do more work
    (such as precaching) during a warmup request. If you set a minimum number
    of idle instance, you may encounter warmup requests when those instances
    first start, but they will remain available after that time.
    '''
    return ''


@RootBP.route('/')
def index():
    return 'Hello world'
