#!encoding=utf-8
import config
import simplejson as json
import requests

def register(info):
    data = {
        "system_basic": info.system_basic,
        "system_status": info.system_status,
        "identity": info.name,
    }
    r = requests.post(config.REGISTER_URL, data=json.dumps(data))
    r.raise_for_status()
    return r.json()

def agent_status(agent):
    return {
        'token': agent.token,
        'state': agent.state,
        'last_update': agent.last_update,
        'start_time': agent.start_time,
        'stop_time': agent.stop_time,
        'error_text': agent.error_text,
    }
def heartbeat(info):
    data = {
        "identity": info.name,
        "system_status": info.system_status,
        "agent_status": map(agent_status, info.agents.itervalues())
    }
    r = requests.post(config.HEARTBEAT_URL, data=json.dumps(data))
    r.raise_for_status()
    return r.json()
