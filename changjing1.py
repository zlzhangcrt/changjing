"""Custom topology chanjing1
"""
from mininet.topo import Topo
class MyTopo( Topo ):

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        # Add hosts and switches
        Host1 = self.addHost( 'h1' )
        Host2 = self.addHost( 'h2' )
        Host3 = self.addHost( 'h3' )
        Switch1 = self.addSwitch( 's1' )
        Switch2 = self.addSwitch( 's2' )
        Switch3 = self.addSwitch( 's3' )
        # Add links
        self.addLink( Host1, Switch1 )
        self.addLink( Host2, Switch2 )
        self.addLink( Host3, Switch3 )
        self.addLink( Switch1, Switch2 )
        self.addLink( Switch1, Switch3)
        self.addLink( Switch2, Switch3 )

topos = { 'mytopo': ( lambda: MyTopo() ) }
