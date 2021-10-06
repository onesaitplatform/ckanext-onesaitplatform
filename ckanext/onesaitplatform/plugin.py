import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckanext.showcase.logic as logic
import ckan.model as model
from ckan.common import c
import ckan.lib.helpers as h
from ckan.plugins import toolkit as tk
from ckan.lib.plugins import DefaultTranslation

def showcases_list_helper():
	showcases = tk.get_action('ckanext_showcase_list')({}, {})
	return showcases

def showcase_show_helper(id):
	showcase = tk.get_action('ckanext_showcase_show')({},{'id':id})
	return showcase

class OnesaitPlatformPlugin(plugins.SingletonPlugin, DefaultTranslation):
	plugins.implements(plugins.ITranslation)
	plugins.implements(plugins.IConfigurer)
	plugins.implements(plugins.ITemplateHelpers)
	plugins.implements(plugins.IRoutes, inherit=True)

	# IConfigurer

	def update_config(self, config_):
		toolkit.add_template_directory(config_, 'templates')
		toolkit.add_public_directory(config_, 'public')
		toolkit.add_resource('fanstatic', 'onesaitplatform')

	def get_helpers(self):
		return {
			'showcases_list_helper': showcases_list_helper,
			'showcase_show_helper': showcase_show_helper
		}

	def before_map(self, m):
		login_onesaitplatform = toolkit.config.get('ckan.onesaitplatform.login', False)
		if login_onesaitplatform:
			m.connect('/user/login',
                  controller='ckanext.onesaitplatform.controller:OnesaitPlatformController',
                  action='login')
		
		return m