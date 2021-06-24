import bluetooth

nearby_devices = bluetooth.discover_devices(lookup_names=True)

for addr, name in nearby_devices:
    print("%s - %s" % (addr, name))

    # services = bluetooth.find_service(address=addr)

    # for svc in services:
    #     print("Service Name: %s" % svc["name"])
    #     print("\tHost: %s" % svc["host"])
    #     print("\tDescription: %s" % svc["description"])
    #     print("\tProvided By: %s" % svc["provider"])
    #     print("\tProtocol: %s" % svc["protocol"])
    #     print("\tChannel/PSM: %s" % svc["port"])
    #     print("\tService Classes: %s " % svc["service-classes"])
    #     print("\tProfiles: %s " % svc["profiles"])
    #     print("\tService Id: %s " % svc["service-id"])

    print('-------------------------------------------')