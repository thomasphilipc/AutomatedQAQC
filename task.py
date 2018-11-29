import csv
import datetime


requiredDir = 'd:\\QA'



class asset:
    asset_name = None
    total_journeys = None
    total_power_ups = None
    total_fault_pu = None
    total_jusm = None
    total_dup_jsum=None
    raw_events=list()

    def __init__(self, asset_name):
        self.asset_name = asset_name
        self.raw_events=[]

    def add_raw_Event(self,data):
        self.raw_events.append(data)

    def view_events(self):
        return (self.raw_events.reverse())

    def print_summary(self):
        print("{},{},{},{},{},{}".format(asset.asset_name,asset.total_journeys,asset.total_power_ups,asset.total_fault_pu,asset.total_jusm,asset.total_dup_jsum))


total_assets=0

total_assets= list()

def time_process(string):
    #20/09/2018 18:09:44 GMT+4
    date = datetime.datetime.strptime(string, '%d/%m/%Y %H:%M:%S GMT+4')
    return (date)

def analyse(asset):
    print("Analysing Asset {} that has {} events".format(asset.asset_name,len(asset.raw_events)))

def analyse_event_powerups(data,asset):
    #print(data)
    fault_counter=0
    normal_counter=0
    Journey_in_progess=False
    event_cursor=0
    total_journeys=0
    for i in data:

        time_min_diff,event_type = i
        if event_type=="Ignition On":
            Journey_in_progess=True
        elif Journey_in_progess and event_type=="Ignition Off":
            Journey_in_progess=False
            total_journeys+=1
        elif event_type=="Power Up" and Journey_in_progess:
            print("**Power Up** observed during Journey around {} event after {} min from the previous event".format(event_cursor,time_min_diff))
            fault_counter=fault_counter+1
            try:
                spacer="          "
                print(spacer+"Sequence below")
                print(spacer+asset.raw_events[event_cursor-1])
                print(spacer+asset.raw_events[event_cursor])
                print(spacer+asset.raw_events[event_cursor+1])
            except:
                print("Out of range")
        elif event_type=="Power Up" and (not Journey_in_progess):
            #print(" Reasonable power up")
            normal_counter=normal_counter+1
        event_cursor=event_cursor+1
    if fault_counter>0 or normal_counter>0:
        print("There were {} Power Up faults and {} normals for {}".format(fault_counter,normal_counter,asset.asset_name))
    asset.total_journeys,asset.total_power_ups,asset.total_fault_pu = total_journeys,fault_counter+normal_counter,fault_counter

def analyse_event_jsum_dup(data,asset):
    #print(data)
    fault_counter=0
    event_cursor=0
    for i in data:

        time_min_diff,event_type = i
        if event_type=="Journey Summary" and time_min_diff==0:
            if (asset.raw_events[event_cursor-1].split(',')[1]=="Journey Summary"):
                print("**Duplicate Journey Summary** observed around {} event after {} min from the previous event".format(event_cursor,time_min_diff))
                fault_counter=fault_counter+1
                try:
                    spacer="          "
                    print(spacer+"Sequence below")
                    print(spacer+asset.raw_events[event_cursor-1])
                    print(spacer+asset.raw_events[event_cursor])
                    print(spacer+asset.raw_events[event_cursor+1])
                except:
                    print("Out of range")

        event_cursor=event_cursor+1
    if fault_counter>0:
        print("{} faults for  {} ".format(fault_counter,asset.asset_name))
        asset.total_dup_jsum = fault_counter

def analyse_event_summary(data,asset):
    #try:
    event_type_list=[]
    event_type_set_list=[]
    event_type_count_list=[]
    for i in data:
        time_min_diff,event_type = i
        event_type_list.append(event_type)

    for i in set(event_type_list):
        event_type_set_list.append(i)
        event_type_count_list.append(event_type_list.count(i))


    if "Power Up" in event_type_set_list and "Ignition On" in event_type_set_list:
        print(event_type_set_list)
        print(event_type_count_list)
        pwrup_cursor=event_type_set_list.index("Power Up")
        ignition_cursor=event_type_set_list.index("Ignition On")
        percent_powerup=(event_type_count_list[pwrup_cursor]/event_type_count_list[ignition_cursor])*100
        print("percentage of power up to trips are {}".format(round(percent_powerup)))
        jsum_cursor=event_type_set_list.index("Journey Summary")
        asset.total_jusm= event_type_count_list[jsum_cursor]
    #except:
    #    print("Error not sufficent data")

with open(requiredDir + "\\"+'actual.csv','r') as csvfile:
    reader = csv.reader(csvfile)

    rowcount=0
    first_entry_flag = True
    fault_flag=False
    current_asset=None
    cursor=0
    myasset=asset(None)

    for row in reader:
        #check row count
        rowcount += 1
        # skip first 9 lines which are comments
        if (rowcount >10 ):
            if (row[1] != ''):
                name=myasset.asset_name
                if not(row[1].startswith('Count:')):
                    #print("{} - {} : {}".format(name,rowcount-cursor,row))
                    myasset.add_raw_Event(row[0]+','+row[1]+','+row[3]+','+row[4])
            elif (not(row[0] in ["Grand Totals",""]) or (len(row[0]) > 15)):
                if (myasset.asset_name):
                    myasset.raw_events.reverse()
                    total_assets.append(myasset)
                    #analyse(myasset)
                #print ("New Asset: {} ".format(row[0]))
                myasset=asset(row[0])
                cursor=rowcount
            else:
                total_assets.append(myasset)


for asset in total_assets:
    timestamp_list = []
    timestamp_list_event=[]
    print(asset.asset_name)
    if len(asset.raw_events)>0:
        for event in asset.raw_events:
            #print(event)
            timestamp_list.append(time_process(event.split(',')[2]))
            timestamp_list_event.append((event.split(',')[1]))
        #analyse(i)
    #print(timestamp_list)
    timestamp_list_len=len(timestamp_list)
    timestamp_diff_min_withevent=[]
    for i in range(0,timestamp_list_len):
        if i>0:
            time_difference = timestamp_list[i]-timestamp_list[i-1]
            #print(timestamp_list[i])
            #print(timestamp_list[i-1])
            timestamp_diff_min_withevent.append((round((time_difference.days * 86400 + time_difference.seconds)/60),timestamp_list_event[i]))
        else:
            timestamp_diff_min_withevent.append((None,timestamp_list_event[0]))
    #print(timestamp_diff_min_withevent)
    if asset.asset_name:
        print("Analysing Power ups")
        data=analyse_event_powerups(timestamp_diff_min_withevent,asset)
        print("Analysing Journey summary duplicates")
        data=analyse_event_jsum_dup(timestamp_diff_min_withevent,asset)
        print("Anlysing event summary")
        data=analyse_event_summary(timestamp_diff_min_withevent,asset)
        print("-----------------------------------------------------")



for asset in total_assets:
    asset.print_summary()
