from __future__ import unicode_literals

import logging

import ckan.lib.base as base
import ckan.plugins.toolkit as toolkit
from ckanext.oauth2 import oauth2
from ckanext.oauth2 import constants

from ckan.lib.base import h, BaseController, render, abort, request
from ckan import model
from ckan.common import c
from ckan.logic import check_access, get_action, clean_dict, tuplize_dict, ValidationError, parse_params
from ckan.lib.navl.dictization_functions import unflatten


log = logging.getLogger(__name__)


class OnesaitPlatformController(base.BaseController):

    def __init__(self):
        self.oauth2helper = oauth2.OAuth2Helper()

    def login(self):
        log.debug('login with Onesait Platform Controller')

        # Log in attemps are fired when the user is not logged in and they click
        # on the log in button

        # Get the page where the user was when the loggin attemp was fired
        # When the user is not logged in, he/she should be redirected to the dashboard when
        # the system cannot get the previous page
        # came_from_url = _get_previous_page(constants.INITIAL_PAGE)
        root_path = toolkit.config.get('ckan.root_path', None)
        locale = toolkit.config.get('ckan.locale_default','en')
        came_from_url = toolkit.config.get('ckan.site_url', None)
        if root_path != None:
            root_path = root_path.replace("{{LANG}}",locale)
            came_from_url += root_path + constants.INITIAL_PAGE
        else:
            came_from_url += constants.INITIAL_PAGE
        log.debug('login redirect to {0}'.format(came_from_url))
        self.oauth2helper.challenge(came_from_url)

    def add_comment(self, dataset_id):
        return self._add_or_reply_comment(dataset_id)

    def edit_comment(self, dataset_id, comment_id):

        context = {'model': model, 'user': c.user}
        data_dict = {'id': dataset_id}
        check_access('package_show', context, data_dict)

        try:
            c.pkg_dict = get_action('package_show')(context, {'id': dataset_id})
            c.pkg = context['package']
        except:
            abort(403)

        if request.method == 'POST':
            data_dict = clean_dict(unflatten(tuplize_dict(parse_params(request.POST))))
            data_dict['id'] = comment_id
            success = False
            try:
                res = get_action('comment_update')(context, data_dict)
                success = True
            except ValidationError, ve:
                log.debug(ve)
            except Exception, e:
                log.debug(e)
                abort(403)

            if success:
                root_path = toolkit.config.get('ckan.root_path','')
                root_path = root_path.replace('{{LANG}}',h.lang())
                if root_path == '':
                    root_path = h.lang()
                h.redirect_to(str('/%s/dataset/%s#comment_%s' % (root_path, c.pkg.name, res['id'])))

            return render("package/read.html")

    def reply_comment(self, dataset_id, parent_id):
        c.action = 'reply'

        try:
            data = {'id': parent_id}
            c.parent_dict = get_action("comment_show")({'model': model, 'user': c.user},
                                                       data)
            c.parent = data['comment']
        except:
            abort(404)

        return self._add_or_reply_comment(dataset_id)

    def _add_or_reply_comment(self, dataset_id):
        """
       Allows the user to add a comment to an existing dataset
       """
        context = {'model': model, 'user': c.user}

        # Auth check to make sure the user can see this package

        data_dict = {'id': dataset_id}
        check_access('package_show', context, data_dict)

        try:
            c.pkg_dict = get_action('package_show')(context, {'id': dataset_id})
            c.pkg = context['package']
        except:
            abort(403)

        if request.method == 'POST':
            data_dict = clean_dict(unflatten(
                tuplize_dict(parse_params(request.POST))))
            data_dict['parent_id'] = c.parent.id if c.parent else None
            data_dict['url'] = '/dataset/%s' % c.pkg.name
            success = False
            try:
                res = get_action('comment_create')(context, data_dict)
                success = True
            except ValidationError, ve:
                log.debug(ve)
            except Exception, e:
                log.debug(e)
                abort(403)

            if success:
                root_path = toolkit.config.get('ckan.root_path','')
                root_path = root_path.replace('{{LANG}}',h.lang())
                if root_path == '':
                   root_path = h.lang()
                h.redirect_to(str('/%s/dataset/%s#comment_%s' % (root_path, c.pkg.name, res['id'])))

        return render("package/read.html")

    def delete_comment(self, dataset_id, comment_id):

        context = {'model': model, 'user': c.user}
        data_dict = {'id': dataset_id}
        check_access('package_show', context, data_dict)

        try:
            c.pkg_dict = get_action('package_show')(context, {'id': dataset_id})
            c.pkg = context['package']
        except:
            abort(403)

        try:
            data_dict = {'id': comment_id}
            get_action('comment_delete')(context, data_dict)
        except Exception, e:
            log.debug(e)
        
        root_path = toolkit.config.get('ckan.root_path','')
        root_path = root_path.replace('{{LANG}}',h.lang())
        if root_path == '':
            root_path = h.lang()
        h.redirect_to(str('/%s/dataset/%s' % (root_path, c.pkg.name)))

        return render("package/read.html")