# Drupal module update github connector
Web endpoint to permit non-contrib Drupal modules to query for available updates from github repositories.

## Setup
### Endpoint Setup
+   Ensure that python is parsed by your webserver : we use mod_python for apache2.
+   Update RewriteBase in .htaccess to reflect your deployment point
+   Copy githubOrgConfiguration.py.example to githubOrgConfiguration.py and populate values.

### Custom Module Configuration
Ensure the following settings are defined in your module.info:
+   project = project_machine_name_with_underscores
+   core = 8.x/7.x/6.x
+   version = 7.x-1.01
+   project status url = http://WebEndpoint

## Development Requirements
+   project name and github repository name must be exactly the same.
+   Modules must be developed in a branch named exactly the same as the 'core' string in the .info file.
+   You MUST tag commits appropriately for this to work. Commit tags must be exactly the same as the version string in the .info file.

## Dependencies :
+   pygithub
+   lxml
