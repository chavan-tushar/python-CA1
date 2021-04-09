
#To check if Payslips folder exits, if not then it will create that folder.
import os

path = "/home/tushar/StudyMaterial/python-CA1/Accounts/Payslips"
if(not os.path.isdir(path)):
    os.makedirs(path)   #makedirs is used to create /Accounts/Payslips.


#This function will read the data from Employees.txt file.
def getStaffDetails(staffID):
    with open("./Accounts/Employees.txt") as empData:
        for empDetails in empData:
            empDetailsList = empDetails.split()
            if staffID == empDetailsList[0]:
                surname = empDetailsList[1]
                firstName = empDetailsList[2]
                PPSNumber = empDetailsList[3]
                stdHrs = float(empDetailsList[4])
                hrRate = float(empDetailsList[5])
                overTimeRate = float(empDetailsList[6])
                taxCredit = float(empDetailsList[7])
                stdBand = float(empDetailsList[8])

                return surname,firstName,PPSNumber,stdHrs,hrRate,overTimeRate,taxCredit,stdBand

#This function will read the data from Taxrates.txt
def getTaxRates():
    with open("./Accounts/Taxrates.txt") as tr:
        for data in tr:
            taxRate = data.split()
            stdRate = float(taxRate[0])
            highRate = float(taxRate[1])

            return stdRate,highRate


with open("./Accounts/Hours.txt") as hrs:
    for data in hrs:
        dataInList = data.split()
        forWeek = dataInList[0]
        forStaffID = dataInList[1]
        hrsWorked = float(dataInList[2])

        #Below code is used to convert DD/MM/YYYY into YYYY_MM_DD format.
        date, month, year = forWeek.split("/")
        formatedDate = "_".join([year, month, date])

        #Below lines will call function and data will be stored in approriate variables
        surname, firstName, PPSNumber, stdHrs, hrRate, overTimeRate, taxCredit, stdBand = getStaffDetails(forStaffID)
        stdRate, highRate = getTaxRates()

        regHrs,overTimeHrs = 0,0
        if(hrsWorked > stdHrs):
            regHrs = hrsWorked - stdHrs
            overTimeHrs = hrsWorked - regHrs
        elif (hrsWorked > 0 and hrsWorked <= stdHrs ):
            regHrs = hrsWorked
        else:
            overTimeHrs = hrsWorked

        #Creating payslips
        with open(f"./Accounts/Payslips/{forStaffID}_{formatedDate}.txt.","w") as ps:

            #Calculations to be used while printing Payslip
            salFromRegHrs = regHrs*hrRate
            salFromOvertimeHrs = overTimeHrs * overTimeRate
            grossPay = salFromRegHrs + salFromOvertimeHrs
            partOfSalForStdRate = stdBand if (grossPay > stdBand) else grossPay
            partOfSalForHighRate = 0 if (grossPay <= stdBand) else grossPay - stdBand
            dedFromStdRate = ((partOfSalForStdRate * stdRate) / 100)
            dedFromHighRate = 0 if (grossPay <= stdBand) else ((highRate * partOfSalForHighRate ) / 100)
            totalDeduction = dedFromStdRate + dedFromHighRate
            netDeduction = totalDeduction - taxCredit if (totalDeduction - taxCredit > 0) else 0
            netPay = grossPay - netDeduction

            #Printing a Payslip
            ps.writelines("\n\t\t\t\tPAYSLIP\n\n\n");
            ps.writelines(f"StaffID: {forStaffID}\n");
            ps.writelines(f"Staff Name: {firstName} {surname}\n");
            ps.writelines(f"PPSN: {PPSNumber}\n");
            ps.writelines(f"Date: {forWeek}\n");
            ps.writelines(f"\t\t\tHours\t\tRate\t\tTotal\n");
            ps.writelines(f"Regular\t\t{regHrs}\t\t{hrRate}\t\t{salFromRegHrs}\n");
            ps.writelines(f"Overtime\t\t{overTimeHrs}\t\t{overTimeRate}\t\t{salFromOvertimeHrs}\n\n");
            ps.writelines(f"Gross Pay\t{grossPay}\n\n")
            ps.writelines(f"\t\t\t\t\tRate\t\tTotal\n");
            ps.writelines(f"Standard Band\t\t{partOfSalForStdRate}\t\t{stdRate}%\t\t{dedFromStdRate}\n");
            ps.writelines(f"Higher Rate\t\t{partOfSalForHighRate}\t\t{highRate}%\t\t{dedFromHighRate}\n\n");
            ps.writelines(f"Total Deductions\t{totalDeduction}\n");
            ps.writelines(f"Tax Credit\t\t{taxCredit}\n");
            ps.writelines(f"Net Deduction\t\t{netDeduction}\n");
            ps.writelines(f"Net Pay\t\t{netPay}\n");
