import os
import unittest
import responses
from fabric.api import task

from fabric_digitalocean.decorators import droplets, TokenError


class TestDecorators(unittest.TestCase):

    def setUp(self):
        super(TestDecorators, self).setUp()

        os.environ["FABRIC_DIGITALOCEAN_TOKEN"] = "afaketokenformockingthings"
        self.base_url = "https://api.digitalocean.com/v2/"

    def load_from_file(self, json_file):
        cwd = os.path.dirname(__file__)
        with open(os.path.join(cwd, 'fixtures/%s' % json_file), 'r') as f:
            return f.read()

    def test_tokenerror(self):
        os.environ["FABRIC_DIGITALOCEAN_TOKEN"] = ""

        with self.assertRaises(TokenError) as context:
            @droplets(ids=3164444)
            def dummy():
                pass

        self.assertTrue('The environmental variable FABRIC_DIGITALOCEAN_TOKEN'
                        in str(context.exception))

    @responses.activate
    def test_droplets_with_id(self):
        data = self.load_from_file('3164444.json')

        url = self.base_url + 'droplets/3164444'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        @droplets(ids=3164444)
        @task
        def dummy():
            pass

        hosts = list(dummy.hosts)

        self.assertItemsEqual(hosts, ["104.131.186.241"])

    @responses.activate
    def test_droplets_with_ids(self):
        data1 = self.load_from_file('3164444.json')
        data2 = self.load_from_file('8193577.json')

        url1 = self.base_url + 'droplets/3164444'
        responses.add(responses.GET, url1,
                      body=data1,
                      status=200,
                      content_type='application/json')

        url2 = self.base_url + 'droplets/8193577'
        responses.add(responses.GET, url2,
                      body=data2,
                      status=200,
                      content_type='application/json')

        @droplets(ids=[3164444, 8193577])
        @task
        def dummy():
            pass

        hosts = list(dummy.hosts)

        self.assertItemsEqual(hosts, ["104.131.186.241", "104.131.187.242"])

    @responses.activate
    def test_droplets_with_region(self):
        data = self.load_from_file('droplets.json')

        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        @droplets(region='nyc3')
        @task
        def dummy():
            pass

        hosts = list(dummy.hosts)

        self.assertItemsEqual(hosts, ["104.236.32.182", "104.236.32.412"])

    @responses.activate
    def test_droplets_with_tag(self):
        data = self.load_from_file('droplets.json')

        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        @droplets(tag='awesome')
        @task
        def dummy():
            pass

        hosts = list(dummy.hosts)

        self.assertItemsEqual(hosts,
                              ["104.236.32.182",
                               "104.236.32.224",
                               "104.236.32.412"])

    @responses.activate
    def test_droplets_with_tag_and_region(self):
        data = self.load_from_file('droplets.json')

        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        @droplets(tag='awesome', region='nyc3')
        @task
        def dummy():
            pass

        hosts = list(dummy.hosts)

        self.assertItemsEqual(hosts, ["104.236.32.182", "104.236.32.412"])

    @responses.activate
    def test_droplets_with_region_and_tag(self):
        data = self.load_from_file('droplets.json')

        url = self.base_url + 'droplets/'
        responses.add(responses.GET, url,
                      body=data,
                      status=200,
                      content_type='application/json')

        @droplets(region='nyc2', tag='awesome')
        @task
        def dummy():
            pass

        hosts = list(dummy.hosts)

        self.assertItemsEqual(hosts, ["104.236.32.224"])
