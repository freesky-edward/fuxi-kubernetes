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

import contextlib
import itertools

from oslo_log import log as logging
from oslo_serialization import jsonutils
import requests

from fuxi_kubernetes import  constants
from fuxi_kubernetes import exceptions as exc

LOG = logging.getLogger(__name__)


class K8sClient(object):
    # REVISIT(ivc): replace with python-k8sclient if it could be extended
    # with 'WATCH' support

    def __init__(self, base_url):
        self._base_url = base_url

    def get(self, path):
        LOG.debug("Get %(path)s", {'path': path})
        url = self._base_url + path
        response = requests.get(url)
        if not response.ok:
            raise exc.K8sClientException(response.text)
        return response.json()

    def post(self, path, data):
        LOG.debug("post %(path)s: %(data)s", {
            'path': path, 'data': data})
        url = self._base_url + path
        response = requests.post(url, json=data)
        if not response.ok:
            raise exc.K8sClientException(response.text)
        return response.json()

    def delete(self, path):
        LOG.debug("Delete %(path)s", {'path': path})
        url = self._base_url + path
        response = requests.delete(url)
        if not response.ok:
            raise exc.K8sClientException(response.text)
        return response.json()

    def watch(self, path):
        params = {'watch': 'true'}
        url = self._base_url + path

        # TODO(ivc): handle connection errors and retry on failure
        while True:
            with contextlib.closing(requests.get(url, params=params,
                                                 stream=True)) as response:
                if not response.ok:
                    raise exc.K8sClientException(response.text)
                for line in response.iter_lines(delimiter='\n'):
                    line = line.strip()
                    if line:
                        yield jsonutils.loads(line)

    def get_pvc(self, namespace, pvc_name):
        pvc_path = constants.K8S_API_NAMESPACES + "/" + namespace + \
                   "/persistentvolumeclaims/" + pvc_name
        pvc_status = self.get(pvc_path)
        return pvc_status
