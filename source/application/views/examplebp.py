# -*- coding:utf-8 -*-

from google.appengine.api import users
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

from flask import current_app, Blueprint, flash, redirect, request, url_for

from application.models import ExampleModel
from application.forms import ExampleForm
from application.helper.extensions import cache
from application.helper.wrapper import render
from decorators import login_required, admin_required

ExampleBP = Blueprint('ExampleBP', __name__)


@ExampleBP.route('/change')
def change():
    #debug purpose
    if current_app.config['THEME']:
        current_app.config['THEME'] = ''
    else:
        current_app.config['THEME'] = 'Bootstrap'

    return redirect(url_for('ExampleBP.list_examples'))


@ExampleBP.route('/hello/<username>')
def hello(username):
    return 'Hello %s' % username


@ExampleBP.route('/admin_only')
@admin_required
def require_admin():
    return 'Welcome administrator'


@ExampleBP.route('/', methods=['GET', 'POST'])
@login_required
def list_examples():
    examples = ExampleModel.query()
    form = ExampleForm()

    if request.method == 'POST' and form.validate_on_submit():
        example = ExampleModel(example_name=form.example_name.data,
                               example_description=form.example_description.data,
                               added_by=users.get_current_user())

        try:
            example.put()
            example_id = example.key.id()
            flash(u'Example %s successfully saved.' % example_id, 'success')
        except CapabilityDisabledError:
            flash(u'App Engine Datastore is currently in read-only mode.', 'info')

        return redirect(url_for('ExampleBP.list_examples'))

    return render('examples/list.html', examples=examples, form=form)


@ExampleBP.route('/cached')
@cache.cached(timeout=60)
def cached_examples():
    """This view should be cached for 60 sec"""
    examples = ExampleModel.query()
    return render('examples/list_cached.html', examples=examples)


@ExampleBP.route('/examples/<int:example_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_example(example_id):
    example = ExampleModel.get_by_id(example_id)
    form = ExampleForm(obj=example)

    if request.method == 'POST' and form.validate_on_submit():
        example.example_name = form.data.get('example_name')
        example.example_description = form.data.get('example_description')
        example.put()
        flash(u'Example %s successfully saved.' % example_id, 'success')
        return redirect(url_for('ExampleBP.list_examples'))

    return render('examples/edit.html', example=example, form=form)


@ExampleBP.route('/examples/<int:example_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_example(example_id):
    """Delete an example object"""
    example = ExampleModel.get_by_id(example_id)

    try:
        example.key.delete()
        flash(u'Example %s successfully deleted.' % example_id, 'success')
    except CapabilityDisabledError:
        flash(u'App Engine Datastore is currently in read-only mode.', 'info')

    return redirect(url_for('ExampleBP.list_examples'))
