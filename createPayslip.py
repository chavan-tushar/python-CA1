import os
path = "/home/tushar/StudyMaterial/python-CA1/Accounts/Payslips"
if(not os.path.isdir(path)):
    os.makedirs(path)

def getStaffDetails(staffID):
    with open("./Accounts/Employees.txt") as empData:
        for empDetails in empData:
            empDetailsList = empDetails.split()
            if staffID == empDetailsList[0]:


                surname = empDetailsList[1];
                firstName = empDetailsList[2];
                PPSNumber = empDetailsList[3];
                stdHrs = empDetailsList[4];
                hrRate = empDetailsList[5];
                overTimeRate = empDetailsList[6];
                taxCredit = empDetailsList[7];
                stdBand = empDetailsList[8];

                return surname,firstName,PPSNumber,stdHrs,hrRate,overTimeRate,taxCredit,stdBand;

def getTaxRates():
    with open("./Accounts/Taxrates.txt") as tr:
        for data in tr:
            taxRate = data.split();
            stdRate = taxRate[0];
            highRate = taxRate[1];

            return stdRate,highRate;


with open("./Accounts/Hours.txt") as hrs:
    for data in hrs:
        dataInList = data.split();
        forWeek = dataInList[0];
        forStaffID = dataInList[1];
        hrsWorked = dataInList[2];

        #Below code is used to convert DD/MM/YYYY into YYYY_MM_DD format.
        date, month, year = forWeek.split("/")
        formatedDate = "_".join([year, month, date])

        surname, firstName, PPSNumber, stdHrs, hrRate, overTimeRate, taxCredit, stdBand = getStaffDetails(forStaffID);
        stdRate, highRate = getTaxRates();



        with open(f"./Accounts/Payslips/{forStaffID}_{formatedDate}.txt.","w") as ps:
            ps.writelines("\n\t\t\t\tPAYSLIP\n\n\n");
            ps.writelines(f"StaffID: {forStaffID}\n");
            ps.writelines(f"Staff Name: {firstName} {surname}\n");
            ps.writelines(f"PPSN: {PPSNumber}\n");
            ps.writelines(f"Date: {forWeek}\n");
            ps.writelines(f"\t\t\tHours\t\tRate\t\tTotal\n");
            ps.writelines(f"Regular\t\t{float(hrsWorked)-float(stdHrs)}");