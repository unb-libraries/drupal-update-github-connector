# Drupal update github connector.
Web endpoint to permit Drupal modules to query updates from github directly.

## Setup
## Endpoint Setup
Ensure this runs in your web daemon : we use mod_python for apache2.
Copy githubOrgConfiguration.py.example to githubOrgConfiguration.py and populate values.

## Custom Module Configuration
Ensure the following settings are defined in your module.info:
+   project = project_machine_name_with_underscores
+   core = 8.x/7.x/6.x
+   version = 7.x-1.01
+   project status url = http://WebEndpoint

## Development Requirements
+   project name and github repository name must be exactly the same.
+   Modules must be developed in a branch named exactly the same as the 'core' string in the .info file.
+   Tags for releases must be exactly the same as the version string in the .info file.

## Dependencies :
+   pygithub
+   lxml