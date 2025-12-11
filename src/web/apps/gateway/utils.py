import os
import json
from datetime import datetime

import redis
from django.conf import settings


def is_whitelisted(norm_path, whitelisted_paths=None):
    is_whitelist = False

    if norm_path.endswith('.ico'):
        return True

    if whitelisted_paths is None:
        whitelisted_paths = []

    for path in whitelisted_paths:
        path = '/' + path if not path.startswith('/') else path
        path = path[:-1] if path.endswith('/') else path 
        if os.path.normpath(norm_path).startswith(path):
            is_whitelist = True
            break

    return is_whitelist


def get_time_length(request_timestamp, response_timestamp, datetime_format):
    diff = datetime.strptime(response_timestamp, datetime_format) - datetime.strptime(request_timestamp,
                                                                                      datetime_format)
    return diff.total_seconds()

from channels.layers import get_channel_layer

async def get_redis():
    channel_layer = get_channel_layer()
    return channel_layer.redis_connection


# Websocket monitoring helpers

def _get_redis_client():
    hosts = settings.CHANNEL_LAYERS.get("default", {}).get("CONFIG", {}).get("hosts", [])
    host_entry = hosts[0] if hosts else ("localhost", 6379)
    if isinstance(host_entry, (list, tuple)):
        host, port = host_entry[0], host_entry[1] if len(host_entry) > 1 else 6379
    else:
        host, port = host_entry, 6379
    return redis.Redis(host=host, port=port, decode_responses=True)


def get_active_ws_connections():
    """Return list of active websocket connection payloads stored by consumers."""
    client = _get_redis_client()
    cursor = 0
    connections = []

    while True:
        cursor, keys = client.scan(cursor=cursor, match="ws:connected:*", count=200)
        if keys:
            values = client.mget(keys)
            for raw in values:
                if not raw:
                    continue
                try:
                    connections.append(json.loads(raw))
                except json.JSONDecodeError:
                    continue
        if cursor == 0:
            break

    return connections


def group_connections_by_path(connections):
    grouped = {}
    for conn in connections:
        path = conn.get("path") or "Unknown"
        grouped.setdefault(path, []).append(conn)
    return grouped


def clear_ws_connections():
    """Delete all tracked websocket connection keys."""
    client = _get_redis_client()
    cursor = 0
    keys_to_delete = []
    while True:
        cursor, keys = client.scan(cursor=cursor, match="ws:connected:*", count=200)
        keys_to_delete.extend(keys)
        if cursor == 0:
            break
    deleted = 0
    if keys_to_delete:
        deleted = client.delete(*keys_to_delete)
    return deleted


# View utils

def is_admin(user):
    return user.is_superuser


def filter_paths(paths, filter_by, value):
    if filter_by == "method":
        if value:
            return [path for path in paths if path.get('method') == value]
        else:
            return paths
    else:
        if value:
            return [path for path in paths if any([value.lower() in [str(val).lower() for val in path.values()]])]
        else:
            return paths
