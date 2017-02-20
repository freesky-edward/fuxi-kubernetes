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

import os

from oslo_concurrency import processutils
from oslo_log import log as logging
from oslo_serialization import jsonutils

from fuxi_kubernetes import clients
from fuxi_kubernetes import constants as k_const

LOG = logging.getLogger(__name__)


class FuxiHandler(object):
    def _get_pvc(self, namespace, pvc_name):
        k8s_cli = clients.get_kubernetes_client()
        pvc_path = k_const.K8S_API_NAMESPACES + "/" + namespace + \
                   "/persistentvolumeclaims/" + pvc_name
        pvc_status = k8s_cli.get(pvc_path)
        if self._is_fuxi_kubernetes(pvc_status):
            return pvc_status
        return None

    def _is_fuxi_kubernetes(self, pvc):
        try:
            return (pvc['metadata']['annotations']
                    [k_const.FUXI_ANNOTATION_PREFIX] == 'fuxi-kubernetes' and
                    pvc['status']['phase'] == 'Bound')
        except KeyError:
            return False

    def _create_dev_path(self, mountpoint, pod):
        if os.path.lexists(pod):
            cmd_unlink = ['unlink', pod]
            processutils.execute(*cmd_unlink, run_as_root=True)
        else:
            cmd_mkdir = ['mkdir', '-p', os.path.dirname(pod)]
            processutils.execute(*cmd_mkdir, run_as_root=True)
        cmd_link = ['ln', '-s', mountpoint, pod]
        processutils.execute(*cmd_link, run_as_root=True)

    def _remove_dev_path(self, mountpoint):
        if os.path.lexists(mountpoint):
            cmd_unlink = ['unlink', mountpoint]
            processutils.execute(*cmd_unlink, run_as_root=True)
            cmd_mkdir = ['mkdir', mountpoint]
            processutils.execute(*cmd_mkdir, run_as_root=True)

    def _umount_vol(self, path):
        cmd_unmount = ['umount', path]
        processutils.execute(*cmd_unmount, run_as_root=True)

    def mount(self, params):
        name = jsonutils.loads(params[2]).get('claimName', None)
        if name is not None:
            clients.setup_clients()
            pvc = self._get_pvc(k_const.K8S_DEFAULT_NAMESPACES, name)
            if pvc is not None:
                fuxi_cli = clients.get_fuxi_client()
                data = {'Name': pvc['spec']['volumeName']}
                mount_info = fuxi_cli.get(data)
                if mount_info['Err'] == 'Volume Not Found' \
                        or mount_info['Volume']['Mountpoint'] == '':
                    mount_info['Volume']['Mountpoint'] = \
                        fuxi_cli.mount(data)['Mountpoint']
                LOG.debug("mount info is: %s", mount_info)
                # self._create_dev_path(config.CONF.kubernetes.volume_mount +
                #                       pvc['metadata']['uid'],
                #                       params[0])
                self._create_dev_path(mount_info['Volume']['Mountpoint'],
                                      params[0])

    def unmount(self, params):
        self._remove_dev_path(params[0])

    def detach(self, params):
        self._umount_vol(params[0])
        clients.setup_clients()
        fuxi = clients.get_fuxi_client()
        data = {'Name': params[0]}
        fuxi.unmount(data)
