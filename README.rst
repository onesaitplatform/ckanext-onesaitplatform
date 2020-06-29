=======================
ckanext-onesaitplatform
=======================

Extension and theme for OnesaitPlatform Data Portal.


------------
Requirements
------------

This extension works with CKAN versions 2.8.X

It is necessary to install and activate these extensions:
    - ckanext-showcase
    - ckanext-oauth2


------------
Installation
------------

To install ckanext-onesaitplatform:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-onesaitplatform Python package into your virtual environment::

     pip install ckanext-onesaitplatform

3. Add ``onesaitplatform`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).
   
NOTE: put ``onesaitplatform`` before any extension

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


---------------
Config Settings
---------------

Add these properties to the config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``):

- To activate js effects: 

    ckan.template_footer_end = <!-- CKAN onesaitplatform frontend controller -->
      <script type="text/javascript">
      $( window ).on( "load", function() { CKAN_Controller.init(); })
      </script>
      <!-- /CKAN onesaitplatform frontend controller -->

- If ckan is running with a non root_path set this property to true, else set it to false:

    ckan.login_onesait = true
 
 
------------------------
Development Installation
------------------------

To install ckanext-onesait for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/onesaitplatform/ckanext-onesaitplatform.git

    cd ckanext-onesaitplatform

    python setup.py develop

    pip install -r dev-requirements.txt

