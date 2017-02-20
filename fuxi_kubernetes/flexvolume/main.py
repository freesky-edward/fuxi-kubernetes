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
import signal
import six
import sys

from oslo_log import log as logging

from fuxi_kubernetes.flexvolume import api as flex_api
from fuxi_kubernetes.flexvolume import handlers as h_flex
from fuxi_kubernetes import config

LOG = logging.getLogger(__name__)
_FLEX_TIMEOUT = 180


def load_fuxi_config_env():
    for k, v in six.iteritems(os.environ):
        if k == 'FUXI_CONFIG':
            return v
    return None


def run():
    runner = flex_api.FLEXRunner(h_flex.FuxiHandler())

    # log, need env variable support, args = ['--config-file', '/etc/fuxi/fuxi.conf']
    args = ['--config-file']
    fuxi_config = load_fuxi_config_env()
    if fuxi_config is not None:
        args.append(fuxi_config)
    else:
        args.append('/etc/fuxi/fuxi.conf')
    config.init(args)
    config.setup_logging()

    def _timeout(signum, frame):
        runner._write_dict(sys.stdout, {
            'status': 'Failure',
            'msg': 'timeout',
        })
        LOG.debug('timed out')
        sys.exit(1)

    signal.signal(signal.SIGALRM, _timeout)
    signal.alarm(_FLEX_TIMEOUT)
    status = runner.run(sys.argv, sys.stdout)
    LOG.debug("Exiting with status %s", status)
    if status:
        sys.exit(status)
