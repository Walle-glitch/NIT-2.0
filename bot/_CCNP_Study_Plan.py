######## CCNP Enarsi and CORE #############
import datetime
import discord
import json
import os

# Fil för att lagra nuvarande vecka
_Current_Week_CCNP = "current_week_CCNP.json"

Study_plan_CCNP = {
    1: {
        'title': 'Week 1: Enterprise Network Design and Administrative Distance Troubleshooting',
        'reading': [
            'High-level enterprise network design: 2-tier, 3-tier, fabric, cloud',
            'Troubleshoot administrative distance across all routing protocols',
            'High availability techniques: Redundancy, FHRP, SSO'
        ],
        'labs': [
            'Lab 1: Configuring HSRP for High Availability',
            'Lab 2: Troubleshooting Administrative Distance with EIGRP and OSPF'
        ],
        'tips': [
            'Förstå skillnaderna mellan 2-tier och 3-tier designmodeller och deras användningsfall.',
            'Simulera hur administrativ distans påverkar routing-val och labba med att justera dessa värden.'
        ],
        'resources': [
            'Cisco Press: CCNP and CCIE Enterprise Core ENCOR 350-401 Official Cert Guide',
            'Cisco Press: CCNP Enterprise Advanced Routing ENARSI 300-410 Official Cert Guide'
        ]
    },
    2: {
        'title': 'Week 2: Wireless Network Design and Route Maps',
        'reading': [
            'Wireless deployment models: centralized, distributed, controller-less, controller-based, cloud, remote branch',
            'Troubleshoot route maps for any routing protocol (attributes, tagging, filtering)',
            'Location services in WLAN design',
            'Client density considerations'
        ],
        'labs': [
            'Lab 3: Wireless Controller Configuration',
            'Lab 4: Troubleshooting Route Maps in OSPF and BGP'
        ],
        'tips': [
            'Testa olika trådlösa distributionsmodeller och förstå deras användningsområden.',
            'Implementera och felsök route maps i olika routingprotokoll och observera hur filtrering och tagging påverkar routing.'
        ],
        'resources': [
            'Cisco Dokumentation: Wireless Network Design Guide',
            'Cisco Dokumentation: Route Maps Configuration and Troubleshooting Guide'
        ]
    },
    3: {
        'title': 'Week 3: SD-WAN and Loop Prevention Mechanisms',
        'reading': [
            'SD-WAN control and data planes elements',
            'Benefits and limitations of SD-WAN solutions',
            'Troubleshoot loop prevention mechanisms (filtering, tagging, split horizon, route poisoning)'
        ],
        'labs': [
            'Lab 5: SD-WAN Deployment and Control Plane Setup',
            'Lab 6: Troubleshooting Loop Prevention Mechanisms in EIGRP and OSPF'
        ],
        'tips': [
            'Implementera en grundläggande SD-WAN-topologi och förstå kontroll- och dataplanernas roller.',
            'Testa loop prevention-mekanismer i olika routingprotokoll och observera effekterna.'
        ],
        'resources': [
            'Cisco Dokumentation: SD-WAN Configuration Guide',
            'Cisco Live Sessions: Loop Prevention Techniques in Dynamic Routing'
        ]
    },
    4: {
        'title': 'Week 4: QoS Configurations and Redistribution Troubleshooting',
        'reading': [
            'QoS components and policies',
            'Hardware and software switching mechanisms: CEF, CAM, TCAM, FIB, RIB, and adjacency tables',
            'Troubleshoot redistribution between any routing protocols or routing sources'
        ],
        'labs': [
            'Lab 7: QoS Classification and Marking Configuration',
            'Lab 8: Troubleshooting Redistribution between EIGRP, OSPF, and BGP'
        ],
        'tips': [
            'Labba på att implementera QoS-policyer för att hantera nätverksflöden.',
            'Simulera redistribution mellan flera routingprotokoll och felsök vanliga problem.'
        ],
        'resources': [
            'Cisco Press: QoS for IP/MPLS Networks',
            'Cisco Dokumentation: Redistribution Configuration and Troubleshooting Guide'
        ]
    },
    5: {
        'title': 'Week 5: Device Virtualization and Summarization Troubleshooting',
        'reading': [
            'Hypervisor types (Type 1 and 2), virtual machines, virtual switching',
            'VRF, GRE, and IPsec tunneling',
            'Troubleshoot manual and auto-summarization with any routing protocol'
        ],
        'labs': [
            'Lab 9: Configuring and Verifying VRF Instances',
            'Lab 10: Troubleshooting Summarization in EIGRP and OSPF'
        ],
        'tips': [
            'Labba på att skapa VRF-inställningar och observera hur de påverkar routningen.',
            'Implementera manuell och automatisk summarization och felsök eventuella problem.'
        ],
        'resources': [
            'Cisco Dokumentation: GRE and IPsec Configuration Guide',
            'Cisco Live Sessions: Route Summarization Best Practices'
        ]
    },
    6: {
        'title': 'Week 6: Layer 2 Troubleshooting and Policy-Based Routing',
        'reading': [
            'Troubleshooting static and dynamic 802.1q trunking protocols',
            'Troubleshooting EtherChannels',
            'Configuring and verifying policy-based routing'
        ],
        'labs': [
            'Lab 11: Trunk Configuration and Troubleshooting',
            'Lab 12: Configuring and Verifying Policy-Based Routing'
        ],
        'tips': [
            'Labba med både statisk och dynamisk trunkning, och felsök vanliga trunk-problem.',
            'Implementera policy-baserad routning för att styra specifika trafikströmmar.'
        ],
        'resources': [
            'Cisco Press: Spanning Tree Protocols Implementation and Best Practices',
            'Cisco Dokumentation: Policy-Based Routing Configuration Guide'
        ]
    },
    7: {
        'title': 'Week 7: EIGRP Troubleshooting and VRF-Lite Configuration',
        'reading': [
            'Troubleshoot EIGRP (classic and named mode, VRF and global)',
            'Configuring and verifying VRF-Lite'
        ],
        'labs': [
            'Lab 13: EIGRP Troubleshooting in Classic and Named Mode',
            'Lab 14: Configuring and Verifying VRF-Lite'
        ],
        'tips': [
            'Labba på att konfigurera och felsöka EIGRP i både klassiskt och namngivet läge, samt i VRF-miljöer.',
            'Implementera VRF-Lite och observera hur det segmenterar nätverkstrafik.'
        ],
        'resources': [
            'Cisco Dokumentation: EIGRP Configuration Guide',
            'Cisco Press: CCNP Enterprise Advanced Routing ENARSI Official Cert Guide'
        ]
    },
    8: {
        'title': 'Week 8: OSPF Troubleshooting and Bidirectional Forwarding Detection',
        'reading': [
            'Troubleshoot OSPF (v2/v3)',
            'Describe Bidirectional Forwarding Detection (BFD)'
        ],
        'labs': [
            'Lab 15: OSPF Troubleshooting with Different Area Types',
            'Lab 16: Configuring and Verifying BFD for Fast Failure Detection'
        ],
        'tips': [
            'Träna på att felsöka OSPF i olika scenarier, inklusive komplexa area-typer som NSSA och Totally Stub.',
            'Implementera BFD för snabbare länkfel detektering och observera hur det påverkar routingprotokoll.'
        ],
        'resources': [
            'Cisco Dokumentation: OSPF Configuration and Troubleshooting Guide',
            'Cisco Dokumentation: BFD Configuration Guide'
        ]
    },
    9: {
        'title': 'Week 9: BGP Troubleshooting and MPLS Fundamentals',
        'reading': [
            'Troubleshoot BGP (Internal and External, unicast, and VRF-Lite)',
            'MPLS operations: LSR, LDP, label switching, LSP'
        ],
        'labs': [
            'Lab 17: BGP Path Selection and Route Reflector Configuration',
            'Lab 18: MPLS Label Switching and LDP Configuration'
        ],
        'tips': [
            'Labba med att felsöka BGP-sessioner, både interna och externa, och observera hur path selection sker.',
            'Simulera MPLS med LDP och observera hur etiketter hanteras för olika trafikströmmar.'
        ],
        'resources': [
            'Cisco Dokumentation: BGP Configuration and Troubleshooting Guide',
            'Cisco Dokumentation: MPLS Configuration Guide'
        ]
    },
    10: {
        'title': 'Week 10: DMVPN Configuration and Router Security Features',
        'reading': [
            'Configure and verify DMVPN (single hub)',
            'Troubleshoot router security features: IPv4 ACLs, IPv6 traffic filter, uRPF'
        ],
        'labs': [
            'Lab 19: DMVPN Single Hub Configuration',
            'Lab 20: Configuring Router Security Features and Felsökning'
        ],
        'tips': [
            'Implementera en enkel DMVPN-konfiguration och observera hur NHRP och mGRE interagerar.',
            'Labba på att konfigurera och felsöka säkerhetsfunktioner som ACL:er och uRPF.'
        ],
        'resources': [
            'Cisco Dokumentation: DMVPN Configuration Guide',
            'Cisco Dokumentation: Router Security Configuration Guide'
        ]
    },
    11: {
        'title': 'Week 11: Control Plane Policing and First Hop Security',
        'reading': [
            'Troubleshoot control plane policing (CoPP)',
            'Describe IPv6 First Hop security features: RA guard, DHCP guard, ND inspection/snooping, source guard'
        ],
        'labs': [
            'Lab 21: Configuring CoPP for Router Protection',
            'Lab 22: Configuring IPv6 First Hop Security Features'
        ],
        'tips': [
            'Testa CoPP-konfigurationer för att skydda kontrollplanet på routrar mot överbelastningsattacker.',
            'Implementera och labba med olika IPv6 säkerhetsfunktioner som RA Guard och ND Inspection.'
        ],
        'resources': [
            'Cisco Dokumentation: CoPP Configuration Guide',
            'Cisco Dokumentation: IPv6 Security Features Guide'
        ]
    },
    12: {
        'title': 'Week 12: Troubleshooting Device Management and Network Assurance',
        'reading': [
            'Troubleshoot device management: Console, VTY, Telnet, SSH, HTTPS',
            'Troubleshoot network problems using Cisco DNA Center assurance'
        ],
        'labs': [
            'Lab 23: Device Management Troubleshooting',
            'Lab 24: Cisco DNA Center Assurance Configuration and Troubleshooting'
        ],
        'tips': [
            'Labba på att felsöka enheter via olika åtkomstmetoder som SSH och Telnet.',
            'Implementera och labba med Cisco DNA Center Assurance för att övervaka och felsöka nätverk.'
        ],
        'resources': [
            'Cisco Dokumentation: Device Management and Troubleshooting Guide',
            'Cisco Dokumentation: Cisco DNA Center Assurance Best Practices'
        ]
    },
    13: {
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
    if os.path.exists(_Current_Week_CCNP):
        try:
            with open(_Current_Week_CCNP, "r") as f:
                data = json.load(f)
                return data.get("current_week", 1)
        except json.JSONDecodeError:
            # Hantera fallet där JSON-filen är tom eller skadad
            print("JSON file is empty or invalid. Initializing to week 1.")
            return 1
    return 1

# Funktion för att spara nuvarande vecka till fil
def save_current_week(week_number):
    with open(_Current_Week_CCNP, "w") as f:
        json.dump({"current_week": week_number}, f)

# Funktion för att hämta veckans mål
def get_weekly_goal(week_number):
    return Study_plan_CCNP.get(week_number, None)

# Funktion för att posta veckans mål i en specifik kanal
async def post_weekly_goal(bot, CCNP_STUDY_CHANNEL_ID):
    # Hämta nuvarande vecka
    current_week = get_current_week()

    goal = get_weekly_goal(current_week)

    if goal:
        channel = bot.get_channel(CCNP_STUDY_CHANNEL_ID)
        
        if not channel:
            print(f"Channel with ID {CCNP_STUDY_CHANNEL_ID} not found.")
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