from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class MyTopo( Topo ):
    "A LinuxRouter connecting three IP subnets"

    def build( self, **_opts ):
		
		# Add hosts and switches
        defaultIP = '192.168.1.1/24'  # IP address for r0-eth1
        router = self.addNode( 'r0', cls=LinuxRouter, ip=defaultIP )		
		s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
		s3 = self.addSwitch( 's3' )
		h1 = self.addHost( 'h1s1' , ip='192.168.1.100/24', defaultRoute='via 192.168.1.1' )
		h2 = self.addHost( 'h2s1' , ip='172.16.0.103/24', defaultRoute='via 172.16.0.1' )
        h3 = self.addHost( 'h1s2' , ip='172.16.0.100/12', defaultRoute='via 172.16.0.1')
		h4 = self.addHost( 'h2s2' , ip='172.16.0.101/12', defaultRoute='via 172.16.0.1')
        h5 = self.addHost( 'h1s3' , ip='10.0.0.100/8', defaultRoute='via 10.0.0.1' )
		h6 = self.addHost( 'h2s3' , ip='10.0.0.101/8', defaultRoute='via 10.0.0.1' )
		
		
		# Add links
		 self.addLink( s1, router, intfName2='r0-eth1', params2={ 'ip' : defaultIP } )
		 self.addLink( s2, router, intfName2='r0-eth2', params2={ 'ip' : '172.16.0.1/12' } )
		 self.addLink( s3, router, intfName2='r0-eth3', params2={ 'ip' : '10.0.0.1/8' } )
		 self.addLink( h1, s1)
		 self.addLink( h2, s1)
		 self.addLink( h3, s2)
		 self.addLink( h4, s2)
		 self.addLink( h5, s3)
		 self.addLink( h6, s3)

def run():
    "Test linux router"
    topo =MyTopo()
    net = Mininet( topo=topo )  # controller is used by s1-s3
    net.start()
    info( '*** Routing Table on Router:\n' )
    info( net[ 'r0' ].cmd( 'route' ) )
    CLI( net )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
topos = { 'mytopo': ( lambda: MyTopo() ) }
