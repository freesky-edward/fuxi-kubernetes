# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import copy

from oslo_log import _options

from fuxi_kubernetes import config

_fuxi_k8s_opts = [
    ('kubernetes', config.k8s_opts),
]


def list_fuxi_opts():
    """Return a list of oslo_config options available in Fuxi service.

    Each element of the list is a tuple. The first element is the name of the
    group under which the list of elements in the second element will be
    registered. A group name of None corresponds to the [DEFAULT] group in
    config files.

    This function is also discoverable via the 'fuxi' entry point under
    the 'oslo_config.opts' namespace.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users by Fuxi.

    :returns: a list of (group_name, opts) tuples
    """

    return ([(k, copy.deepcopy(o)) for k, o in _fuxi_k8s_opts] +
            _options.list_opts())
