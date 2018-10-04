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
import pprint
import json
from prettytable import PrettyTable

from advisor_client.client import AdvisorClient
from advisor_client.runner.runner_launcher import RunnerLauncher

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


def print_studies_as_table(studies):
  table = PrettyTable()
  table.field_names = [
      "Id", "Name", "Configuration", "Status", "Create", "Updated"
  ]

  for study in studies:
    table.add_row([
        study.id, study.name, study.study_configuration, study.status,
        study.created_time, study.updated_time
    ])

  print(table)


def print_trials(trials):
  print("{:16} {:16} {:16} {:16} {:16} {:16} {:32} {:32}".format(
      "ID", "STUDY", "NAME", "PARAMETER", "OBJECTIVE", "STATUS", "CREATED",
      "UPDATED"))

  for trial in trials:
    print("{:16} {:16} {:16} {:16} {:16} {:16} {:32} {:32}".format(
        trial.id, trial.study_name, trial.name, trial.parameter_values,
        trial.objective_value, trial.status, trial.created_time,
        trial.updated_time))


def print_trials_as_table(trials):
  table = PrettyTable()
  table.field_names = [
      "Id", "Study", "Name", "PARAMETER", "Objective", "Status", "Create",
      "Updated"
  ]

  for trial in trials:
    table.add_row([
        trial.id, trial.study_name, trial.name, trial.parameter_values,
        trial.objective_value, trial.status, trial.created_time,
        trial.updated_time
    ])
  print(table)


def list_studies(args):
  client = AdvisorClient()
  print_studies_as_table(client.list_studies())


def describe_studie(args):
  client = AdvisorClient()
  study = client.get_study_by_name(args.study_name)

  # Print study
  table = PrettyTable()
  table.field_names = [
      "Id", "Name", "Algorithm", "Status", "Create", "Updated"
  ]
  table.add_row([
      study.id, study.name, study.algorithm, study.status, study.created_time,
      study.updated_time
  ])
  print(table)

  # Print study configuration
  """
  table = PrettyTable()
  table.field_names = ["Configuration"]
  table.add_row([study.study_configuration])
  print(table)
  """
  pprint.pprint(json.loads(study.study_configuration))

  # Print related trials
  study_trials = client.list_trials(args.study_name)
  if (len(study_trials)) > 0:
    print_trials_as_table(study_trials)


def list_trials(args):
  client = AdvisorClient()
  print_trials_as_table(client.list_trials(args.study_name))


def run_with_file(args):
  launcher = RunnerLauncher(args.run_file)
  launcher.run()


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
  study_parser = main_subparser.add_parser(
      "study", help="Commands about study")
  study_subparser = study_parser.add_subparsers(
      dest="study_command", help="Subcommands of study")

  # subcommand: study list
  study_list_parser = study_subparser.add_parser("list", help="List studies")
  study_list_parser.set_defaults(func=list_studies)

  # subcommand: study describe
  study_describe_parser = study_subparser.add_parser(
      "describe", help="Describe studiy")
  study_describe_parser.add_argument(
      "-s",
      "--study_name",
      dest="study_name",
      help="The id of the resource",
      required=True)
  study_describe_parser.set_defaults(func=describe_studie)

  # subcommand: trial
  trial_parser = main_subparser.add_parser(
      "trial", help="Commands about trial")
  trial_subparser = trial_parser.add_subparsers(
      dest="trial_command", help="Subcommands of trial")

  # subcommand: trial list
  trial_list_parser = trial_subparser.add_parser("list", help="List trials")
  trial_list_parser.add_argument(
      "-s",
      "--study_name",
      dest="study_name",
      help="The id of the resource",
      required=True)
  trial_list_parser.set_defaults(func=list_trials)

  # subcommand: run
  run_parser = main_subparser.add_parser("run", help="Commands about run")
  run_parser.add_argument(
      "-f", "--file", dest="run_file", help="The run file", required=True)
  run_parser.set_defaults(func=run_with_file)

  # Display help information by default
  if len(sys.argv) == 1:
    args = parser.parse_args(["-h"])
  else:
    args = parser.parse_args(sys.argv[1:])
  args.func(args)


if __name__ == "__main__":
  main()
