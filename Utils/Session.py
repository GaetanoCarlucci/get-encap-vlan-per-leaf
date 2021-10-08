#!/usr/bin/env python
#
#   Author: Gaetano Carlucci, Cisco CX
#   Python Version: 3
#
#   This software is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class Session(object):
    def __init__(self, apic_ip, apic_port, user, passwd):
        self.ip = apic_ip
        self.port = apic_port
        self.user = user
        self.passwd = passwd
        self.cookie = ''

    def set_cookie(self,cookie):
        self.cookie = cookie

    def get_cookie(self):
        try:
            auth_url = "https://%s:%s/api/mo/aaaLogin.xml" % (self.ip, self.port)
            auth_xml = "<aaaUser name='%s' pwd ='%s'/>" % (self.user, self.passwd)
            print("Getting cookie from %s" % self.ip)
            session = requests.post(auth_url, data=auth_xml, verify=False, timeout=5)
            return session.cookies
        except requests.exceptions.Timeout:
            print("APIC %s timed out " % (self.ip))
        except requests.exceptions.ConnectionError:
            print("Connection error can't logging to APIC %s with user %s" % (self.ip, self.user))

    def apic_json_get(self, url):
        get_json_url = "https://%s:%s/api/class/%s.json" % (self.ip, self.port, url)
        json_get = requests.get(get_json_url, cookies=self.cookie, verify=False)
        print(get_json_url)
        if json_get.status_code != 200:
            print(json_get.text)
        else:
            return json_get.text