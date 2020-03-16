#
# PySNMP MIB module JANUS-MIB (http://pysnmp.sf.net)
# ASN.1 source file://./JANUS-MIB
# Produced by pysmi-0.2.2 at Fri Jun 15 10:49:05 2018
# On host finch platform Linux version 4.15.0-23-generic by user scarlettanager
# Using Python version 3.6.5 (default, Apr  1 2018, 05:46:30) 
#
Integer, OctetString, ObjectIdentifier = mibBuilder.importSymbols("ASN1", "Integer", "OctetString", "ObjectIdentifier")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
ValueRangeConstraint, ConstraintsUnion, ConstraintsIntersection, ValueSizeConstraint, SingleValueConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "ValueRangeConstraint", "ConstraintsUnion", "ConstraintsIntersection", "ValueSizeConstraint", "SingleValueConstraint")
ModuleCompliance, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "NotificationGroup")
MibScalar, MibTable, MibTableRow, MibTableColumn, Unsigned32, ModuleIdentity, ObjectIdentity, IpAddress, enterprises, MibIdentifier, iso, TimeTicks, Counter64, Gauge32, Counter32, Bits, NotificationType, Integer32 = mibBuilder.importSymbols("SNMPv2-SMI", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Unsigned32", "ModuleIdentity", "ObjectIdentity", "IpAddress", "enterprises", "MibIdentifier", "iso", "TimeTicks", "Counter64", "Gauge32", "Counter32", "Bits", "NotificationType", "Integer32")
DisplayString, TextualConvention = mibBuilder.importSymbols("SNMPv2-TC", "DisplayString", "TextualConvention")
janus = ModuleIdentity((1, 3, 6, 1, 4, 1, 9934))
janus.setRevisions(('2016-10-28 00:00',))
if mibBuilder.loadTexts: janus.setLastUpdated('201610280000Z')
if mibBuilder.loadTexts: janus.setOrganization('Janus Research Group, Inc.')
mibBuilder.exportSymbols("JANUS-MIB", PYSNMP_MODULE_ID=janus, janus=janus)
