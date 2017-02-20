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

import sys

from fuxi.i18n import _LI
from oslo_log import log as logging
from oslo_service import service

from fuxi_kubernetes import clients
from fuxi_kubernetes import config
from fuxi_kubernetes import constants
from fuxi_kubernetes.controller.handlers import pipeline as h_pipeline
from fuxi_kubernetes.controller.handlers import pod_volume as h_pvl
from fuxi_kubernetes.controller.handlers import pvc as h_pvc
from fuxi_kubernetes import watcher

LOG = logging.getLogger(__name__)


class FuxiK8sService(service.Service):
    """Fuxi-Kubernetes controller Service."""

    def __init__(self):
        super(FuxiK8sService, self).__init__()

        pipeline = h_pipeline.ControllerPipeline(self.tg)
        self.watcher = watcher.Watcher(pipeline, self.tg)
        # TODO(ivc): pluggable resource/handler registration
        # for resource in ["pods", "persistentvolumeclaims"]:
        for resource in ["persistentvolumeclaims"]:
            self.watcher.add("%s/%s" % (constants.K8S_API_BASE, resource))
        pipeline.register(h_pvc.PVCHandler())
        #pipeline.register(h_pvl.PodVolumeHandler())

    def start(self):
        LOG.info(_LI("Service '%s' starting"), self.__class__.__name__)
        super(FuxiK8sService, self).start()
        self.watcher.start()
        LOG.info(_LI("Service '%s' started"), self.__class__.__name__)

    def wait(self):
        super(FuxiK8sService, self).wait()
        LOG.info(_LI("Service '%s' stopped"), self.__class__.__name__)

    def stop(self, graceful=False):
        LOG.info(_LI("Service '%s' stopping"), self.__class__.__name__)
        self.watcher.stop()
        super(FuxiK8sService, self).stop(graceful)


def start():
    config.init(sys.argv[1:])
    config.setup_logging()
    clients.setup_clients()
    fuxik8s_launcher = service.launch(config.CONF, FuxiK8sService())
    fuxik8s_launcher.wait()
