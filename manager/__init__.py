#!encoding=utf-8
import sys_info
import base_class
import comm
import supervisor
import time
import config

info = None

def login():
    global info
    identity = sys_info.id_name
    info = base_class.InfoHolder(identity)
    info.system_basic = sys_info.basic_info()
    info.system_status = sys_info.run_info()

    return comm.register(info)

def heartbeat():
    global info
    info.system_status = sys_info.run_info()
    supervisor.update_status(info)

    return comm.heartbeat(info)

def token2agent(token):
    try:
        return info.agents[token]
    except:
        raise base_class.TokenNotFound

def dispatch(ret):
    for action in ret['actions']:
        if action['type'] == 'start_agent':
            new = info.add_agent(action['data'])
            supervisor.update_conf(info)
            supervisor.start_agent(new)
        elif action['type'] == 'stop_agent':
            agent = token2agent(action['data'])
            supervisor.stop_agent(agent)
            info.remove_agent(action['data'])
            supervisor.update_conf(info)
        elif action['type'] == 'restart_agent':
            agent = token2agent(action['data'])
            supervisor.restart_agent(agent)
        elif action['type'] == 'update':
            #TODO
            pass
    pass

def run():
    ret = login()
    last_update = time.time()
    dispatch(ret)

    while True:
        now = time.time()
        time_left = config.HEARTBEAT_INTERVAL - (now - last_update)
        time.sleep(time_left)
        ret = heartbeat()
        last_update = time.time()
        dispatch(ret)
