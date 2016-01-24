# Licensed to the Software Freedom Conservancy (SFC) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The SFC licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import errno
import os
import platform
import subprocess
from subprocess import PIPE
import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common import utils

class Service(object):

    def __init__(self, executable, port=0, log_file=PIPE, env=None, start_error_message=""):
        self.path = executable

        self.port = port
        if self.port == 0:
            self.port = utils.free_port()
        if type(self.port) == str:
            self.ip,self.port = self.port.split(':')
            self.port = int(self.port)
        else:
            self.ip = "127.0.0.1"

        self.start_error_message = start_error_message
        self.log_file = log_file
        self.env = env or os.environ

    @property
    def service_url(self):
        """
        Gets the url of the Service
        """
        return "http://localhost:%d" % self.port

    def command_line_args(self):
        raise NotImplemented("This method needs to be implemented in a sub class")

    def start(self):
        """
        Starts the Service.

        :Exceptions:
         - WebDriverException : Raised either when it can't start the service
           or when it can't connect to the service
        """
        try:
            cmd = [self.path]
            cmd.extend(self.command_line_args())
            print cmd
            self.process = subprocess.Popen(cmd, env=self.env,
                                            close_fds=platform.system() != 'Windows',
                                            stdout=self.log_file, stderr=self.log_file)
        except TypeError:
            raise
        except OSError as err:
            if err.errno == errno.ENOENT:
                raise WebDriverException(
                    "'%s' executable needs to be in PATH. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            elif err.errno == errno.EACCES:
                raise WebDriverException(
                    "'%s' executable may have wrong permissions. %s" % (
                        os.path.basename(self.path), self.start_error_message)
                )
            else:
                raise
        except Exception as e:
            raise WebDriverException(
                "The executable %s needs to be available in the path. %s\n%s" %
                (os.path.basename(self.path), self.start_error_message, str(e))
                )
        count = 0
        while not self.is_connectable():
            count += 1
            time.sleep(1)
            if count == 30:
                raise WebDriverException("Can not connect to the Service %s" % self.path)

    def is_connectable(self):
        return utils.is_connectable(self.port,ip=self.ip)

    def send_remote_shutdown_command(self):
        try:
            from urllib import request as url_request
            URLError = url_request.URLError
        except ImportError:
            import urllib2 as url_request
            import urllib2
            URLError = urllib2.URLError

        try:
            url_request.urlopen("http://127.0.0.1:%d/shutdown" % self.port)
        except URLError:
            return
        count = 0
        while self.is_connectable():
            if count == 30:
                break
            count += 1
            time.sleep(1)

    def stop(self):
        """
        Stops the service.
        """
        if self.log_file != PIPE:
            try:
                self.log_file.close()
            except Exception:
                pass

        if self.process is None:
            return

        try:
            self.send_remote_shutdown_command()
        except TypeError:
            pass

        try:
            if self.process:
                for stream in [self.process.stdin,
                               self.process.stdout,
                               self.process.stderr]:
                    try:
                        stream.close()
                    except AttributeError:
                        pass
                self.process.terminate()
                self.process.kill()
                self.process.wait()
                self.process = None
        except OSError:
            # kill may not be available under windows environment
            pass

    def __del__(self):
        # subprocess.Popen doesn't send signal on __del__;
        # we have to try to stop the launched process.
        self.stop()
