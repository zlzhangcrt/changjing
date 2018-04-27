#!/usr/bin/env python

import sys
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController

class MyTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Add hosts and switches
        r = self.addNode('r')
		s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
		s3 = self.addSwitch('s3')
        h0 = self.addHost('h0')
        h1 = self.addHost('h1')
		h2 = self.addHost('h2')
		h3 = self.addHost('h3')
		h4 = self.addHost('h4')
		h5 = self.addHost('h5')

        # Add links
		self.addLink( s1, r)
		self.addLink( s2, r)
		self.addLink( s3, r)
		self.addLink( h0, s1)
		self.addLink( h1, s1)
		self.addLink( h2, s2)
		self.addLink( h3, s2)
		self.addLink( h4, s3)
		self.addLink( h5, s3)
		
    def configure(self, net):
        # Get node instance
        r = net.get('r')
        h0 = net.get('h0')
		h1 = net.get('h1')
        h2 = net.get('h2')
		h3 = net.get('h3')
		h4 = net.get('h4')
		h5 = net.get('h5')

        # Sepcify IPv6 address
        r.cmd('ifconfig r-eth0 inet6 add fc00::1/8')
        r.cmd('ifconfig r-eth1 inet6 add fd00::1/8')
		r.cmd('ifconfig r-eth2 inet6 add fb00::1/8')
        h0.cmd('ifconfig h0-eth0 inet6 add fc00::2/8')
		h1.cmd('ifconfig h1-eth0 inet6 add fc00::3/8')
        h2.cmd('ifconfig h2-eth0 inet6 add fd00::2/64')
		h3.cmd('ifconfig h2-eth0 inet6 add fd00::3/64')
		h4.cmd('ifconfig h2-eth0 inet6 add fb00::2/64')
		h5.cmd('ifconfig h2-eth0 inet6 add fb00::3/64')
		
        # Sepcify route table
        h0.cmd('route -A inet6 add default gw fc00::1')
		h1.cmd('route -A inet6 add default gw fc00::1')
        h2.cmd('route -A inet6 add default gw fd00::1')
		h3.cmd('route -A inet6 add default gw fd00::1')
		h4.cmd('route -A inet6 add default gw fb00::1')
		h5.cmd('route -A inet6 add default gw fb00::1')

        # Enable router forwarding
        r.cmd('sysctl net.ipv6.conf.all.forwarding=1')

def main():
    topo = MyTopo()
    net = Mininet(topo = topo)

    if len(sys.argv) > 1:
        hp = sys.argv[1].split(':', 1)
        net.addController(RemoteController('c0', ip = hp[0], port = int(hp[1])))

    net.start()
    topo.configure(net)
    CLI(net)
    net.stop()：

if __name__ == '__main__':
    main()
