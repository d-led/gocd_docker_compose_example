from urlwait import wait_for_url
import requests
import sys
import time

requests.packages.urllib3.disable_warnings()

url = "http://go-server:8153"
url_ssl = "https://go-server:8154"
config_url = url_ssl + "/go/api/admin/config.xml"

print("Waiting for " + url)
if not wait_for_url(url, 300):
    print("Go server did not start in a timely fashion. Please retry docker-compose up provisioner")
    sys.exit()

print("Go server is up...")

time.sleep(100)

orig = requests.api.request('get', config_url, verify=False)
md5 = orig.headers['x-cruise-config-md5']
xml_orig = orig.text

repos = """<config-repos>
  <config-repo plugin="yaml.config.plugin">
    <git url="https://github.com/d-led/gocd-rpi-unicorn-hat-monitor.git" />
  </config-repo>
</config-repos>
"""

xml_new = xml_orig.replace("<agents>",repos+"<agents>")

data = {'xmlFile': xml_new, 'md5': md5}

post = requests.api.request('post', config_url, data=data, verify=False)

print("Updating the pipeline config: "+str(post))

print(xml_new)
