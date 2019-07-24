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

"""
  Flask App definition for Cataloji
"""

from slackeventsapi import SlackEventAdapter
from flask import Flask
import re
from influxdb import InfluxDBClient


__version__ = '0.1.0'
__author__ = 'Jay Kline <jay.kline@target.com>'
__copyright__ = "Copyright (C) 2009 Target Brands, Inc."
__license__ = "Apache License, Version 2.0"


def create_app():
    """Generate the Flask app"""

    app = Flask(__name__)

    # Gather config
    app.config.from_object('cataloji.settings')

    # Register the components
    slack_event = SlackEventAdapter(app.config.get('SLACK_SIGNING_SECRET'),
                                    app.config.get('SLACK_EVENTS_ENDPOINT'),
                                    app)

    app.logger.setLevel(app.config.get("log_level", "DEBUG"))

    @app.route("/", methods=["GET"])
    @app.route("/health", methods=["GET"])
    def default():
        return "ok", 200

    @slack_event.on("reaction_added")
    @slack_event.on("reaction_removed")
    def handle_reaction(event_wrapper):
        event = event_wrapper.get("event")
        emoji = event.get("reaction")
        channel = None
        value = 1 if event.get("type") == "reaction_added" else -1

        if event.get("item").get("type") == "message":
            channel = event.get("item").get("channel")
        elif event.get("item").get("type") == "file":
            channel = event.get("item").get("file")
        elif event.get("item").get("type") == "file_comment":
            channel = event.get("item").get("file")

        if len(app.config.get('WHITELIST_EMOJI')):
            if emoji not in app.config.get('WHITELIST_EMOJI'):
                if app.config.get('RECORD_UNKNOWN_EMOJI', False):
                    log_metrics("slack", {'emoji': ':unknown:', 'location': channel}, "reaction", value)
                return

        log_metrics("slack", {'emoji': emoji, 'location': channel}, "reaction", value)

    @slack_event.on("message")
    def handle_message(event_wrapper):
        event = event_wrapper.get("event")
        message = event.get("text")
        channel = event.get("channel")

        # TODO:  Take into account message formatting.   Pre- and Code blocks should probably be ignored.
        for match in re.finditer(r":(?P<emoji>[a-z0-9'_+-]{1,100}):", message):
            if len(app.config.get('WHITELIST_EMOJI')):
                if match.group('emoji') not in app.config.get('WHITELIST_EMOJI'):
                    if app.config.get('RECORD_UNKNOWN_EMOJI', False):
                        log_metrics("slack", {'emoji': ':unknown:', 'location': channel}, "emoji", 1)
                    continue

            tags = {'emoji': match.group('emoji'), 'location': channel}
            log_metrics("slack", tags, "emoji", 1)

    # Error events
    @slack_event.on("error")
    def slack_error_handler(err):
        print("ERROR: " + str(err))

    def log_metrics(measurement, tags, field, value):
        extra_tags = app.config.get('EXTRA_TAGS')
        tags.update(extra_tags)
        json_body = [
            {
                'measurement': measurement,
                'tags': tags,
                'fields': {
                    field: value
                }
            }
        ]

        client = InfluxDBClient.from_dsn(app.config.get('INFLUXDB_URI'))

        client.write_points(json_body)

    return app
