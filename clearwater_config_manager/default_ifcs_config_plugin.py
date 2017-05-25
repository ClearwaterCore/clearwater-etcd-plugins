# Project Clearwater - IMS in the Cloud
# Copyright (C) 2017  Metaswitch Networks Ltd
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version, along with the "Special Exception" for use of
# the program along with SSL, set forth below. This program is distributed
# in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details. You should have received a copy of the GNU General Public
# License along with this program.  If not, see
# <http://www.gnu.org/licenses/>.
#
# The author can be reached by email at clearwater@metaswitch.com or by
# post at Metaswitch Networks Ltd, 100 Church St, Enfield EN2 6BQ, UK
#
# Special Exception
# Metaswitch Networks Ltd  grants you permission to copy, modify,
# propagate, and distribute a work formed by combining OpenSSL with The
# Software, or a work derivative of such a combination, even if such
# copying, modification, propagation, or distribution would otherwise
# violate the terms of the GPL. You must comply with the GPL in all
# respects for all of the code used other than OpenSSL.
# "OpenSSL" means OpenSSL toolkit software distributed by the OpenSSL
# Project and licensed under the OpenSSL Licenses, or a work based on such
# software and licensed under the OpenSSL Licenses.
# "OpenSSL Licenses" means the OpenSSL License and Original SSLeay License
# under which the OpenSSL Project distributes the OpenSSL toolkit software,
# as those licenses appear in the file LICENSE-OPENSSL.

from metaswitch.clearwater.config_manager.plugin_base import ConfigPluginBase, FileStatus
from metaswitch.clearwater.etcd_shared.plugin_utils import run_command, safely_write
import logging

_log = logging.getLogger("default_ifcs_config_plugin")
_file = "/etc/clearwater/default_ifcs.xml"

_default_value = """\
<?xml version="1.0" encoding="UTF-8"?>
<DefaultIFCsSet>
</DefaultIFCsSet>"""

class DefaultIFCsConfigPlugin(ConfigPluginBase):
    def __init__(self, _params):
        pass

    def key(self):  # pragma: no cover
        return "default_ifcs"

    def file(self):
        return _file

    def default_value(self):
        return _default_value

    def status(self, value):
        try:
            with open(_file, "r") as ifile:
                current = ifile.read()
                if current == value:
                    return FileStatus.UP_TO_DATE
                else:
                    return FileStatus.OUT_OF_SYNC
        except IOError:  # pragma: no cover
            return FileStatus.MISSING

    def on_config_changed(self, value, alarm):
        _log.info("Updating Default IFCs configuration file")

        if self.status(value) != FileStatus.UP_TO_DATE:
            safely_write(_file, value)
            run_command("/usr/share/clearwater/bin/reload_default_ifcs_config")

def load_as_plugin(params):  # pragma: no cover
    return DefaultIFCsConfigPlugin(params)