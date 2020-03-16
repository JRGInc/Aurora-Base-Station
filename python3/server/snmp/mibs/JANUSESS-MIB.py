#
# PySNMP MIB module JANUSESS-MIB (http://pysnmp.sf.net)
# ASN.1 source file://./JANUSESS-MIB
# Produced by pysmi-0.2.2 at Fri Jun 15 10:54:20 2018
# On host finch platform Linux version 4.15.0-23-generic by user scarlettanager
# Using Python version 3.6.5 (default, Apr  1 2018, 05:46:30) 
#
ObjectIdentifier, Integer, OctetString = mibBuilder.importSymbols("ASN1", "ObjectIdentifier", "Integer", "OctetString")
NamedValues, = mibBuilder.importSymbols("ASN1-ENUMERATION", "NamedValues")
SingleValueConstraint, ConstraintsIntersection, ValueRangeConstraint, ConstraintsUnion, ValueSizeConstraint = mibBuilder.importSymbols("ASN1-REFINEMENT", "SingleValueConstraint", "ConstraintsIntersection", "ValueRangeConstraint", "ConstraintsUnion", "ValueSizeConstraint")
janus, = mibBuilder.importSymbols("JANUS-MIB", "janus")
ModuleCompliance, ObjectGroup, NotificationGroup = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup", "NotificationGroup")
Integer32, iso, Unsigned32, TimeTicks, ObjectIdentity, Counter32, Gauge32, IpAddress, Bits, NotificationType, ModuleIdentity, MibIdentifier, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64 = mibBuilder.importSymbols("SNMPv2-SMI", "Integer32", "iso", "Unsigned32", "TimeTicks", "ObjectIdentity", "Counter32", "Gauge32", "IpAddress", "Bits", "NotificationType", "ModuleIdentity", "MibIdentifier", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "Counter64")
TextualConvention, DisplayString = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention", "DisplayString")
janusessMIB = ModuleIdentity((1, 3, 6, 1, 4, 1, 9934, 0))
janusessMIB.setRevisions(('2018-06-15 15:00', '2018-05-25 15:00', '2018-05-02 14:00', '2018-05-01 17:00', '2018-03-01 13:00', '2018-02-15 13:00', '2018-02-14 21:00', '2018-01-14 12:00', '2018-01-09 15:00', '2017-12-17 16:00', '2017-09-23 14:00', '2017-07-27 16:00', '2017-06-08 15:08', '2017-06-08 14:56', '2017-05-26 11:29', '2017-05-22 18:06', '2017-03-24 23:30', '2017-03-23 13:00', '2017-03-23 12:00', '2017-03-23 11:00', '2016-11-18 19:00', '2016-11-07 22:00', '2016-11-05 19:00', '2016-11-04 21:00', '2016-11-02 22:00', '2016-11-01 15:00', '2016-11-01 14:00', '2016-10-29 16:00', '2016-10-29 14:00', '2016-10-29 04:00',))
if mibBuilder.loadTexts: janusessMIB.setLastUpdated('201806151500Z')
if mibBuilder.loadTexts: janusessMIB.setOrganization('Janus Research Group, Inc.')
class OneDecimalFloat(TextualConvention, Integer32):
    status = 'current'
    displayHint = 'd-1'
    subtypeSpec = Integer32.subtypeSpec + ValueRangeConstraint(0, 2147483647)

