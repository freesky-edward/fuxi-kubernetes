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

from fuxi.i18n import _LE
from oslo_log import log as logging
from oslo_serialization import jsonutils

from fuxi_kubernetes import exceptions as k_exc

LOG = logging.getLogger(__name__)


class FLEXRunner(object):
    def __init__(self, plugin):
        self._plugin = plugin

    def run(self, argv, fout):
        try:
            LOG.debug("fuxi argv=%s" % argv)
            #import pdb;pdb.set_trace()
            if argv[1] == 'init':
                LOG.debug("fuxi init")
                self._write_dict(fout, {}, 'Success')
            elif argv[1] == 'attach':
                LOG.debug("fuxi attach")
                att_out = {'device': 'fuxi-fake'}
                self._write_dict(fout, att_out, 'Success')
            elif argv[1] == 'detach':
                LOG.debug("fuxi detach")
                self._plugin.detach(argv[2:])
                self._write_dict(fout, {}, 'Success')
            elif argv[1] == 'mount':
                LOG.debug("fuxi mount")
                self._plugin.mount(argv[2:])
                self._write_dict(fout, {}, 'Success')
            elif argv[1] == 'unmount':
                LOG.debug("fuxi unmount")
                self._plugin.unmount(argv[2:])
                self._write_dict(fout, {}, 'Success')
            else:
                raise k_exc.FLEXError(_LE("unknown flex command: %s")
                                      % argv[1])
        except Exception as ex:
            # LOG.exception
            self._write_dict(fout, {})
            return 1
        return 0

    def _write_dict(self, fout, dct, status='Failure'):
        output = {'status': status}
        output.update(dct)
        LOG.debug("fuxi output: %s", output)
        jsonutils.dump(output, fout, sort_keys=True)
