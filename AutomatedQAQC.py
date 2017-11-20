import os
import csv

requiredDir = 'C:\\QA'


for filename in os.listdir(requiredDir):
    print(filename)


file = open(requiredDir + "\\" + filename, 'r', errors='replace')
newfile_flag = 1
filename = filename.split('.csv')

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


    def __init__(self,asset_name):
        self.asset_name=asset_name

    def add_events(self,ign_on,ign_off,tag_in,tag_out,idle_start,idle_end,journey_periodic,journey_summary,heartbeat,power_up,command_response,ext_power_loss,ext_power_restore,others,driver_behaviour):
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
        self.driver_behaviour= driver_behaviour
        self.others = others

    def add_summary(self,event_count,total_events):
        self.total_event=total_events
        self.event_count=event_count


    def createsheet(self):

        # if int(self.tag_in)> 0:
        #     self.tag_in= 1
        #
        # if int(self.ignition_on)> 0:
        #     self.ignition_on= 1
        #
        # if int(self.journey_periodic)> 0:
        #     self.journey_periodic= 1
        #
        # if int(self.driver_behaviour)> 0:
        #     self.driver_behaviour= 1
        #
        # if int(self.idle_start)> 0:
        #     self.idle_start= 1
        #
        # if int(self.idle_end)> 0:
        #     self.idle_end= 1
        #
        # if int(self.ignition_off)> 0:
        #     self.ignition_off= 1
        #
        # if int(self.journey_summary)> 0:
        #     self.journey_summary= 1
        #
        # if int(self.journey_periodic) > 0:
        #     self.journey_periodic=  1
        #
        # if int(self.tag_out) > 0:
        #     self.tag_out=  1

        print ("{},{},{},{},{},{},{},{},{},{},{}".format(self.asset_name,self.tag_in,self.ignition_on,self.journey_periodic,self.power_up,self.driver_behaviour,self.idle_start,self.idle_end,self.ignition_off,self.journey_summary,self.tag_out))

    def processQA(self):

        score=15
        print("###########################################", file=open("output.txt", "a"))
        print("Analysis for {}".format(self.asset_name), file=open("output.txt", "a"))


        print ("-----------Ignition On/Off Analysis--------------", file=open("output.txt", "a"))
        if (int(self.ignition_on) > 0):
            engine_event_accuracy = (int(self.ignition_off)/int(self.ignition_on))*100
            difference_ignition_events = abs(int(self.ignition_on)-int(self.ignition_off))
            if (difference_ignition_events>2 and engine_event_accuracy < 95):
                print("Engine event accuracy is {} i.e. ignition off @{}/ ignition on @{} ".format(engine_event_accuracy,self.ignition_off,self.ignition_on), file=open("output.txt", "a"))
                print("There is multipleinstances with ignition on and ignition off pair mismatches", file=open("output.txt", "a"))
                score = score - 1.5
            else:
                print("Engine event accuracy is {} i.e. ignition off @{}/ ignition on @{} ".format(engine_event_accuracy,self.ignition_off,self.ignition_on), file=open("output.txt", "a"))
        else:
            print ("No ignition On/Off events", file=open("output.txt", "a"))
            score = score - 2



        print("-----------Ignition On/Off Analysis--------------", file=open("output.txt", "a"))

        if (int(self.tag_in) > 0):
            tag_event_accuracy = (int(self.tag_out)/int(self.tag_in))*100
            print("Tag event accuracy is {} i.e. tagout @{}/ tag in @{} ".format(tag_event_accuracy,self.tag_out,self.tag_in), file=open("output.txt", "a"))
            if tag_event_accuracy <95:
                score = score - 1.5
        else:
            print("No Tag In/Out events", file=open("output.txt", "a"))
            score = score - 2

        print("-----------Tag & Ignition Analysis--------------", file=open("output.txt", "a"))

        if (int(self.ignition_on) > 0 and int(self.tag_in)>0):
            percentage_engine_on_w_tagins= (int(self.tag_in)/int(self.ignition_on))*100
            print("The percentage of engine on with tag in is {} i.e tag-in{}/ignition-on{}".format(percentage_engine_on_w_tagins,self.tag_in,self.ignition_on), file=open("output.txt", "a"))
            if percentage_engine_on_w_tagins <95:
                score = score - 1.5
            engine_on_wo_tagins = abs(int(self.ignition_on) - int(self.tag_in))
            if engine_on_wo_tagins>0:
                print( "There was {} trips with no tag-ins".format(engine_on_wo_tagins), file=open("output.txt", "a"))
                if engine_on_wo_tagins > 5:
                    score= score-1.5
            else:
                print("All trips appear to have associated Tag-ins", file=open("output.txt", "a"))
        else:
            if (int(self.ignition_on)>0):
                print("No ignition On events for tag-in events", file=open("output.txt", "a"))
            else:
                print("No Tag-In events for ignition on events", file=open("output.txt", "a"))


        print("-----------Journey Summary Analysis--------------", file=open("output.txt", "a"))

        if (int(self.journey_summary)>0):
            journey_summary_accuracy_ign_off = (int(self.ignition_off) / int(self.journey_summary)) * 100
            print("Journey summary accuracy is based on engine Off is {} i.e ignitionoff {} / journey summary {}".format(journey_summary_accuracy_ign_off,self.ignition_off,self.journey_summary), file=open("output.txt", "a"))
            if journey_summary_accuracy_ign_off < 95:
                score = score - 1.5
        else:
            if (int(self.ignition_on) > 0):
                score = score -2
                print(" The device has no journey summary but has ignition on events", file=open("output.txt", "a"))


        print("-----------Idling Analysis--------------", file=open("output.txt", "a"))

        if (int(self.idle_start)>0 or int(self.idle_end>0)):
            if int(self.idle_end)>0:
                idling_acc_percentage = int(self.idle_start)/int(self.idle_end)*100
                print("Idling pair accuracy is {} i.e idle start {} / idle end {}".format(idling_acc_percentage,self.idle_start,self.idle_end), file=open("output.txt", "a"))
            else:
                idling_acc_percentage =0
                print("Idling pair accuracy is {} i.e idle start {} / idle end {}".format(idling_acc_percentage,
                                                                                          self.idle_start,
                                                                                          self.idle_end), file=open("output.txt", "a"))
            idle_mismatch=abs(int(self.idle_start)-int(self.idle_end))
            if idle_mismatch>0:
               print("There is a mismatch of {}".format(idle_mismatch), file=open("output.txt", "a"))
               if idle_mismatch>4:
                score = score - 1.5
        else:
            print("No idling events occured", file=open("output.txt", "a"))

        if int(power_up)>0:
            print("-----------Unit/Vehicle Health--------------", file=open("output.txt", "a"))
            if int(self.ext_power_loss)>0 or int(self.ext_power_restore)>0:
                print("The unit has power ups @{} events ".format(self.power_up), file=open("output.txt", "a"))
                print (" The unit has external power loss @ {} & external power restore @ {} perhaps indicating a wiring issue".format(self.ext_power_loss,self.ext_power_restore), file=open("output.txt", "a"))
                score = score - 1
            else:
                print("The unit has power ups @{} events but no external power loss or power restore. This indicates the loss of unit power abruptly due to depleted battery".format(self.power_up), file=open("output.txt", "a"))
                score = score - 1

        print("-----------Unit Comm Health--------------", file=open("output.txt", "a"))
        if int(self.heartbeat)>0:
            print("The heartbeat events were {}".format(self.heartbeat), file=open("output.txt", "a"))
        else:
            print("No heartbeat events were recoreded", file=open("output.txt", "a"))

        print("-----------Driver Behaviour--------------", file=open("output.txt", "a"))
        if int(self.driver_behaviour)>0:
            print ("There were {} events triggered due to driver behaviour".format(self.driver_behaviour), file=open("output.txt", "a"))
        else:
            print ("There were no events triggered due to driver behaviour", file=open("output.txt", "a"))

        print("-----------Vehicle Usage--------------", file=open("output.txt", "a"))
        if int(self.journey_periodic)>0:
            estimated_active_time=int(self.journey_periodic)*15#reportin rate at 15
            print("The estimated active time is {} minutes".format(estimated_active_time), file=open("output.txt", "a"))

        print("-----------Work in progress--------------", file=open("output.txt", "a"))
        print("Other event counts is {}".format(self.others), file=open("output.txt", "a"))

        print("-----------Summary--------------", file=open("output.txt", "a"))
        print ("Total event type counts = {} and total event counts = {}".format(self.event_count,self.total_event), file=open("output.txt", "a"))
        print ("QA score = {}/15".format(score), file=open("output.txt", "a"))
        print("###########################################", file=open("output.txt", "a"))
        # if self.ignition_on == self.ignition_off:
        #    print(self.ignition_on)
        #    print (" Perfect ignition ")
        #
        # if self.tag_in == self.tag_out:
        #     print(self.tag_in)
        #     print("Perfect Tags")


