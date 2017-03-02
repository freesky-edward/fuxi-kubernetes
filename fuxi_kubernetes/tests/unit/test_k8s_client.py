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
import mock

from oslo_serialization import jsonutils

from fuxi_kubernetes import exceptions as exc
from fuxi_kubernetes import k8s_client
from fuxi_kubernetes.tests import base as test_base


class TestK8sClient(test_base.TestCase):
    def setUp(self):
        super(TestK8sClient, self).setUp()
        self.base_url = 'http://127.0.0.1:12345'
        self.client = k8s_client.K8sClient(self.base_url)

    @mock.patch('requests.get')
    def test_get(self, m_get):
        path = '/test'
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_get.return_value = m_resp

        self.assertEqual(ret, self.client.get(path))
        m_get.assert_called_once_with(self.base_url + path)

    @mock.patch('requests.get')
    def test_get_exception(self, m_get):
        path = '/test'

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_get.return_value = m_resp

        self.assertRaises(exc.K8sClientException, self.client.get, path)

    @mock.patch('requests.post')
    def test_post(self, m_post):
        path = '/test'
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_post.return_value = m_resp

        self.assertEqual(ret, self.client.post(path, ret))
        m_post.assert_called_once_with(self.base_url + path, json=ret)

    @mock.patch('requests.post')
    def test_post_exception(self, m_post):
        path = '/test'
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_post.return_value = m_resp

        self.assertRaises(exc.K8sClientException, self.client.post, path, ret)

    @mock.patch('requests.delete')
    def test_delete(self, m_delete):
        path = '/test'
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_delete.return_value = m_resp

        self.assertEqual(ret, self.client.delete(path))
        m_delete.assert_called_once_with(self.base_url + path)

    @mock.patch('requests.delete')
    def test_delete_exception(self, m_delete):
        path = '/test'

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_delete.return_value = m_resp

        self.assertRaises(exc.K8sClientException, self.client.delete, path)

    @mock.patch('requests.get')
    def test_watch(self, m_get):
        path = '/test'
        data = [{'obj': 'obj%s' % i} for i in range(3)]
        lines = [jsonutils.dumps(i) for i in data]

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.iter_lines.return_value = lines
        m_get.return_value = m_resp

        cycles = 3
        self.assertEqual(
            data * cycles,
            list(itertools.islice(self.client.watch(path),
                                  len(data) * cycles)))

        self.assertEqual(cycles, m_get.call_count)
        self.assertEqual(cycles, m_resp.close.call_count)
        m_get.assert_called_with(self.base_url + path, stream=True,
                                 params={'watch': 'true'})

    @mock.patch('requests.get')
    def test_watch_exception(self, m_get):
        path = '/test'

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_get.return_value = m_resp

        self.assertRaises(exc.K8sClientException, next,
                          self.client.watch(path))

    @mock.patch('requests.get')
    def test_get_pvc(self, m_get):
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_get.return_value = m_resp

        self.assertEqual(ret, self.client.get_pvc('default', 'test'))
