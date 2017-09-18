# Copyright 2017.
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

try:
  from setuptools import setup
  setup()
except ImportError:
  from distutils.core import setup

setup(name="advisor_client",
      version="0.1.0",
      author="tobegit3hub",
      install_requires=["requests>=2.6.0", "pyOpenSSL>=16.1.0",
                        "argcomplete>=1.4.1"],
      description="Advisor is the hyper parameters tuning system for black box optimization",
      packages=["advisor_client"],
      entry_points={
          "console_scripts": [
          ],
      })