with open('EOEventCount.csv','r') as csvfile:
    reader = csv.reader(csvfile)
    rowcount=0
    total_assets=0
    assets_reported=0
    total_event = 0
    tag_in = 0
    tag_out = 0
    ignition_on = 0
    ignition_off = 0
    idle_start = 0
    idle_end = 0
    journey_periodic = 0
    journey_summary = 0
    heartbeat = 0
    power_up = 0
    command_response = 0
    ext_power_loss = 0
    ext_power_restore = 0
    event_count = None
    total_event = None
    driver_behaviour = 0
    others =0
    first_entry_flag = True
    for row in reader:
        rowcount += 1
        # skip first 7 lines
        if rowcount > 7:
            # print ("starts the data processing")
            # print(row)
            # row[1] and row[3] same means they have no data this usually indicates a new asset data follows
            if (row[1] == row[3]):
                #print("entered condition indicaiting new asset")
                total_assets+=1
                #print (row)
                #now we check if this is the first entry
                if first_entry_flag:
                    #print("entered first entry")
                    #print (row)
                    current_asset = asset(str(row[0]))
                    # we set the flag to False
                    first_entry_flag=False
                else:
                    #print("entered else")
                    # we save the existing data to the class
                    current_asset.add_events(ignition_on,ignition_off,tag_in,tag_out,idle_start,idle_end,journey_periodic,journey_summary,heartbeat,power_up,command_response,ext_power_loss,ext_power_restore,others,driver_behaviour)
                    current_asset.add_summary(event_count,total_event)
                    # we process data for the asset in memorry

                    # process the Analysis
                    current_asset.processQA()
                    #prepare a sheet
                    current_asset.createsheet()
                    current_asset = asset(str(row[0]))


                    # create new asset
                    #print(row[0])
                    current_asset = asset(str(row[0]))

                    # initialize all counter variables to 0
                    total_event = 0
                    tag_in = 0
                    tag_out = 0
                    ignition_on = 0
                    ignition_off = 0
                    idle_start = 0
                    idle_end = 0
                    journey_periodic = 0
                    journey_summary = 0
                    heartbeat = 0
                    power_up = 0
                    driver_behaviour = 0
                    event_count = 0
                    others = 0

            # if the read line has count in the second columm this indicates the end of the asset information
            elif str(row[1]).startswith('Count'):

                if current_asset.asset_name == row[0]:
                    event_count = row[1]
                    total_event = row [3]

                    #print (rowcount)
                    #print(row)
                    assets_reported += 1

            # if the row zero starts with assetname equal to class namen then we need to save this
            elif str(row[0]) == current_asset.asset_name :

                if row[2] == 'Ignition On':
                    ignition_on = row[3]
                elif row[2] == 'Ignition Off':
                    ignition_off = row [3]
                elif row[2] == 'Tag In':
                    tag_in = row [3]
                elif row[2] == 'Tag Out':
                    tag_out = row [3]
                elif row[2] == 'Idle Start':
                    idle_start = row [3]
                elif row[2] == 'Idle End':
                    idle_end = row [3]
                elif row[2] == 'Journey Periodic':
                    journey_periodic = row [3]
                elif row[2] == 'Journey Summary':
                    journey_summary = row [3]
                elif row[2] == 'Heartbeat':
                    heartbeat = row[3]
                elif row[2] == 'Power Up':
                    power_up = row[3]
                elif row[2] == 'Harsh Cornering':
                    driver_behaviour += int(row[3])
                elif row[2]  == 'Harsh Acceleration':
                    driver_behaviour += int(row[3])
                elif row[2] == 'Harsh Deceleration':
                    driver_behaviour += int(row[3])
                elif row[2] == 'Harsh RPM':
                    driver_behaviour += int(row[3])
                else:
                    others +=1




    print (" There are a total of {} assets".format(total_assets))
    print (" There are a total of {} assets that reported".format(assets_reported))


# for line in file:
#     print (line)
