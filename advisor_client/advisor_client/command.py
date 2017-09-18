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

from advisor_client.model import Study
from advisor_client.model import Trial
from advisor_client.model import TrialMetric
from advisor_client.client import AdvisorClient

logging.basicConfig(level=logging.DEBUG)
# Disable debug log from requests and urllib3
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


def print_studies(studies):
  print("{:16} {:16} {:16} {:16} {:32} {:32}".format(
      "ID", "NAME", "CONFIGURATION", "STATUS", "CREATED", "UPDATED"))

  for study in studies:
    print("{:16} {:16} {:16} {:16} {:32} {:32}".format(
        study.id, study.name, study.study_configuration, study.status,
        study.created_time, study.updated_time))


def print_trials(trials):
  print("{:16} {:16} {:16} {:16} {:16} {:16} {:32} {:32}".format(
      "ID", "STUDY", "NAME", "PARAMETER", "OBJECTIVE", "STATUS", "CREATED",
      "UPDATED"))

  for trial in trials:
    print("{:16} {:16} {:16} {:16} {:16} {:16} {:32} {:32}".format(
        trial.id, trial.study_id, trial.name, trial.parameter_values, trial.
        objective_value, trial.status, trial.created_time, trial.updated_time))


def list_studies(args):
  client = AdvisorClient()
  print_studies(client.list_studies())


def list_trials(args):
  client = AdvisorClient()
  print_trials(client.list_trials(args.study_id))


def main():
  parser = argparse.ArgumentParser()

  parser.add_argument(
      "-v",
      "--version",
      action="version",
      version=pkg_resources.require("advisor_client")[0].version,
      help="Display sdk version")

  main_subparser = parser.add_subparsers(dest="command_group", help="Commands")

  # subcommand: study
  study_parser = main_subparser.add_parser(
      "study", help="Commands about study")
  study_subparser = study_parser.add_subparsers(
      dest="study_command", help="Subcommands of study")

  # subcommand: study list
  study_list_parser = study_subparser.add_parser("list", help="List studies")
  study_list_parser.set_defaults(func=list_studies)

  # subcommand: trial
  trial_parser = main_subparser.add_parser(
      "trial", help="Commands about trial")
  trial_subparser = trial_parser.add_subparsers(
      dest="trial_command", help="Subcommands of trial")

  # subcommand: trial list
  trial_list_parser = trial_subparser.add_parser("list", help="List trials")
  trial_list_parser.add_argument(
      "-s",
      "--study_id",
      dest="study_id",
      help="The id of the resource",
      required=True)
  trial_list_parser.set_defaults(func=list_trials)

  # Display help information by default
  if len(sys.argv) == 1:
    args = parser.parse_args(["-h"])
  else:
    args = parser.parse_args(sys.argv[1:])
  args.func(args)


if __name__ == "__main__":
  main()
