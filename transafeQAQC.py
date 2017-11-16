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

with open('TransafeAssetHistory.csv','r') as csvfile:
    reader = csv.reader(csvfile)

    rowcount=0
    first_entry_flag = True
    current_asset=None
    previous_1_row = []
    previous_2_row = []
    previous_3_row = []
    previous_4_row = []
    previous_5_row = []

    for row in reader:
        rowcount += 1
        # skip first 7 lines
        if rowcount > 9:
            # print ("starts the data processing")
            # print(row)
            # row[1] and row[3] same means they have no data this usually indicates a new asset data follows
            if (row[1] == row[3]):
                if first_entry_flag:
                    current_asset = row[0]
                    # print("entered condition indicaiting new asset")
                    total_assets += 1
                    num_of_events = 0
                    print(row)

                    first_entry_flag=False
                else:
                    print(" {} has {} events".format(current_asset, num_of_events))
                    current_asset = row[0]
                    # print("entered condition indicaiting new asset")
                    total_assets += 1
                    num_of_events = 0
                    print(row)
                #now we check if this is the first entry
            elif row[0]==current_asset and row[2] != "":
                if row[1]== previous_1_row[1]:
                    print("Eureka")
                if ((row [1] == previous_1_row [1]) and (previous_2_row[1] == previous_3_row[1])):
                    print ("Shite mate all of them are the same")
                #print(row)
                num_of_events +=1
            else :
                pass

            previous_5_row = previous_4_row
            previous_4_row = previous_3_row
            previous_3_row = previous_2_row
            previous_2_row = previous_1_row
            previous_1_row = row

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



        print("###########")
        print(row)
        print(previous_1_row)
        print(previous_2_row)
        print(previous_3_row)
        print(previous_4_row)
        print(previous_5_row)
        print ("###########")
        previous_1_row = row

