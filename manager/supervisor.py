#!encoding=utf-8
import xmlrpclib
import config

server = xmlrpclib.Server(config.RPC_ADDRESS)
supervisor = server.supervisor

def update_conf(info):
    agent_list = info.agents.values()

    with open(config.SUPERVISOR_AGENT_CONF_FILE, 'w') as f:
        conf = [config.SUPERVISOR_TEMPLATE.format(token=agent.token) for agent in agent_list]
        f.write('\n'.join(conf))
    __reload_config()
    return

def update_status(info):
    data = supervisor.getAllProcessInfo()
    state_map = {}
    for item in data:
        state_map[item['name']] = item
    for agent in info.agents.itervalues():
        if agent.name not in state_map:
            agent.state = 1000 # set to unknow first
            continue
        state = state_map[agent.name]

        agent.state = state['state']
        agent.last_update = state['now']
        agent.start_time = state['start']
        agent.stop_time = state['stop']
        agent.error_text = state['spawnerr']
    return

def __reload_config():
    result = supervisor.reloadConfig()
    added, changed, removed = result[0]
    for gname in removed:
        supervisor.stopProcessGroup(gname)
        supervisor.removeProcessGroup(gname)
    for gname in changed:
        supervisor.stopProcessGroup(gname)
        supervisor.removeProcessGroup(gname)
        supervisor.addProcessGroup(gname)
    for gname in added:
        supervisor.addProcessGroup(gname)
    return

def start_agent(agent):
    try:
        supervisor.startProcess(agent.name)
    except xmlrpclib.Fault as e:
        if e.faultCode != 60:
            raise
def stop_agent(agent):
    try:
        supervisor.stopProcess(agent.name)
    except:
        pass
def print_log(agent):
    print supervisor.readProcessStdoutLog(agent.name, 100, 0)

def restart_agent(agent):
    stop_agent(agent)
    start_agent(agent)
    return
