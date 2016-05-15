
# Copyright (c) 2016, G.A. vd. Hoorn
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

from setuptools import setup, find_packages

setup(
    author='G.A. vd. Hoorn',
    author_email='g.a.vanderhoorn@tudelft.nl',
    description='A Python (Twisted) implementation of the Simple Message protocol',
    install_requires=['construct', 'nose', 'twisted'],
    license='Apache License, Version 2.0',
    maintainer='G.A. vd. Hoorn',
    maintainer_email='g.a.vanderhoorn@tudelft.nl',
    name='simple_message',
    packages=find_packages(exclude=('tests', 'docs')),
    url='https://github.com/gavanderhoorn/simple_message_py',
    version='0.0.1',
)
