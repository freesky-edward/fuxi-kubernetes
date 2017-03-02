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

import fixtures
import mock

from fuxi_kubernetes import fuxi_client
from fuxi_kubernetes import k8s_client


class MockK8sClient(fixtures.Fixture):
    def _setUp(self):
        self.client = mock.Mock(k8s_client.K8sClient)
        self.useFixture(fixtures.MockPatch(
            'fuxi_kubernetes.clients.get_kubernetes_client',
            lambda: self.client))


class MockFuxiClient(fixtures.Fixture):
    def _setUp(self):
        self.client = mock.Mock(fuxi_client.FuxiClient)
        self.useFixture(fixtures.MockPatch(
            'fuxi_kubernetes.clients.get_fuxi_client',
            lambda: self.client))
