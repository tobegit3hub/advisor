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


def start_server(args):

  print("Are you sure to run server container(Y/N):")
  choice = raw_input().lower()
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

  print("Are you sure to stop server container(Y/N):")
  choice = raw_input().lower()
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


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "-v",
      "--version",
      action="version",
      version=pkg_resources.require("advisor-clients")[0].version,
      help="Display sdk version")

  main_subparser = parser.add_subparsers(dest="command_group", help="Commands")

  # subcommand: starta_server
  start_server_parser = main_subparser.add_parser(
      "start_server", help="Commands about start_server")
  start_server_parser.add_argument(
      "-p",
      "--port",
      dest="port",
      nargs='?',
      const=8000,
      default=8000,
      type=int,
      help="The port",
      required=False)
  start_server_parser.add_argument(
      "--command_args",
      dest="command_args",
      help="The extrs command args",
      required=False)

  # subcommand: stop_server
  stop_server_parser = main_subparser.add_parser(
      "stop_server", help="Commands about stop_server")
  stop_server_parser.set_defaults(func=stop_server)

  start_server_parser.set_defaults(func=start_server)

  # Display help information by default
  if len(sys.argv) == 1:
    args = parser.parse_args(["-h"])
  else:
    args = parser.parse_args(sys.argv[1:])
  args.func(args)


if __name__ == "__main__":
  main()
