from pysnmp.entity.rfc3413.oneliner import cmdgen


myoid = "1.3.6.1.4.1.2620.1.6.7.8.1.1.3.2.0"
myagent = '10.0.0.208'
mycommunity = 'vpn123'


cmdGen = cmdgen.CommandGenerator()

errorIndication, errorStatus, errorIndex, varBinds = cmdGen.getCmd(
    cmdgen.CommunityData(mycommunity),
    cmdgen.UdpTransportTarget((myagent, 161)),
    myoid
)

# Check for errors and print out results
if errorIndication:
    print(errorIndication)
else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )
    else:
        for name, val in varBinds:
            print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))