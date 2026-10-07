import yaml
import time
import threading
import os
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class MultipathTopo(Topo):
    def build(self):
        client = self.addHost('client')
        server = self.addHost('server')

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        self.addLink(client, s1)
        self.addLink(s1, server)
        self.addLink(client, s2)
        self.addLink(s2, server)

def apply_profile(net, profile_path, switch, peer):
    with open(profile_path, 'r') as f:
        profile = yaml.safe_load(f)
    
    link = net.linksBetween(net.getNodeByName(switch), net.getNodeByName(peer))[0]
    intf = link.intf1
    
    delay = f"{profile.get('delay', 0)}ms"
    jitter = f"{profile.get('jitter', 0)}ms"
    loss = float(profile.get('loss', 0))
    bw = float(profile.get('bandwidth', 1000))
    
    intf.config(bw=bw, delay=delay, jitter=jitter, loss=loss)
    info(f"*** Applied {profile_path} to {intf.name}: bw={bw}Mbit, delay={delay}, jitter={jitter}, loss={loss}%\n")
    return profile, intf

def handover_simulator(intf, profile):
    interval = float(profile.get('handover_interval', 15))
    loss = float(profile.get('handover_loss', 10))
    duration = float(profile.get('handover_duration', 500)) / 1000.0
    base_loss = float(profile.get('loss', 1.5))
    
    while True:
        time.sleep(interval)
        info(f"\n*** Simulating LEO handover on {intf.name}: {loss}% loss\n")
        intf.config(loss=loss)
        time.sleep(duration)
        info(f"\n*** Handover complete, restoring base loss {base_loss}%\n")
        intf.config(loss=base_loss)

def run():
    topo = MultipathTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    terr_path = os.path.join(base_dir, 'link-profiles', 'terrestrial.yaml')
    leo_path = os.path.join(base_dir, 'link-profiles', 'leo-satellite.yaml')
    
    info("*** Configuring Path A (Terrestrial)\n")
    apply_profile(net, terr_path, 's1', 'server')
    
    info("*** Configuring Path B (LEO)\n")
    leo_profile, leo_intf = apply_profile(net, leo_path, 's2', 'server')
    
    t = threading.Thread(target=handover_simulator, args=(leo_intf, leo_profile))
    t.daemon = True
    t.start()
    
    info("*** Setting up routing\n")
    client = net.get('client')
    server = net.get('server')
    
    client.cmd('ip addr add 10.0.1.1/24 dev client-eth0')
    client.cmd('ip addr add 10.0.2.1/24 dev client-eth1')
    server.cmd('ip addr add 10.0.1.2/24 dev server-eth0')
    server.cmd('ip addr add 10.0.2.2/24 dev server-eth1')
    
    dumpNodeConnections(net.hosts)
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
