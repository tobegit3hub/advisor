#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

# Copyright 2017 The Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argcomplete
import argparse
import logging
import pkg_resources
import sys
import subprocess

logging.basicConfig(level=logging.DEBUG)
# Disable debug log from requests and urllib3
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
  raw_input = raw_input
else:
  raw_input = input


def start_server(args):

  if is_server_running() == True:
    print("Server running, do not start again")
    return

  choice = raw_input("Are you sure to run server container(Y/N): ").lower()
  if choice in ("y", "yes"):
    print("Try to start the server with container")

    command = "docker run -d -p {}:8000 tobegit3hub/advisor".format(args.port)
    if args.command_args != None:
      command += " " + args.command_args
    print("Run the command: {}".format(command))

    exit_code = subprocess.call(command, shell=True)

    if exit_code != 0:
      print("Fail to run server, exit code: {}".format(exit_code))
    else:
      print("Success to start the server, please access http://127.0.0.1:{}".
            format(args.port))

  else:
    print("Cancel operation")


def stop_server(args):

  if is_server_running() == False:
    print("Server not running, do not stop again")
    return

  choice = raw_input("Are you sure to stop server container(Y/N): ").lower()
  if choice in ("y", "yes"):
    print("Try to start the server with container")

    command = "docker ps |grep 'tobegit3hub/advisor' | awk '{print $1}' | xargs docker stop"
    print("Run the command: {}".format(command))

    exit_code = subprocess.call(command, shell=True)

    if exit_code != 0:
      print("Fail to stop server, exit code: {}".format(exit_code))
    else:
      print("Success to stop the server")

  else:
    print("Cancel operation")


def check_server_status(args):

  print("Try to get status of the server container")
  if is_server_running():
    print("Server running")
  else:
    print("Server not running")


def is_server_running():

  command = "docker ps |grep 'tobegit3hub/advisor'"
  print("Run the command: {}".format(command))

  try:
    command_output = subprocess.check_output(command, shell=True)

    if command_output != "":
      return True

  except subprocess.CalledProcessError, e:
    if e.output == "":
      pass
    else:
      print("Get error: {}".format(e.output))
    return False


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "-v",
      "--version",
      action="version",
      version=pkg_resources.require("advisor")[0].version,
      help="Display sdk version")

  main_subparser = parser.add_subparsers(dest="command_group", help="Commands")

  # subcommand: study
  server_parser = main_subparser.add_parser(
      "server", help="Commands about server")
  server_subparser = server_parser.add_subparsers(
      dest="server_command", help="Subcommands of server")

  # subcommand: server start
  server_start_parser = server_subparser.add_parser(
      "start", help="Commands about server start")
  server_start_parser.add_argument(
      "-p",
      "--port",
      dest="port",
      nargs='?',
      const=8000,
      default=8000,
      type=int,
      help="The port",
      required=False)
  server_start_parser.add_argument(
      "--command_args",
      dest="command_args",
      help="The extrs command args",
      required=False)
  server_start_parser.set_defaults(func=start_server)

  # subcommand: server stop
  server_stop_parser = server_subparser.add_parser(
      "stop", help="Commands about server stop")
  server_stop_parser.set_defaults(func=stop_server)

  # subcommand: server status
  server_status_parser = server_subparser.add_parser(
      "status", help="Commands about server status")
  server_status_parser.set_defaults(func=check_server_status)

  # Display help information by default
  if len(sys.argv) == 1:
    args = parser.parse_args(["-h"])
  else:
    args = parser.parse_args(sys.argv[1:])
  args.func(args)


if __name__ == "__main__":
  main()
