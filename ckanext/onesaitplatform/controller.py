from __future__ import unicode_literals

import logging

import ckan.lib.base as base
import ckan.plugins.toolkit as toolkit
from ckanext.oauth2 import oauth2
from ckanext.oauth2 import constants

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
        came_from_url = None
        if root_path != None:
            root_path = root_path.replace("{{LANG}}",locale)
            came_from_url = root_path + constants.INITIAL_PAGE
        else:
            came_from_url = constants.INITIAL_PAGE

        self.oauth2helper.challenge(came_from_url)