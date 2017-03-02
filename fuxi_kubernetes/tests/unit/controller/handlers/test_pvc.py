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

from fuxi_kubernetes import clients
from fuxi_kubernetes.controller.handlers import pvc as h_pvc
from fuxi_kubernetes import exceptions as exc
from fuxi_kubernetes.tests import base as test_base

PVC_UNBOUND = {
    'status': {'phase': 'unBound'},
    'metadata': {'name': 'test',
                 'namespace': 'test',
                 'uid': 'test'},
    'spec': {'hostPath': {'path': 'test'},
             'accessModes': 'test',
             'resources': {'requests': {'storage': '1'}}}
}

PVC_BOUND = {
    'status': {'phase': 'Bound'},
    'metadata': {'name': 'test'},
    'spec': {'volumeName': 'test',
             'claimRef': {'name': 'test'}}
}


class TestPVCHandler(test_base.TestCase):
    def setUp(self):
        super(TestPVCHandler, self).setUp()
        self.handler = h_pvc.PVCHandler()
        self.handler._is_fuxi_kubernetes = mock.MagicMock()
        self._set_up_client()

    @mock.patch('fuxi_kubernetes.config.CONF')
    def _set_up_client(self, m_cfg):
        # pass
        m_cfg.kubernetes.api_root = 'http://127.0.0.1:1234'
        m_cfg.my_ip = 'http://127.0.0.1'
        m_cfg.fuxi_port = 7879
        clients.setup_clients()
        self.fuxi_client = clients.get_fuxi_client()
        self.k8s_client = clients.get_kubernetes_client()

    def test_on_present_unrelated(self):
        self.handler._is_fuxi_kubernetes.return_value = False
        self.assertEqual(None, self.handler.on_present({}))

    def test_on_present_bound(self):
        pvc_bound = {'status': {'phase': 'Bound'}}

        self.handler._is_fuxi_kubernetes.return_value = True
        self.assertEqual(None, self.handler.on_present(pvc_bound))

    def test_on_present_create_success(self):
        self.handler._is_fuxi_kubernetes.return_value = True
        self.fuxi_client.create = mock.MagicMock()
        self.fuxi_client.create.return_value = None
        self.k8s_client.post = mock.MagicMock()
        self.k8s_client.post.return_value = None

        self.assertEqual(None, self.handler.on_present(PVC_UNBOUND))

    def test_on_present_fuxi_create_failed(self):
        self.handler._is_fuxi_kubernetes.return_value = True
        self.fuxi_client.create = mock.MagicMock()
        self.fuxi_client.create.side_effect = exc.FuxiClientException()

        self.assertRaises(exc.FuxiClientException, self.handler.on_present,
                          PVC_UNBOUND)

    def test_on_present_k8s_create_failed(self):
        self.handler._is_fuxi_kubernetes.return_value = True
        self.fuxi_client.create = mock.MagicMock()
        self.fuxi_client.create.return_value = None
        self.k8s_client.post = mock.MagicMock()
        self.k8s_client.post.side_effect = exc.K8sClientException()
        self.fuxi_client.delete = mock.MagicMock()
        self.fuxi_client.delete.return_value = None

        self.assertRaises(exc.K8sClientException, self.handler.on_present,
                          PVC_UNBOUND)

    def test_on_deleted_unrelated(self):
        self.handler._is_fuxi_kubernetes.return_value = False
        self.assertEqual(None, self.handler.on_deleted({}))

    def test_on_deleted_unbound(self):
        pvc_bound = {'status': {'phase': 'unBound'}}

        self.handler._is_fuxi_kubernetes.return_value = True
        self.assertEqual(None, self.handler.on_deleted(pvc_bound))

    def test_on_deleted_success(self):
        self.handler._is_fuxi_kubernetes.return_value = True
        self.k8s_client.get = mock.MagicMock()
        self.k8s_client.get.return_value = PVC_BOUND
        self.fuxi_client.delete = mock.MagicMock()
        self.fuxi_client.delete.return_value = None
        self.k8s_client.delete = mock.MagicMock()
        self.k8s_client.delete.return_value = None

        self.assertEqual(None, self.handler.on_deleted(PVC_BOUND))

    def test_on_deleted_get_failed(self):
        self.handler._is_fuxi_kubernetes.return_value = True
        self.k8s_client.get = mock.MagicMock()
        self.k8s_client.get.side_effect = exc.K8sClientException()

        self.assertRaises(exc.K8sClientException, self.handler.on_deleted,
                          PVC_BOUND)

    def test_on_deleted_fuxi_delete_failed(self):
        self.handler._is_fuxi_kubernetes.return_value = True
        self.k8s_client.get = mock.MagicMock()
        self.k8s_client.get.return_value = PVC_BOUND
        self.fuxi_client.delete = mock.MagicMock()
        self.fuxi_client.delete.side_effect = exc.FuxiClientException()

        self.assertRaises(exc.FuxiClientException, self.handler.on_deleted,
                          PVC_BOUND)

    def test_on_deleted_k8s_delete_failed(self):
        self.handler._is_fuxi_kubernetes.return_value = True
        self.handler._is_fuxi_kubernetes.return_value = True
        self.k8s_client.get = mock.MagicMock()
        self.k8s_client.get.return_value = PVC_BOUND
        self.fuxi_client.delete = mock.MagicMock()
        self.fuxi_client.delete.return_value = None
        self.k8s_client.delete = mock.MagicMock()
        self.k8s_client.delete.side_effect = exc.K8sClientException()

        self.assertRaises(exc.K8sClientException, self.handler.on_deleted,
                          PVC_BOUND)
