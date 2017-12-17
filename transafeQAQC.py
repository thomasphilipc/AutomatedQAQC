import csv

class asset:
    asset_name = None
    total_event = None
    tag_in = None
    tag_out = None
    ignition_on = None
    ignition_off = None
    idle_start = None
    idle_end = None
    journey_periodic = None
    journey_summary = None
    heartbeat = None
    power_up = None
    event_count = None
    command_response = None
    ext_power_loss = None
    ext_power_restore = None
    others = None
    driver_behaviour=0

    def __init__(self, asset_name):
        self.asset_name = asset_name

    def add_events(self, ign_on, ign_off, tag_in, tag_out, idle_start, idle_end, journey_periodic, journey_summary,
                   heartbeat, power_up, command_response, ext_power_loss, ext_power_restore, others, driver_behaviour):
        self.heartbeat = heartbeat
        self.idle_end = idle_end
        self.idle_start = idle_start
        self.ignition_off = ign_off
        self.ignition_on = ign_on
        self.journey_periodic = journey_periodic
        self.power_up = power_up
        self.tag_in = tag_in
        self.tag_out = tag_out
        self.journey_summary = journey_summary
        self.command_response = command_response
        self.ext_power_loss = ext_power_loss
        self.ext_power_restore = ext_power_restore
        self.driver_behaviour = driver_behaviour
        self.others = others

    def add_summary(self, event_count, total_events):
        self.total_event = total_events
        self.event_count = event_count


total_assets=0

with open('TransafeNov1to12.csv','r') as csvfile:
    reader = csv.reader(csvfile)

    rowcount=0
    first_entry_flag = True
    fault_flag=False
    current_asset=None
    previous_1_row = []
    previous_2_row = []
    previous_3_row = []
    previous_4_row = []
    previous_5_row = []

    for row in reader:
        #check row count
        rowcount += 1
        # skip first 9 lines which are comments
        if rowcount > 9:

            # print("###########")
            # print(row)
            # print(previous_1_row)
            # print(previous_2_row)
            # print(previous_3_row)
            # print(previous_4_row)
            # print(previous_5_row)
            # print("###########")

            # print(row)

            # row[1] and row[3] same means they have no data this usually indicates a new asset data follows
            if (row[1] == row[3]) and row[0] != "Grand Totals":
                last_odo = None
                # check if this is the first entry
                if first_entry_flag:
                    # print initialize the current asset
                    current_asset = row[0]
                    # print("entered condition indicaiting new asset")
                    total_odo_jumps=0
                    total_unexpected_order=0
                    total_assets += 1
                    num_of_events = 0
                    print("Analysing events for {}" .format(row[0]))
                    # set first entry to false
                    first_entry_flag=False
                else:
                    # print summary of the previous asset
                    if fault_flag:
                        print("QC FAIL !! {} has {} events".format(current_asset, num_of_events))
                        print("QC FAIL !! {} has {} odo jumps and {} unexpected order of events".format(current_asset, total_odo_jumps, total_unexpected_order))
                        print("----------------------------------------------------------------")
                    else:
                        print("QC PASS !! {} has {} events".format(current_asset, num_of_events))
                        print("----------------------------------------------------------------")
                    current_asset = row[0]
                    fault_flag=False
                    total_odo_jumps = 0
                    total_unexpected_order = 0
                    # print("entered condition indicaiting new asset")
                    total_assets += 1
                    num_of_events = 0
                    print("Analysing events for {}".format(row[0]))
                #now we check if the following line has the same asset name and has some content in the 3rd column
            elif row[0]==current_asset and row[2] != "":


                # check for odometer drops or high jumps
                if (row[1] in ["CAN Periodic","Position Report","Journey Summary"]):

                    if last_odo == None:
                        last_odo = int(row[6])
                    else:
                        odo_change = int(last_odo)-int(row[6])
                        last_odo = int(row[6])

                        if odo_change < 0 or odo_change>300:
                            #print("checking odo")
                            fault_flag=True
                            print(" ERROR !! fault found odometer jump {} at row {}".format(odo_change,rowcount))
                            total_odo_jumps+=1


                # now we check if the sequence of events are in the expected order for ignition off
                if row[1] == "Ignition Off":
                    if previous_1_row[1] in ["Journey Summary","Idle End","Tag Out"] and previous_2_row[1] in ["External Power Loss","Tag Out","Tag In","Journey Summary","Idle End","Heartbeat","Stop Moving"]:
                        # print("Looks Good, sequence of events {} , {} , {}  , {} are fine  at row {}".format(row[1],
                        #                                                                            previous_1_row[1],
                        #                                                                            previous_2_row[1],
                        #                                                                            previous_3_row[1],
                        #                                                                            rowcount))
                        pass
                    else:
                        fault_flag = True
                        print(" ERROR !! {} , {} , {}  ,{} fault found in sequence of events at row {}".format(row[1],previous_1_row[1],previous_2_row[1],previous_3_row[1],rowcount))
                        total_unexpected_order+=1
                # now we check if the sequence of events are in the expected order for ignition on
                if row[1] == "Tag In":
                    if previous_1_row[1] in ["Journey Summary","Tag In","Ignition On","External Power Restore"] and previous_2_row[1] in ["External Power Loss","Power Up","CAN Periodic", "Heartbeat","Tag Out","Position Report","Start Moving","Ignition Off"]:
                            # print("Looks Good, sequence of events {} , {} , {}  , are fine  at row {}".format(row[1],
                            #                                                                                     previous_1_row[
                            #                                                                                         1],
                            #                                                                                     previous_2_row[
                            #                                                                                         1],
                            #                                                                                     previous_3_row[1],
                            #                                                                                     rowcount))
                        pass
                    else:
                        fault_flag = True
                        print(" ERROR !! {} , {} , {}  , fault found in sequence of events at row {}".format(row[1], previous_1_row[1], previous_2_row[1],rowcount))
                        total_unexpected_order+=1


                #print(row)
                num_of_events +=1




        if rowcount == 7:
            previous_2_row = previous_1_row
            previous_1_row=row
        if rowcount == 8:
            previous_3_row = previous_2_row
            previous_2_row = previous_1_row
            previous_1_row = row
        if rowcount == 9:
            previous_4_row = previous_3_row
            previous_3_row = previous_2_row
            previous_2_row = previous_1_row
            previous_1_row = row
        if rowcount > 9:
            previous_5_row = previous_4_row
            previous_4_row = previous_3_row
            previous_3_row = previous_2_row
            previous_2_row = previous_1_row
            previous_1_row = row






