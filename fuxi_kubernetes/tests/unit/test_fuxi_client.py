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

import mock

from fuxi_kubernetes import exceptions as exc
from fuxi_kubernetes import fuxi_client
from fuxi_kubernetes.tests import base as test_base


class TestFuxiClient(test_base.TestCase):
    def setUp(self):
        super(TestFuxiClient, self).setUp()
        self.base_url = '127.0.0.1:7879'
        self.client = fuxi_client.FuxiClient(self.base_url)

    @mock.patch('requests.post')
    def test_get(self, m_get):
        ret = {'Name': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_get.return_value = m_resp

        self.assertEqual(ret, self.client.get(ret))
        m_get.assert_called_once_with('http://' + self.base_url +
                                      '/VolumeDriver.Get', json=ret)

    @mock.patch('requests.post')
    def test_get_exception(self, m_get):
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_get.return_value = m_resp

        self.assertRaises(exc.FuxiClientException, self.client.get, ret)

    @mock.patch('requests.post')
    def test_create(self, m_create):
        ret = {'Name': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_create.return_value = m_resp

        self.assertEqual(ret, self.client.create(ret))
        m_create.assert_called_once_with('http://' + self.base_url +
                                         '/VolumeDriver.Create', json=ret)

    @mock.patch('requests.post')
    def test_create_exception(self, m_create):
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_create.return_value = m_resp

        self.assertRaises(exc.FuxiClientException, self.client.create, ret)

    @mock.patch('requests.post')
    def test_delete(self, m_delete):
        ret = {'Name': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_delete.return_value = m_resp

        self.assertEqual(ret, self.client.delete(ret))
        m_delete.assert_called_once_with('http://' + self.base_url +
                                         '/VolumeDriver.Remove', json=ret)

    @mock.patch('requests.post')
    def test_delete_exception(self, m_delete):
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_delete.return_value = m_resp

        self.assertRaises(exc.FuxiClientException, self.client.delete, ret)

    @mock.patch('requests.post')
    def test_mount(self, m_mount):
        ret = {'Name': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_mount.return_value = m_resp

        self.assertEqual(ret, self.client.mount(ret))
        m_mount.assert_called_once_with('http://' + self.base_url +
                                        '/VolumeDriver.Mount', json=ret)

    @mock.patch('requests.post')
    def test_mount_exception(self, m_mount):
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_mount.return_value = m_resp

        self.assertRaises(exc.FuxiClientException, self.client.mount, ret)

    @mock.patch('requests.post')
    def test_unmount(self, m_unmount):
        ret = {'Name': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = True
        m_resp.json.return_value = ret
        m_unmount.return_value = m_resp

        self.assertEqual(ret, self.client.unmount(ret))
        m_unmount.assert_called_once_with('http://' + self.base_url +
                                          '/VolumeDriver.Unmount', json=ret)

    @mock.patch('requests.post')
    def test_unmount_exception(self, m_unmount):
        ret = {'test': 'value'}

        m_resp = mock.MagicMock()
        m_resp.ok = False
        m_unmount.return_value = m_resp

        self.assertRaises(exc.FuxiClientException, self.client.unmount, ret)
