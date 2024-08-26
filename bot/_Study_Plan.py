import datetime
import discord
import json
import os

# Fil för att lagra nuvarande vecka
CURRENT_WEEK_FILE = "current_week.json"

# Studieplanens innehåll
study_plan = {
    1: {
        'title': 'Week 1: Switched Campus - Switch Administration',
        'reading': [
            'Managing MAC address table',
            'Errdisable recovery',
            'L2 MTU'
        ],
        'labs': [
            'Lab 1: Basic Switch Configuration',
            'Lab 2: VLAN Configuration'
        ],
        'tips': [
            'Förstå hur MAC address-tabellen fungerar, särskilt under dynamiska förhållanden.',
            'Experimentera med Errdisable-recovery och förstå vilka triggers som orsakar det.'
        ],
        'resources': [
            'Cisco Press: CCIE Routing and Switching v5.1 Foundations',
            'Cisco Dokumentation: Errdisable Recovery på Catalyst Switches'
        ]
    },
    2: {
        'title': 'Week 2: Layer 2 Protocols and VLAN Technologies',
        'reading': [
            'CDP, LLDP',
            'UDLD',
            'VLAN Technologies: Access ports, Trunk ports (802.1Q), Native VLAN'
        ],
        'labs': [
            'Lab 3: Trunk Configuration',
            'Lab 4: EtherChannel Configuration'
        ],
        'tips': [
            'Implementera och observera skillnaderna mellan CDP och LLDP i en labbmiljö.',
            'Testa att konfigurera UDLD och se hur det skyddar mot uni-directional länkar.'
        ],
        'resources': [
            'Cisco Live Sessions: Layer 2 Protocols Deep Dive',
            'Cisco Dokumentation: Configuring VLANs på Cisco Switchar'
        ]
    },
    3: {
        'title': 'Week 3: VLAN Management and EtherChannel',
        'reading': [
            'Manual VLAN pruning',
            'Normal range and extended range VLANs',
            'Voice VLAN',
            'LACP, static EtherChannel',
            'Layer 2 vs Layer 3 EtherChannel'
        ],
        'labs': [
            'Lab 5: Manual VLAN Pruning',
            'Lab 6: EtherChannel Troubleshooting'
        ],
        'tips': [
            'Labba på att manuellt klippa av VLAN-trafik över trunkar och observera effekten på nätverket.',
            'Träna på att sätta upp både Layer 2 och Layer 3 EtherChannel.'
        ],
        'resources': [
            'Cisco Dokumentation: EtherChannel Configuration',
            'Cisco Support: VLAN och Trunking Best Practices'
        ]
    },
    4: {
        'title': 'Week 4: Spanning Tree Protocol and Advanced VLAN Features',
        'reading': [
            'PVST+, Rapid PVST+, MST',
            'PortFast, BPDU guard, BPDU filter',
            'Loop guard, root guard',
            'Switch priority, port priority, tuning port/path cost'
        ],
        'labs': [
            'Lab 7: Spanning Tree Tuning',
            'Lab 8: Configuring BPDU Guard and Root Guard'
        ],
        'tips': [
            'Labba på olika STP-varianter och notera skillnader i konvergenstid.',
            'Testa att simulera loop-fel och hur skyddsmekanismerna fungerar.'
        ],
        'resources': [
            'Cisco Press: Understanding Spanning Tree Protocol',
            'Cisco Dokumentation: Configuring STP Features'
        ]
    },
    5: {
        'title': 'Week 5: Routing Concepts and Static Routing',
        'reading': [
            'Administrative distance',
            'Static routing (unicast, multicast)',
            'Policy-based routing',
            'VRF-Lite'
        ],
        'labs': [
            'Lab 9: Static Routing Configuration',
            'Lab 10: Policy-based Routing'
        ],
        'tips': [
            'Experimentera med statisk routning och hur administrativ distans påverkar routing-beslut.',
            'Implementera policy-baserad routning för att styra trafikvägar baserat på specifika kriterier.'
        ],
        'resources': [
            'Cisco Press: CCIE Enterprise Infrastructure Official Cert Guide',
            'Cisco Dokumentation: Policy-Based Routing Configuration Guide'
        ]
    },
    6: {
        'title': 'Week 6: EIGRP Fundamentals and Optimization',
        'reading': [
            'EIGRP Adjacencies',
            'EIGRP Metrics and Feasibility Condition',
            'EIGRP Stuck-in-active',
            'EIGRP Optimization and Scalability'
        ],
        'labs': [
            'Lab 11: EIGRP Basic Configuration',
            'Lab 12: EIGRP Optimization and Troubleshooting'
        ],
        'tips': [
            'Labba på att skapa och felsöka EIGRP adjacencies och förstå påverkan av olika metric-kriterier.',
            'Träna på att optimera EIGRP för snabbare konvergens och skalbarhet.'
        ],
        'resources': [
            'Cisco Live Sessions: EIGRP Advanced Concepts',
            'Cisco Dokumentation: EIGRP Configuration Guide'
        ]
    },
    7: {
        'title': 'Week 7: OSPF Fundamentals and Advanced Features',
        'reading': [
            'OSPFv2 and OSPFv3 Adjacencies',
            'OSPF Network Types and Area Types',
            'OSPF Path Preference',
            'LSA Throttling and SPF Tuning'
        ],
        'labs': [
            'Lab 13: OSPF Basic Configuration',
            'Lab 14: OSPF Advanced Features and Tuning'
        ],
        'tips': [
            'Träna på att förstå skillnader mellan OSPF nätverkstyper och hur area typer påverkar routing.',
            'Simulera olika LSA-typer och notera hur OSPF konvergerar med olika throttling och tuning-inställningar.'
        ],
        'resources': [
            'Cisco Press: OSPF Network Design Solutions',
            'Cisco Dokumentation: OSPF Configuration Best Practices'
        ]
    },
    8: {
        'title': 'Week 8: BGP Basics and Advanced Policy Management',
        'reading': [
            'IBGP and EBGP Peering',
            'BGP Path Selection',
            'BGP Attribute Manipulation',
            'BGP Route Reflectors'
        ],
        'labs': [
            'Lab 15: BGP Peering Configuration',
            'Lab 16: BGP Policy-Based Routing'
        ],
        'tips': [
            'Testa IBGP och EBGP peer relationer och förstå när det är lämpligt att använda route-reflectors.',
            'Experimentera med att manipulera BGP-attribut och se hur det påverkar best-path valet.'
        ],
        'resources': [
            'Cisco Press: BGP Design and Implementation',
            'Cisco Dokumentation: BGP Configuration Guide'
        ]
    },
    9: {
        'title': 'Week 9: Multicast Routing and Optimization',
        'reading': [
            'IGMPv2, IGMPv3',
            'PIM Sparse Mode',
            'Source Specific Multicast',
            'Multicast Boundaries'
        ],
        'labs': [
            'Lab 17: IGMP Configuration and Troubleshooting',
            'Lab 18: PIM Sparse Mode and SSM Configuration'
        ],
        'tips': [
            'Labba med olika IGMP-versioner och testa multicast snooping.',
            'Träna på att implementera PIM sparse mode och multicast gränser.'
        ],
        'resources': [
            'Cisco Dokumentation: Multicast Routing Configuration',
            'Cisco Live Sessions: Advanced Multicast Deployment'
        ]
    },
    10: {
        'title': 'Week 10: Cisco SD-Access Fundamentals',
        'reading': [
            'SD-Access Underlay and Overlay Concepts',
            'LISP and VXLAN Integration',
            'Cisco TrustSec Policy Plane',
            'Fabric Design and Deployment'
        ],
        'labs': [
            'Lab 19: SD-Access Fabric Deployment',
            'Lab 20: Cisco TrustSec Configuration'
        ],
        'tips': [
            'Labba med SD-Access underlay och overlay konfigurationer och observera hur LISP och VXLAN samverkar.',
            'Träna på att implementera TrustSec policyer inom ett fabric.'
        ],
        'resources': [
            'Cisco Live Sessions: SD-Access Fundamentals',
            'Cisco Dokumentation: SD-Access Deployment Guide'
        ]
    },
    11: {
        'title': 'Week 11: Cisco SD-WAN and Controller Architecture',
        'reading': [
            'SD-WAN Controller Architecture',
            'SD-WAN Underlay and Overlay Management',
            'OMP Attributes and Route Redistribution',
            'Centralized and Localized Policies'
        ],
        'labs': [
            'Lab 21: SD-WAN vManage Configuration',
            'Lab 22: OMP Route Policies and Redistribution'
        ],
        'tips': [
            'Labba med att sätta upp SD-WAN kontrollerarkitektur och implementera grundläggande OMP policyer.',
            'Testa att skapa både centrala och lokala SD-WAN policyer för olika scenarion.'
        ],
        'resources': [
            'Cisco Press: SD-WAN Fundamentals',
            'Cisco Dokumentation: SD-WAN Deployment and Best Practices'
        ]
    },
    12: {
        'title': 'Week 12: Security and QoS in Cisco IOS XE',
        'reading': [
            'Control Plane Policing and Protection',
            'Switch Security Features (VACL, PACL, DHCP Snooping)',
            'QoS: Classification, Marking, and Policing',
            'End-to-End Layer 3 QoS'
        ],
        'labs': [
            'Lab 23: Control Plane Protection Configuration',
            'Lab 24: QoS Classification and Policing'
        ],
        'tips': [
            'Implementera Control Plane Policing och observera effekterna på trafik som försöker överskrida skyddade resurser.',
            'Labba på QoS-konfigurationer och säkerställ att du förstår hur trafik klassificeras och markeras genom hela nätverket.'
        ],
        'resources': [
            'Cisco Dokumentation: QoS Configuration on Cisco Devices',
            'Cisco Live Sessions: Advanced Security Features on Cisco IOS XE'
        ]
    },
    13: {
        'title': 'Week 13: MPLS, DMVPN, and Network Services',
        'reading': [
            'MPLS Operations (LDP, Label Stacking)',
            'DMVPN Phase 3 Troubleshooting',
            'First-Hop Redundancy Protocols (HSRP, VRRP)',
            'Time Synchronization Protocols (NTP, PTP)'
        ],
        'labs': [
            'Lab 25: MPLS LDP Configuration',
            'Lab 26: DMVPN Dual Hub Setup'
        ],
        'tips': [
            'Labba på att sätta upp MPLS med LDP och observera hur etiketter staplas för olika trafikströmmar.',
            'Träna på att konfigurera DMVPN med dubbla hubbar och observera routingfailovers.'
        ],
        'resources': [
            'Cisco Dokumentation: MPLS Configuration Guide',
            'Cisco Live Sessions: DMVPN and Advanced WAN Technologies'
        ]
    },
    14: {
        'title': 'Week 14: Automation and Programmability',
        'reading': [
            'JSON, XML, YAML Data Encoding Formats',
            'EEM Applets and Guest Shell Scripting',
            'Cisco DNA Center and vManage API Integration',
            'Model-Driven Telemetry Deployment'
        ],
        'labs': [
            'Lab 27: Creating EEM Applets for Automation',
            'Lab 28: Interacting with DNA Center API via Python'
        ],
        'tips': [
            'Träna på att skapa EEM-script för automatisering av uppgifter och observera hur guest shell kan användas för scripting.',
            'Labba på att integrera med Cisco DNA Center och vManage API för att automatisera nätverkshantering.'
        ],
        'resources': [
            'Cisco Press: Network Programmability and Automation',
            'Cisco Dokumentation: Model-Driven Telemetry Deployment Guide'
        ]
    },
    15: {
        'title': 'Week 15: Restart The Studdy plan Script... Or add more stuff',
        'reading': [
        ],
        'labs': [
        ],
        'tips': [
        ],
        'resources': []
    }
}

