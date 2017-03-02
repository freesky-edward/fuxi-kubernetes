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
from fuxi_kubernetes.tests import base as test_base


class TestK8sClient(test_base.TestCase):

    @mock.patch('fuxi_kubernetes.config.CONF')
    @mock.patch('fuxi_kubernetes.k8s_client.K8sClient')
    @mock.patch('fuxi_kubernetes.fuxi_client.FuxiClient')
    def test_setup_clients(self, m_fuxi, m_k8s, m_cfg):
        k8s_api_root = 'http://127.0.0.1:1234'
        fuxi_api_root = 'http://127.0.0.1:7879'

        k8s_dummy = object()
        fuxi_dummy = object()

        m_cfg.kubernetes.api_root = k8s_api_root
        m_cfg.my_ip = 'http://127.0.0.1'
        m_cfg.fuxi_port = 7879
        m_k8s.return_value = k8s_dummy
        m_fuxi.return_value = fuxi_dummy

        clients.setup_clients()

        m_k8s.assert_called_with(k8s_api_root)
        self.assertIs(k8s_dummy, clients.get_kubernetes_client())
        m_fuxi.assert_called_with(fuxi_api_root)
        self.assertIs(fuxi_dummy, clients.get_fuxi_client())
