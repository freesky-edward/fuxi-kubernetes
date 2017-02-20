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

from fuxi_kubernetes import config
from fuxi_kubernetes import fuxi_client
from fuxi_kubernetes import k8s_client

_clients = {}
_FUXI_CLIENT = 'fuxi-client'
_KUBERNETES_CLIENT = 'kubernetes-client'


def get_fuxi_client():
    return _clients[_FUXI_CLIENT]


def get_kubernetes_client():
    return _clients[_KUBERNETES_CLIENT]


def setup_clients():
    setup_fuxi_client()
    setup_kubernetes_client()


def setup_fuxi_client():
    _clients[_FUXI_CLIENT] = fuxi_client.FuxiClient(
        config.CONF.my_ip + ":" + str(config.CONF.fuxi_port))


def setup_kubernetes_client():
    _clients[_KUBERNETES_CLIENT] = k8s_client.K8sClient(
        config.CONF.kubernetes.api_root)
