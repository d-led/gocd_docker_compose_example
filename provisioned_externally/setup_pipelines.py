import requests
from requests import get
import sys
import time
import re

requests.packages.urllib3.disable_warnings()

url = "http://go-server:8153"
health_url = url + "/go/api/v1/health"
url_ssl = "https://go-server:8154"
config_url = url_ssl + "/go/api/admin/config.xml"
retries = 30
sleep_seconds = 10

print("Waiting for " + health_url)
sys.stdout.flush()

for i in range(retries + 1):
    try:
        if "OK" in get(health_url).text:
            break
    except:
        print("not yet...")
        sys.stdout.flush()

    if i == retries:
        print("Go server did not start in a timely fashion. Please retry docker-compose up provisioner")
        sys.exit()

    time.sleep(sleep_seconds)

print("Go server is up...")
sys.stdout.flush()

print("Sleeping a bit...")
sys.stdout.flush()

time.sleep(10)

orig = requests.api.request('get', config_url, verify=False)
md5 = orig.headers['X-CRUISE-CONFIG-MD5']
# remove old config
xml_old = re.sub(r'(?is)<config-repos>.+</config-repos>', '', orig.text)
# remove <pipelines group="defaultGroup" />
xml_old = re.sub(r'(?is)<pipelines group.+/>', '', xml_old)
# set the standard autoregistration key 123456789abcdef
xml_old = re.sub(r'(?is)agentAutoRegisterKey=\".*?\"', 'agentAutoRegisterKey=\"123456789abcdef\"', xml_old)

repos = """<config-repos>
    <config-repo pluginId="yaml.config.plugin" id="gocd-rpi-unicorn-hat-monitor">
      <git url="https://github.com/d-led/gocd-rpi-unicorn-hat-monitor.git" />
    </config-repo>
    <config-repo pluginId="yaml.config.plugin" id="automatic-lua-property-tables">
      <git url="https://github.com/d-led/automatic-lua-property-tables.git" />
    </config-repo>
    <config-repo pluginId="yaml.config.plugin" id="dont_wait_forever_for_the_tests">
      <git url="https://github.com/d-led/dont_wait_forever_for_the_tests.git" />
    </config-repo>
</config-repos>
<pipelines group="defaultGroup" />
"""

xml_new = xml_old.replace("</cruise>", repos+"</cruise>")

headers = {'Confirm': 'true'}

data = {'xmlFile': xml_new, 'md5': md5}

post = requests.api.request('post', config_url, data=data, headers=headers, verify=False)

print("Updating the pipeline config: "+str(post) + " " + str(post.content))

print(xml_new)
