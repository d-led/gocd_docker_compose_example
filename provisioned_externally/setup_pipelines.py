from urlwait import wait_for_url
import requests
import sys
import time
import re

requests.packages.urllib3.disable_warnings()

url = "http://go-server:8153"
url_ssl = "https://go-server:8154"
config_url = url_ssl + "/go/api/admin/config.xml"

print("Waiting for " + url)
if not wait_for_url(url, 300):
    print("Go server did not start in a timely fashion. Please retry docker-compose up provisioner")
    sys.exit()

print("Go server is up...")

print("Sleeping a bit...")
time.sleep(100)

orig = requests.api.request('get', config_url, verify=False)
md5 = orig.headers['x-cruise-config-md5']
# remove old config
xml_old = re.sub(r'(?is)<config-repos>.+</config-repos>', '', orig.text)
# remove <pipelines group="defaultGroup" />
xml_old = re.sub(r'(?is)<pipelines group.+/>', '', xml_old)
# set the standard autoregistration key 123456789abcdef
xml_old = re.sub(r'(?is)agentAutoRegisterKey=\".*?\"', 'agentAutoRegisterKey=\"123456789abcdef\"', xml_old)

repos = """<config-repos>
  <config-repo plugin="yaml.config.plugin">
    <git url="https://github.com/downtrev/tdawg-yaml-config.git" />
  </config-repo>
  <config-repo plugin="yaml.config.plugin">
    <git url="https://github.com/d-led/automatic-lua-property-tables.git" />
  </config-repo>
  <config-repo plugin="yaml.config.plugin">
    <git url="https://github.com/d-led/dont_wait_forever_for_the_tests.git" />
  </config-repo>
</config-repos>
<pipelines group="defaultGroup" />
"""

xml_new = xml_old.replace("</cruise>", repos+"</cruise>")

data = {'xmlFile': xml_new, 'md5': md5}

post = requests.api.request('post', config_url, data=data, verify=False)

print("Updating the pipeline config: "+str(post))

print(xml_new)
