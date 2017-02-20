# Copyright (c) 2016 Mirantis, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import itertools
import time

from oslo_log import log as logging
import requests

from fuxi_kubernetes import constants
from fuxi_kubernetes import exceptions as exc

LOG = logging.getLogger(__name__)


class FuxiClient(object):
    def __init__(self, base_url):
        self._base_url = 'http://' + base_url + '/VolumeDriver.'

    def get(self, data):
        LOG.debug("Get %(data)s", {'data': data})
        url = self._base_url + 'Get'
        response = requests.post(url, json=data)
        if not response.ok:
            raise exc.FuxiClientException(response.text)
        return response.json()

    def create(self, data):
        LOG.debug("Create %(data)s", {'data': data})
        url = self._base_url + 'Create'
        response = requests.post(url, json=data)
        if not response.ok:
            raise exc.FuxiClientException(response.text)
        # for attempts in itertools.count(1):
        #     if self.get(data)['Err'] != 'Volume Not Found':
        #         LOG.debug("Creating volume finish in %(se)s seconds",
        #                   {"se": attempts})
        #         break
        #     if attempts > constants.DEFAULT_TIMEOUT:
        #         return constants.FUXI_TIMEOUT_CODE
        #     time.sleep(1)
        return response.json()

    def delete(self, data):
        LOG.debug("Delete %(data)s", {'data': data})
        url = self._base_url + 'Remove'
        response = requests.post(url, json=data)
        if not response.ok:
            raise exc.FuxiClientException(response.text)
        return response.json()

    def mount(self, data):
        LOG.debug("Mount %(data)s", {'data': data})
        url = self._base_url + 'Mount'
        response = requests.post(url, json=data)
        if not response.ok:
            raise exc.FuxiClientException(response.text)
        return response.json()

    def unmount(self, data):
        LOG.debug("Unmount %(data)s", {'data': data})
        url = self._base_url + 'Unmount'
        response = requests.post(url, json=data)
        if not response.ok:
            raise exc.FuxiClientException(response.text)
        return response.json()
