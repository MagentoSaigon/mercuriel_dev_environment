# build.py
from fabric.api import *
import yaml
with open('servers.yml', 'r') as f:
    servers = yaml.load(f)

LOCAL_REPO_DIR = servers["local"]["git_path"]
LOCAL_MEDIA_DIR = LOCAL_REPO_DIR + "/src/magento/media"
LOCAL_BIN_DIR = servers["local"]["bin_path"]
MAGE_DIR = servers["staging"]["magento_path"]
ROOT_DIR = servers["staging"]["root_path"]
SCRIPTS_DIR = servers["staging"]["scripts_path"]
BIN_DIR = servers["staging"]["bin_path"]
MAGERUN = BIN_DIR + "/magerun"
MEDIA_FOLDER = MAGE_DIR + "/media"

env.hosts = [servers["staging"]["address"]]
env.user = "gahlanch"
env.key_filename = "~/.ssh/id_rsa"
env.port = 22

@parallel
def deploy():
 print("Update local git")
 local('cd ' + LOCAL_REPO_DIR)
 local('git pull origin master')

 print("Sniff code")
 local('cd ' + LOCAL_REPO_DIR + '&& bin/codesniff.sh')

 print("Set maintenance flag")
 with cd(MAGE_DIR):
  run("touch maintenance.flag")

 print("Updating source code on deployment server")
 with cd(ROOT_DIR):
  run("git pull origin master")

 print("Updating dependencies")
 with cd(BIN_DIR):
  run("composer update")

 print("Cleaning cache")
 with cd(MAGE_DIR):
  run("%s cache:clean" % MAGERUN)
  run("%s cache:flush" % MAGERUN)

 print("Running install and update scripts")
 with cd(MAGE_DIR):
  run("%s sys:setup:run" % MAGERUN)

 print("Setting maintenance mode OFF")
 with cd(MAGE_DIR):
  run("rm maintenance.flag")

def catalogImport():
 print("Importing attributes")
 with cd(SCRIPTS_DIR):
  run("php importCategories.php -f Categories.csv")

 print("Importing products")
 with cd(SCRIPTS_DIR):
  run("php createProducts.php -f Catalogue.csv --delimiter semicolon")

 print("Creating diamonds")
 with cd(SCRIPTS_DIR):
  run("php createProducts.php -c config.json -g")

 print("Cleaning cache")
 with cd(MAGE_DIR):
  run("%s cache:clean" % MAGERUN)
  run("%s cache:flush" % MAGERUN)

def syncMedia():
 print("Transfer media folder to the staging server")
 run('mkdir -p ' + MEDIA_FOLDER)
 put(LOCAL_MEDIA_DIR , MAGE_DIR)