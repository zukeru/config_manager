# Config Overwatch by Grant Zukel

#Description

config_overwatch uses a github repo to manage application configs. This process is an agent that needs to run locally on each 
instance that needs to be managed. In side your github repo for configs you have to create an enviroment folder, application folder, and config.
The process will check that the local copy of the config repo is up todate with what is in github. If it is not uptodate it will then do a pull request
and do an in place replacement of the config at the specified location. There is an option to reload your application service but it must be set up as a service.

#Install
	

#Config_overwatch Config.
The config manager config should be set at install. 

<dl>
  <dt>How to install</dt>
  <dd>Clone the repo, and edit the config.ini to point to your github repo.</dd>
  <dd>Currently you have to setup ssh keys for github, there is no feature to include a username and password.        https://help.github.com/articles/generating-ssh-keys/</dd>
</dl>

<dl>
  <dt>Config ini</dt>
  <dd>[Github]</dd>
  <dd>config_repo = configs this is the name of the repo in github that holds your configs.</dd>
  <dd>config_url = https://github.com/zukeru/configs.git</dd>
  <dd>update_interval = 120 this is the sleep interval for the time between config checks in seconds.</dd>
  <dd>enviroment = /dev this is the first folder representing your enviroment in your config repo in github.</dd>
  <dd>application_name = /config_overwatch this is the name of the folder representing your application in the configs/evn/application folder in your config repo.</dd>
  <dd>restart_application = false this is the option to reload applications in place when configs change, false by default.</dd>
  <dd>config_name = /config.ini this is the name of your config. The config name in your repo must be the same as the name of the config for your app.</dd>
  <dd>config_location = /Users/grantzukel/Documents/WorkScripts/PythonScripts/config_overwatch this is the location of the config you want to replace without the name.</dd>
  <dd>repo_location = /Users/grantzukel/Documents/WorkScripts/PythonScripts/ this is the location where you cloned your config repo.</dd>
</dl>
