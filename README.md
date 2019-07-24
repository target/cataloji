# Cataloji for Slack

Measure Emoji usage in Slack.

## Features

* Send stats to influxdb
* Only measures where bot is, allowing private channels to remain private if desired


## Architecture

This implementation uses Flask and InfluxDB.


The Flask web service listens for the events from Slack and sends metrics to InfluxDB

## Setup

* Set up a Metrics service, something that accepts InfluxDB line protocol over a TCP port.  See the `docker-compose.yml` for an example of a Telegraph instance that does this. 
* Create the app entry in `api.slack.com/apps`.
* Create the Cataloji bot entry
* Start the Cataloji instance somewhere.  Its designed to be a Docker service, and configuration is handled via environment variables. 
* Update the app entry in `api.slack.com/apps`:
 * Create event subscriptions and point at the proper HTTP endpoint for events. Subscribe to Bot Events:
     * `app_mention`
     * `message.channels`
     * `message.groups`
  * Set OAuth permissions to include:
    * `bot`
    * `commands`
    * `channels:write`
    * `chat:write:bot`
    * `im:write`
    * `usergroups:read`
* Invite the Emojinounce bot into channels you wish to track Emoji usage

### Environment Variables

As mentioned, configuration is handled via environment variables.  Here is the list of things you can configure:
 * `VERIFICATION_TOKEN` The verification from your Slack App config. There is no default, you must set this.
 * `SLACK_EVENTS_ENDPOINT` The base URI to accept Slack events on.  Defaults to `/slack_events`
 * `SLACK_SIGNING_SECRET` The Slack signing secret from your Slack App config. There is no default, you must set this.
 * `INFLUXDB_URI` The InfluxDB location.  Defaults to `influxdb://localhost:8086/metrics`
 * `WHITELIST_EMOJI` A space separated list of emoji to specifically record.  If unset (the default) all emoji are recorded.
 * `RECORD_UNKNOWN_EMOJI` If `WHISTLIST_EMOJI` is set and `RECORD_UNKOWN_EMOJI` is True, non-whitelisted emoji will all be recorded as `:unknown:`.  If `RECORD_UNKNOWN_EMOJI` is False, non-whistelisted emoji will be ignored.
 * `EXTRA_TAGS` A JSON definition of extra tags to send with the metrics to InfluxDB.  Defaults to `{}`. 


## How to contribute

This is intended to be a community driven project. Feel free to submit a PR if you think you can improve it, or just open an issue if you have an idea but can't implement it.

We won't take every feature request, but if its a good idea, we will take it in.


## Contributors

* Jay Kline (@slushpupie)
