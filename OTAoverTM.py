import csv

# declare a class to manage the action
class asset:
    imei = None
    status_flag = True
    failed_lines = []


    # function to initialize class
    def __init__(self, imei):
        self.imei = imei
        self.status_flag = True

    # function to check if the identifier line was a successs or fail
    def check_status(self,identifier,text):

        if (identifier in text):
            # print (self.status_flag)
            # print(self.imei)
            # print("text {}".format(text))
            # print("idenitifer{}".format(identifier))
            if ("$SUCCESS$" in text):
                if self.status_flag == False:
                    self.status_flag = False
            else:
                self.status_flag = False
        if (text == "Failed"):
            self.status_flag = False



# open the file that contains the list of lines
with open('WT-ST1.csv','r') as csvfile:
    reader = csv.reader(csvfile)

    first_entry= True
    rowcount = 0
    current_imei=None
    success_count = 0
    success =True
    for row in reader:
        # check row count
        rowcount += 1

        #skip the first line which is headers
        if rowcount>1:

            # print the row
            #print (row)
            # split the row at every occurunce of | (pipe sign)
            list=row[0].split("|")

            #print (" read value :{} current in-memory: {} ".format(list[0],current_imei))

            # if this is the first entry create a list
            if first_entry:
                print("first entry")
                # obtain the current Imei
                current_imei=list[0]
                first_entry=False
                #assign the class witht he current imei
                current_asset = asset(current_imei)


            # the content to parse is stored in text
            text=list[2]



            # check if the imei is same as the current imei
            if list[0] == current_asset.imei:

                # print(current_asset.status_flag)
                # print(current_asset.imei)
                # print("text {}".format(text))


                current_asset.check_status("CNF.EraseBackup",text)
                current_asset.check_status("AL29",text)
                current_asset.check_status("AL34",text)
                current_asset.check_status("AL81",text)
                current_asset.check_status("AL82",text)
                current_asset.check_status("AL76",text)
                current_asset.check_status("AL99",text)
                current_asset.check_status("AL83",text)
                current_asset.check_status("DEVICE.CMD.PFAL.EN",text)
                current_asset.check_status("CNF.EraseBackup",text)


            else:
                print ("new asset reached")
                print ("{} is current imei , {} is read imei".format(current_imei,list[0]))
                if current_asset.status_flag:
                    print("Analysis for {} is Suceess".format(current_imei))
                    current_imei = list[0]
                    current_asset = asset(current_imei)
                else:
                    print("Analysis for {} has failed".format(current_imei))
                current_imei = list[0]
                current_asset = asset(current_imei)






