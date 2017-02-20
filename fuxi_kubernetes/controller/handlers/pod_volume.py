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

from oslo_config import cfg
from oslo_log import log as logging

from fuxi_kubernetes import clients
from fuxi_kubernetes import config
from fuxi_kubernetes import constants
from fuxi_kubernetes.handlers import k8s_base

LOG = logging.getLogger(__name__)


class PodVolumeHandler(k8s_base.ResourceEventHandler):
    """Controller side of VIF binding process for Kubernetes pods.

    `VIFHandler` runs on the Kuryr-Kubernetes controller and together with
    the CNI driver (that runs on 'kubelet' nodes) is responsible for providing
    networking to Kubernetes pods. `VIFHandler` relies on a set of drivers
    (which are responsible for managing Neutron resources) to define the VIF
    object and pass it to the CNI driver in form of the Kubernetes pod
    annotation.
    """

    OBJECT_KIND = constants.K8S_OBJ_POD

    def __init__(self):
        pass

    def on_present(self, pod):
        LOG.debug("on_present watch pod: %s", pod)
        return
        # if not self._this_node(pod):
        #     # REVISIT(ivc): consider an additional configurable check that
        #     # would allow skipping pods to enable heterogeneous environments
        #     # where certain pods/namespaces/nodes can be managed by other
        #     # networking solutions/CNI drivers.
        #     return
        #
        # for v in pod['spec']['volumes']:
        #     if 'persistentVolumeClaim' in v:
        #         pvc_status = self._get_pv_and_pvc(pod['metadata']['namespace'],
        #                                           v['persistentVolumeClaim']['claimName'])
        #         LOG.debug("on_present get pvc: %s", pvc_status)
        #         if pvc_status is not None:
        #             fuxi = clients.get_fuxi_client()
        #             data = {'Name': pvc_status['spec']['volumeName']}
        #             if fuxi.get(data)['Err'] == 'Volume Not Found':
        #                 fuxi.mount(data)

    def on_deleted(self, pod):
        LOG.debug("on_deleted watch pod: %s", pod)
        return
        # if not self._this_node(pod):
        #     return
        # for v in pod['spec']['volumes']:
        #     if 'persistentVolumeClaim' in v:
        #         pvc_status = self._get_pv_and_pvc(pod['metadata']['namespace'],
        #                                           v['persistentVolumeClaim']['claimName'])
        #         LOG.debug("on_present get pvc: %s", pvc_status)
        #         if self._is_fuxi_kubernetes(pvc_status):
        #             fuxi = clients.get_fuxi_client()
        #             data = {'Name': pvc_status['spec']['volumeName']}
        #             fuxi.unmount(data)

    def _get_pv_and_pvc(self, namespace, pvc_name):
        k8s = clients.get_kubernetes_client()
        pvc_path = constants.K8S_API_NAMESPACES + "/" + namespace + \
                   "/persistentvolumeclaims/" + pvc_name
        pvc_status = k8s.get(pvc_path)
        if self._is_fuxi_kubernetes(pvc_status):
            # pv_path = constants.K8S_API_NAMESPACES + "/persistentvolumes/" + \
            #           pvc_status['spec']['volumeName']
            # pv_status = k8s.get(pv_path)
            return pvc_status#, pv_status
        return None#, None

    def _is_fuxi_kubernetes(self, pvc):
        try:
            return (pvc['metadata']['annotations']
                    [constants.FUXI_ANNOTATION_PREFIX] == 'fuxi-kubernetes' and
                    pvc['status']['phase'] == 'Bound')
        except KeyError:
            return False

    @staticmethod
    def _is_fuxi_volume(pod):
        return pod['spec'].get('hostNetwork', False)

    @staticmethod
    def _this_node(pod):
        try:
            return (pod['spec']['nodeName'] and
                    pod['spec']['nodeName'] == config.CONF.my_ip)
        except KeyError:
            return False
