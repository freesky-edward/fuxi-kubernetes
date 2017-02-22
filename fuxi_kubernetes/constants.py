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

K8S_API_BASE = '/api/v1'
K8S_API_NAMESPACES = K8S_API_BASE + '/namespaces'
K8S_DEFAULT_NAMESPACES = 'default'

K8S_OBJ_NAMESPACE = 'Namespace'
K8S_OBJ_POD = 'Pod'
K8S_OBJ_SERVICE = 'Service'
K8S_OBJ_ENDPOINTS = 'Endpoints'
K8S_OBJ_PV = 'PersistentVolume'
K8S_OBJ_PVC = 'PersistentVolumeClaim'

FUXI_ANNOTATION_PREFIX = 'openstack.org/createdby'
FUXI_STORAGE_PREFIX = 'volume.beta.kubernetes.io/storage-class'

FUXI_TIMEOUT_CODE = 400
DEFAULT_TIMEOUT = 120
