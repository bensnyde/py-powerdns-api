"""
Python Library for PowerDNS REST API

        http://doc.powerdns.com/md/httpapi/api_spec/

"""

import requests
import json

class PowerDNS:
    def __init__(self, base_url, apikey):
        self.base_url = base_url
        self.apikey = apikey

    def _query(self, uri, method, **kwargs):
        headers = {'X-API-Key': self.apikey, 'Accept': 'application/json'}
        url = self.base_url+uri

        if kwargs:
                kwargs = json.dumps(kwargs)

        if method == "GET":
            request = requests.get(url, headers=headers)
        elif method == "POST":
            request = requests.post(url, headers=headers, data=kwargs)
        elif method == "PUT":
            request = requests.put(url, headers=headers, data=kwargs)
        elif method == "PATCH":
            request = requests.patch(url, headers=headers, data=kwargs)
        elif method == "DELETE":
            request = requests.delete(url, headers=headers)

        return request.json()

    def list_zones(self):
        return self._query("/servers/localhost/zones", "GET")

    def get_zone(self, domain):
        return self._query("/servers/localhost/zones/%s" % domain, "GET")

    def create_zone(self, domain):
        data = {
                'kind': 'Native',
                'nameservers': ['ns1.example.com', 'ns2.example.com'],
                'name': domain
        }

        return self._query("/servers/localhost/zones", "POST", **data)

    def delete_zone(self, domain):
        return self._query("/servers/localhost/zones/%s" % domain, "DELETE")

    def set_zone_records(self, domain, rrsets):
        """
            changetype Must be REPLACE or DELETE.

            With DELETE, all existing RRs matching name and type will be deleted, incl. all comments.

            With REPLACE: when records is present, all existing RRs matching name and type will be deleted, and then new records given in records will be created.
            If no records are left, any existing comments will be deleted as well.

            When comments is present, all existing comments for the RRs matching name and type will be deleted, and then new comments given in comments will be created.

            rrsets example:

                                [{
                                            'type': 'A',
                                            'name': 'mail.example.com',
                                            'changetype': 'delete'
                                        },
                                        {
                                            'type': 'MX',
                                            'name': 'example.com',
                                            'changetype': 'replace',
                                            'records': [{'content': '0 example.com',
                                                      'disabled': False,
                                                      'name': 'example.com',
                                                      'ttl': 600,
                                                      'type': 'MX'}],
                                        }
                                ]
        """
        data = {
            'rrsets': rrsets
        }

        return self._query("/servers/localhost/zones/%s" % domain, "PATCH", **data)


pdns = PowerDNS("http://127.0.0.1:8081", "changeme")
print pdns.create_zone("fdsafdsa.com")
print pdns.get_zone("fdsafdsa.com")

a = [{
            'type': 'A',
            'name': 'mail.example.com',
            'changetype': 'delete'
        },
        {
            'type': 'MX',
            'name': 'example.com',
            'changetype': 'replace',
            'records': [{'content': '0 example.com',
                      'disabled': False,
                      'name': 'example.com',
                      'ttl': 600,
                      'type': 'MX'}],
        }
]

#print pdns.set_zone_records("example.com", a)
