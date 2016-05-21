"""
Python Library for PowerDNS REST API

        http://doc.powerdns.com/md/httpapi/api_spec/

Author: Benton Snyder
Website: http://bensnyde.me
Created: 2/21/15
Revised: 5/17/16

"""
import requests
import json


class PowerDNS:
    def __init__(self, base_url, apikey):
        self.base_url = base_url
        self.apikey = apikey

    def _query(self, uri, method, kwargs):
        headers = {
            'X-API-Key': self.apikey,
            'Accept': 'application/json'
        }

        if method == "GET":
            request = requests.get(self.base_url+uri, headers=headers)
        elif method == "POST":
            request = requests.post(self.base_url+uri, headers=headers, data=kwargs)
        elif method == "PUT":
            request = requests.put(self.base_url+uri, headers=headers, data=kwargs)
        elif method == "PATCH":
            request = requests.patch(self.base_url+uri, headers=headers, data=kwargs)
        elif method == "DELETE":
            request = requests.delete(self.base_url+uri, headers=headers)

        return request.json()

    def list_zones(self):
        return self._query("/servers/localhost/zones", "GET")

    def get_zone(self, domain):
        return self._query("/servers/localhost/zones/%s" % domain, "GET")

    def create_zone(self, domain):
        return self._query("/servers/localhost/zones", "POST", {
                'kind': 'Native',
                'nameservers': ['ns1.example.com', 'ns2.example.com'],
                'name': domain
        })

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
            }]
        """
        return self._query("/servers/localhost/zones/%s" % domain, "PATCH", {
            'rrsets': rrsets
        })
