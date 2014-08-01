#!encoding=utf-8



REGISTER_URL= 'http://localhost:8008/manager/register'
HEARTBEAT_URL= 'http://localhost:8008/manager/heartbeat'

RPC_ADDRESS = 'http://localhost:9001/RPC2'

AGENT_DIRECTORY='/home/xxr/Distribute-Crawler-Agent'
SUPERVISOR_NAME_TEMPLATE = 'agent-{token}'

SUPERVISOR_AGENT_CONF_FILE = '/etc/supervisor/conf.d/agent.conf'
HEARTBEAT_INTERVAL = 5

# Please do not change below

SUPERVISOR_TEMPLATE = """
[program:{name}]
command={base_dir}/run.sh {token}
numprocs=1
user=xxr
directory={base_dir}
stopsignal=TERM
autostart=false
autorestart=true
redirect_stderr=true
"""

SUPERVISOR_TEMPLATE=SUPERVISOR_TEMPLATE.format(base_dir=AGENT_DIRECTORY, token='{token}', name=SUPERVISOR_NAME_TEMPLATE)
