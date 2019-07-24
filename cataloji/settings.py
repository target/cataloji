# Copyright (c) 2019 Target Brands, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from urllib.parse import urlparse
import json

SLACK_SIGNING_SECRET = os.environ.get('SLACK_SIGNING_SECRET', '')
VERIFICATION_TOKEN = os.environ.get('VERIFICATION_TOKEN', '')
SLACK_EVENTS_ENDPOINT = os.environ.get("SLACK_EVENTS_ENDPOINT", "/slack_events")
INFLUXDB_URI = os.environ.get('INFLUXDB_URI', 'http://localhost:8086')
WHITELIST_EMOJI = os.environ.get('WHITELIST_EMOJI', '').split()
RECORD_UNKNOWN_EMOJI = os.environ.get('RECORD_UNKNOWN_EMOJI', "False") in ['True', 'true', 'TRUE', 't', 'T']
EXTRA_TAGS = json.loads(os.environ.get('EXTRA_TAGS', '{}'))