# Funktion för att hämta nuvarande vecka från fil
def get_current_week():
    if os.path.exists(CURRENT_WEEK_FILE):
        try:
            with open(CURRENT_WEEK_FILE, "r") as f:
                data = json.load(f)
                return data.get("current_week", 1)
        except json.JSONDecodeError:
            # Hantera fallet där JSON-filen är tom eller skadad
            print("JSON file is empty or invalid. Initializing to week 1.")
            return 1
    return 1

# Funktion för att spara nuvarande vecka till fil
def save_current_week(week_number):
    with open(CURRENT_WEEK_FILE, "w") as f:
        json.dump({"current_week": week_number}, f)

# Funktion för att hämta veckans mål
def get_weekly_goal(week_number):
    return study_plan.get(week_number, None)

# Funktion för att posta veckans mål i en specifik kanal
async def post_weekly_goal(bot, study_channel_id):
    # Hämta nuvarande vecka
    current_week = get_current_week()

    goal = get_weekly_goal(current_week)

    if goal:
        channel = bot.get_channel(study_channel_id)
        
        if not channel:
            print(f"Channel with ID {study_channel_id} not found.")
            return

        embed = discord.Embed(
            title=f"Week {current_week}: {goal['title']}",
            description="This week's study plan",
            color=discord.Color.green()
        )
        embed.add_field(name="Reading", value="\n".join(goal['reading']), inline=False)
        embed.add_field(name="Labs", value="\n".join(goal['labs']), inline=False)
        
        await channel.send(embed=embed)

        # Öka veckan och spara
        current_week += 1
        save_current_week(current_week)
    else:
        print("No study plan available for this week.")