janusessNotifications = MibIdentifier((1, 3, 6, 1, 4, 1, 9934, 0, 0))
janusessObjects = MibIdentifier((1, 3, 6, 1, 4, 1, 9934, 0, 1))
janusessConformance = MibIdentifier((1, 3, 6, 1, 4, 1, 9934, 0, 2))
baseProcessNotify = NotificationType((1, 3, 6, 1, 4, 1, 9934, 0, 0, 1)).setObjects(("JANUSESS-MIB", "baseProcess"), ("JANUSESS-MIB", "notifyMessage"))
if mibBuilder.loadTexts: baseProcessNotify.setStatus('current')
laneStatusNotify = NotificationType((1, 3, 6, 1, 4, 1, 9934, 0, 0, 101)).setObjects(("JANUSESS-MIB", "laneStatus"), ("JANUSESS-MIB", "laneLastModule"), ("JANUSESS-MIB", "lanePollStatus"), ("JANUSESS-MIB", "lanePollLastDTG"), ("JANUSESS-MIB", "notifyMessage"))
if mibBuilder.loadTexts: laneStatusNotify.setStatus('current')
moduleStatusNotify = NotificationType((1, 3, 6, 1, 4, 1, 9934, 0, 0, 201)).setObjects(("JANUSESS-MIB", "moduleLocation"), ("JANUSESS-MIB", "moduleType"), ("JANUSESS-MIB", "moduleVersion"), ("JANUSESS-MIB", "moduleNumberSensors"), ("JANUSESS-MIB", "moduleStatus"), ("JANUSESS-MIB", "notifyMessage"))
if mibBuilder.loadTexts: moduleStatusNotify.setStatus('current')
sensorAlertNotify = NotificationType((1, 3, 6, 1, 4, 1, 9934, 0, 0, 301)).setObjects(("JANUSESS-MIB", "sensorAlertType"), ("JANUSESS-MIB", "sensorValue"), ("JANUSESS-MIB", "sensorAlertThreshold"), ("JANUSESS-MIB", "sensorUnit"), ("JANUSESS-MIB", "sensorDescr"), ("JANUSESS-MIB", "sensorDTG"), ("JANUSESS-MIB", "notifyMessage"))
if mibBuilder.loadTexts: sensorAlertNotify.setStatus('current')
baseProcess = MibScalar((1, 3, 6, 1, 4, 1, 9934, 0, 1, 1), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseProcess.setStatus('current')
baseTable = MibTable((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2), )
if mibBuilder.loadTexts: baseTable.setStatus('current')
baseEntry = MibTableRow((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1), ).setIndexNames((0, "JANUSESS-MIB", "baseIndex"))
if mibBuilder.loadTexts: baseEntry.setStatus('current')
baseIndex = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 0)))
if mibBuilder.loadTexts: baseIndex.setStatus('current')
baseCommandListener = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseCommandListener.setStatus('current')
baseCouchDB = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 3), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseCouchDB.setStatus('current')
baseEmail = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 4), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseEmail.setStatus('current')
baseFile = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseFile.setStatus('current')
baseInfluxDB = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseInfluxDB.setStatus('current')
baseInterface = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 7), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseInterface.setStatus('current')
baseLogging = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseLogging.setStatus('current')
baseNetwork = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 9), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseNetwork.setStatus('current')
basePollData = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 10), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: basePollData.setStatus('current')
basePollDispatch = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 11), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: basePollDispatch.setStatus('current')
baseTasks = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 2, 1, 12), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: baseTasks.setStatus('current')
laneTable = MibTable((1, 3, 6, 1, 4, 1, 9934, 0, 1, 3), )
if mibBuilder.loadTexts: laneTable.setStatus('current')
laneEntry = MibTableRow((1, 3, 6, 1, 4, 1, 9934, 0, 1, 3, 1), ).setIndexNames((0, "JANUSESS-MIB", "laneAddress"))
if mibBuilder.loadTexts: laneEntry.setStatus('current')
laneAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 3, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 4)))
if mibBuilder.loadTexts: laneAddress.setStatus('current')
laneStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 3, 1, 2), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: laneStatus.setStatus('current')
laneLastModule = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 3, 1, 4), Integer32().subtype(subtypeSpec=ValueRangeConstraint(-1, 126))).setMaxAccess("readonly")
if mibBuilder.loadTexts: laneLastModule.setStatus('current')
lanePollStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 3, 1, 5), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: lanePollStatus.setStatus('current')
lanePollLastDTG = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 3, 1, 6), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: lanePollLastDTG.setStatus('current')
moduleTable = MibTable((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4), )
if mibBuilder.loadTexts: moduleTable.setStatus('current')
moduleEntry = MibTableRow((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1), ).setIndexNames((0, "JANUSESS-MIB", "moduleLaneAddress"), (0, "JANUSESS-MIB", "moduleAddress"))
if mibBuilder.loadTexts: moduleEntry.setStatus('current')
moduleLaneAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 3)))
if mibBuilder.loadTexts: moduleLaneAddress.setStatus('current')
moduleAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 126)))
if mibBuilder.loadTexts: moduleAddress.setStatus('current')
moduleType = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1, 3), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: moduleType.setStatus('current')
moduleVersion = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1, 4), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: moduleVersion.setStatus('current')
moduleLocation = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1, 5), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: moduleLocation.setStatus('current')
moduleStatus = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1, 6), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2, 3, 4, 5, 6, 7, 8))).clone(namedValues=NamedValues(("operational", 0), ("sensorEvent", 1), ("operationalEvent", 2), ("operationalError", 3), ("criticalError", 4), ("notSetup", 5), ("configError", 6), ("undetermined", 7), ("untracked", 8)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: moduleStatus.setStatus('current')
moduleNumberSensors = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 4, 1, 7), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 5))).setMaxAccess("readonly")
if mibBuilder.loadTexts: moduleNumberSensors.setStatus('current')
sensorTable = MibTable((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5), )
if mibBuilder.loadTexts: sensorTable.setStatus('current')
sensorEntry = MibTableRow((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1), ).setIndexNames((0, "JANUSESS-MIB", "sensorLaneAddress"), (0, "JANUSESS-MIB", "sensorModAddress"), (0, "JANUSESS-MIB", "sensorAddress"))
if mibBuilder.loadTexts: sensorEntry.setStatus('current')
sensorLaneAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 1), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 3)))
if mibBuilder.loadTexts: sensorLaneAddress.setStatus('current')
sensorModAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 2), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 126)))
if mibBuilder.loadTexts: sensorModAddress.setStatus('current')
sensorAddress = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 3), Integer32().subtype(subtypeSpec=ValueRangeConstraint(0, 5)))
if mibBuilder.loadTexts: sensorAddress.setStatus('current')
sensorDescr = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 4), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sensorDescr.setStatus('current')
sensorUnit = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 5), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sensorUnit.setStatus('current')
sensorValue = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 6), OneDecimalFloat()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sensorValue.setStatus('current')
sensorAlertThreshold = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 7), OneDecimalFloat()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sensorAlertThreshold.setStatus('current')
sensorAlertType = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 8), Integer32().subtype(subtypeSpec=ConstraintsUnion(SingleValueConstraint(0, 1, 2))).clone(namedValues=NamedValues(("none", 0), ("low", 1), ("high", 2)))).setMaxAccess("readonly")
if mibBuilder.loadTexts: sensorAlertType.setStatus('current')
sensorDTG = MibTableColumn((1, 3, 6, 1, 4, 1, 9934, 0, 1, 5, 1, 9), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: sensorDTG.setStatus('current')
notifyMessage = MibScalar((1, 3, 6, 1, 4, 1, 9934, 0, 1, 7), OctetString()).setMaxAccess("readonly")
if mibBuilder.loadTexts: notifyMessage.setStatus('current')
janusessCompliances = MibIdentifier((1, 3, 6, 1, 4, 1, 9934, 0, 2, 1))
janusessGroups = MibIdentifier((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2))
janusessCompliance = ModuleCompliance((1, 3, 6, 1, 4, 1, 9934, 0, 2, 1, 1)).setObjects(("JANUSESS-MIB", "baseGroup"), ("JANUSESS-MIB", "laneGroup"), ("JANUSESS-MIB", "moduleGroup"), ("JANUSESS-MIB", "sensorGroup"), ("JANUSESS-MIB", "defaultGroup"), ("JANUSESS-MIB", "baseNotificationGroup"), ("JANUSESS-MIB", "laneNotificationGroup"), ("JANUSESS-MIB", "moduleNotificationGroup"), ("JANUSESS-MIB", "sensorNotificationGroup"), ("JANUSESS-MIB", "baseGroup"), ("JANUSESS-MIB", "laneGroup"), ("JANUSESS-MIB", "moduleGroup"), ("JANUSESS-MIB", "sensorGroup"), ("JANUSESS-MIB", "defaultGroup"), ("JANUSESS-MIB", "baseNotificationGroup"), ("JANUSESS-MIB", "laneNotificationGroup"), ("JANUSESS-MIB", "moduleNotificationGroup"), ("JANUSESS-MIB", "sensorNotificationGroup"))

if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    janusessCompliance = janusessCompliance.setStatus('current')
baseGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 1)).setObjects(("JANUSESS-MIB", "baseCommandListener"), ("JANUSESS-MIB", "baseCouchDB"), ("JANUSESS-MIB", "baseEmail"), ("JANUSESS-MIB", "baseFile"), ("JANUSESS-MIB", "baseInfluxDB"), ("JANUSESS-MIB", "baseInterface"), ("JANUSESS-MIB", "baseLogging"), ("JANUSESS-MIB", "baseNetwork"), ("JANUSESS-MIB", "basePollData"), ("JANUSESS-MIB", "basePollDispatch"), ("JANUSESS-MIB", "baseTasks"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    baseGroup = baseGroup.setStatus('current')
laneGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 2)).setObjects(("JANUSESS-MIB", "laneStatus"), ("JANUSESS-MIB", "laneLastModule"), ("JANUSESS-MIB", "lanePollStatus"), ("JANUSESS-MIB", "lanePollLastDTG"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    laneGroup = laneGroup.setStatus('current')
moduleGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 3)).setObjects(("JANUSESS-MIB", "moduleType"), ("JANUSESS-MIB", "moduleVersion"), ("JANUSESS-MIB", "moduleLocation"), ("JANUSESS-MIB", "moduleStatus"), ("JANUSESS-MIB", "moduleNumberSensors"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    moduleGroup = moduleGroup.setStatus('current')
sensorGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 4)).setObjects(("JANUSESS-MIB", "sensorDescr"), ("JANUSESS-MIB", "sensorUnit"), ("JANUSESS-MIB", "sensorValue"), ("JANUSESS-MIB", "sensorAlertThreshold"), ("JANUSESS-MIB", "sensorAlertType"), ("JANUSESS-MIB", "sensorDTG"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    sensorGroup = sensorGroup.setStatus('current')
defaultGroup = ObjectGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 5)).setObjects(("JANUSESS-MIB", "baseProcess"), ("JANUSESS-MIB", "notifyMessage"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    defaultGroup = defaultGroup.setStatus('current')
baseNotificationGroup = NotificationGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 6)).setObjects(("JANUSESS-MIB", "baseProcessNotify"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    baseNotificationGroup = baseNotificationGroup.setStatus('current')
laneNotificationGroup = NotificationGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 7)).setObjects(("JANUSESS-MIB", "laneStatusNotify"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    laneNotificationGroup = laneNotificationGroup.setStatus('current')
moduleNotificationGroup = NotificationGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 8)).setObjects(("JANUSESS-MIB", "moduleStatusNotify"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    moduleNotificationGroup = moduleNotificationGroup.setStatus('current')
sensorNotificationGroup = NotificationGroup((1, 3, 6, 1, 4, 1, 9934, 0, 2, 2, 9)).setObjects(("JANUSESS-MIB", "sensorAlertNotify"))
if getattr(mibBuilder, 'version', (0, 0, 0)) > (4, 4, 0):
    sensorNotificationGroup = sensorNotificationGroup.setStatus('current')
mibBuilder.exportSymbols("JANUSESS-MIB", moduleLocation=moduleLocation, moduleAddress=moduleAddress, sensorDescr=sensorDescr, laneStatus=laneStatus, moduleEntry=moduleEntry, sensorUnit=sensorUnit, janusessGroups=janusessGroups, laneTable=laneTable, sensorAlertThreshold=sensorAlertThreshold, laneAddress=laneAddress, baseProcess=baseProcess, moduleVersion=moduleVersion, baseTasks=baseTasks, PYSNMP_MODULE_ID=janusessMIB, moduleGroup=moduleGroup, janusessObjects=janusessObjects, sensorTable=sensorTable, moduleStatus=moduleStatus, moduleTable=moduleTable, moduleNotificationGroup=moduleNotificationGroup, sensorAlertNotify=sensorAlertNotify, sensorAddress=sensorAddress, lanePollStatus=lanePollStatus, notifyMessage=notifyMessage, laneStatusNotify=laneStatusNotify, janusessMIB=janusessMIB, janusessConformance=janusessConformance, moduleStatusNotify=moduleStatusNotify, baseIndex=baseIndex, basePollDispatch=basePollDispatch, janusessCompliances=janusessCompliances, moduleType=moduleType, sensorNotificationGroup=sensorNotificationGroup, baseFile=baseFile, defaultGroup=defaultGroup, laneEntry=laneEntry, baseNotificationGroup=baseNotificationGroup, moduleLaneAddress=moduleLaneAddress, baseGroup=baseGroup, laneGroup=laneGroup, baseInfluxDB=baseInfluxDB, baseInterface=baseInterface, sensorModAddress=sensorModAddress, sensorAlertType=sensorAlertType, baseNetwork=baseNetwork, janusessNotifications=janusessNotifications, laneNotificationGroup=laneNotificationGroup, janusessCompliance=janusessCompliance, sensorEntry=sensorEntry, sensorGroup=sensorGroup, baseTable=baseTable, baseCommandListener=baseCommandListener, baseCouchDB=baseCouchDB, baseEntry=baseEntry, baseProcessNotify=baseProcessNotify, baseEmail=baseEmail, basePollData=basePollData, moduleNumberSensors=moduleNumberSensors, lanePollLastDTG=lanePollLastDTG, sensorLaneAddress=sensorLaneAddress, sensorValue=sensorValue, sensorDTG=sensorDTG, baseLogging=baseLogging, laneLastModule=laneLastModule, OneDecimalFloat=OneDecimalFloat)
