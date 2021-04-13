
#To check if Payslips folder exits, if not then it will create that folder.
import datetime
import os
import datetime

# makedirs is used to create folder in hierarical order e.g /python-CA1/Accounts/Payslips.
payslipPath = "/home/tushar/StudyMaterial/python-CA1/Accounts/Payslips"
if(not os.path.isdir(payslipPath)):
    os.makedirs(payslipPath)

avgGrossPaypath = "/home/tushar/StudyMaterial/python-CA1/Accounts/AvgGrossPay"
if(not os.path.isdir(avgGrossPaypath)):
    os.makedirs(avgGrossPaypath)


weekwisePayDict = {}
staffwisePayDict = {}

#date is converted from YYYY-MM-DD format to YYYY_MM_DD format
#timedelta is used to get date 6 weeks before.
currentDate = "_".join(str(datetime.datetime.today()).split()[0].split("-"))
previousDate = "_".join(str(datetime.datetime.today() - datetime.timedelta(days=42)).split()[0].split("-"))
staffIDwithError = []

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

#This function will write errors into Errors_{currentDate} file.
#some rows will have only error message where as some rows will have staffID and Error Message
#Hence *args is used as number of arguments are not fixed.
def writeError(*args):
    with open(f"./Accounts/Errors_{currentDate}.txt","a") as err:
        if len(args) == 1:
            err.writelines(f"{args[0]}\n")
        elif len(args) == 2:
            err.writelines(f"Staff ID {args[0]} | {args[1]}\n")

#It will be a starting point of the code.
#Every Record from Hours.txt file will be checked in Employees.txt file and Payslip will be generated.
with open("./Accounts/Hours.txt") as hrs:
    for data in hrs:
        dataInList = data.split()
        forWeek = dataInList[0]
        forStaffID = dataInList[1]
        hrsWorked = float(dataInList[2])

        #if there is an error for some staffid then it will be added in staffIDwithError list.
        #for loop will not be executed for remaining occurances for that staff it.
        if forStaffID not in staffIDwithError:

            #Convert DD/MM/YYYY into YYYY_MM_DD format.
            try:
                date, month, year = forWeek.split("/")
            except ValueError:
                # StaffID is not added in staffIDwithError list as
                #there might be another record for same employee in Hours.txt with correct/required date format.
                writeError(forStaffID, "Payslip Not Generated, Reason - Incorrect Date Format in Hours.txt file")
                continue

            formatedDate = "_".join([year, month, date])

            #Below lines will call functions and data will be stored in approriate variables
            try:
                surname, firstName, PPSNumber, stdHrs, hrRate, overTimeRate, taxCredit, stdBand = getStaffDetails(forStaffID)
            except TypeError:
                writeError(forStaffID, "Payslip Not Generated, Reason - Details Not Found in Employees.txt file")
                staffIDwithError.append(forStaffID)
                continue
            except FileNotFoundError:
                writeError("Employees.txt file is not available in 'Accounts' Folder")
                break
            except ValueError:
                writeError(forStaffID, "Payslip Not Generated, Reason - Data is not provided in required format in Employee.txt file")
                staffIDwithError.append(forStaffID)
                continue
            finally:
                if stdHrs < 0 or hrRate <= 0 or overTimeRate <=0 or taxCredit < 0:
                    writeError(forStaffID,"Payslip Not Generated, Reason - Incorrect Data in Employees.txt file")
                    staffIDwithError.append(forStaffID)
                    continue

            try:
                stdRate, highRate = getTaxRates()
            except TypeError:
                writeError("Data Missing in Taxrates.txt file.")
                break
            except FileNotFoundError:
                writeError("Taxrates.txt file is not available in 'Account' folder.")
                break
            except ValueError:
                writeError("Data in Taxrates.txt file is not in required format.")
                break
            finally:
                if (stdRate < 0 or stdRate > 100) or (highRate < 0 or highRate > 100):
                    writeError("Incorrect Data in Taxrates.txt file.")
                    break

            regHrs, overTimeHrs = 0, 0
            if(hrsWorked > stdHrs):
                regHrs = stdHrs
                overTimeHrs = hrsWorked - regHrs
            elif (hrsWorked > 0 and hrsWorked <= stdHrs ):
                regHrs = hrsWorked
            else:
                overTimeHrs = hrsWorked

            if regHrs > hrsWorked or regHrs > stdHrs:
                writeError(forStaffID, "Payslip Not Generated, Reason - Regular Hours greater than Standard Hours or Hours Worked")
                break
            elif overTimeHrs < 0:
                writeError(forStaffID,"Payslip Not Generated, Reason - Negative overtime hours")
                break

            #Creating payslips
            with open(f"./Accounts/Payslips/{forStaffID}_{formatedDate}.txt.", "w") as ps:

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


                if partOfSalForStdRate > stdBand or partOfSalForStdRate > grossPay or partOfSalForStdRate <= 0 or partOfSalForStdRate > grossPay:
                    writeError(forStaffID,"Payslip Not Generated, Reason - Incorrect Standard Band")
                    break
                elif partOfSalForHighRate < 0 or partOfSalForHighRate > grossPay:
                    writeError(forStaffID,"Payslip Not Generated, Reason - Incorrect Higher Rate")
                    break
                elif netDeduction < 0:
                    # it will never be less than 0 as while calculating its value is already being taken care.
                    # However it has been mentioned here just to be on a safer side.
                    writeError(forStaffID, "Payslip Not Generated, Reason - Negative Net Deduction")
                    break

                #Printing a Payslip
                ps.writelines("\n\t\t\t\tPAYSLIP\n\n\n")
                ps.writelines(f"StaffID: {forStaffID}\n")
                ps.writelines(f"Staff Name: {firstName} {surname}\n")
                ps.writelines(f"PPSN: {PPSNumber}\n")
                ps.writelines(f"Date: {forWeek}\n")
                ps.writelines(f"\t\t\tHours\t\tRate\t\tTotal\n")
                ps.writelines(f"Regular\t\t{regHrs}\t\t{hrRate}\t\t{salFromRegHrs}\n")
                ps.writelines(f"Overtime\t\t{overTimeHrs}\t\t{overTimeRate}\t\t{salFromOvertimeHrs}\n\n")
                ps.writelines(f"Gross Pay\t{grossPay}\n\n")
                ps.writelines(f"\t\t\t\t\tRate\t\tTotal\n")
                ps.writelines(f"Standard Band\t\t{partOfSalForStdRate}\t\t{stdRate}%\t\t{dedFromStdRate}\n")
                ps.writelines(f"Higher Rate\t\t{partOfSalForHighRate}\t\t{highRate}%\t\t{dedFromHighRate}\n\n")
                ps.writelines(f"Total Deductions\t{totalDeduction}\n")
                ps.writelines(f"Tax Credit\t\t{taxCredit}\n")
                ps.writelines(f"Net Deduction\t\t{netDeduction}\n")
                ps.writelines(f"Net Pay\t\t{netPay}\n")

            #it will check if data for that week is already present in weekwisePayDict
            #if data is present then it will add gross pay of current staff to gross pay and count of staff will be increase by 1
            #if data is not present then it will add a list containing gross pay and initial count as 1 for that week.
            if formatedDate in weekwisePayDict.keys():
                weekwisePayDict[formatedDate][0] += grossPay
                weekwisePayDict[formatedDate][1] += 1
            else:
                weekwisePayDict[formatedDate] = [grossPay, 1]


            if forStaffID in staffwisePayDict.keys():
                staffwisePayDict[forStaffID].append([formatedDate,grossPay])
            else:
                staffwisePayDict[forStaffID] = [[formatedDate, grossPay]]

#to print weekly average gross pay

with open("./Accounts/AvgGrossPay/WeekwiseGrossPayForAllWorkers.txt", "w") as WGP:
    for week, data in weekwisePayDict.items():
        #print(f"Weekly Average Gross Pay for all workers for week {week} is {data[0]/data[1]}")
        WGP.writelines(f"Weekly Average Gross Pay of all workers for week {week} is {data[0]/data[1]}\n")

with open("./Accounts/AvgGrossPay/StaffwiseGrossPay.txt", "w") as SGP:
    for staffID, payDetails in staffwisePayDict.items():
        if len(payDetails) >= 2:
            payDetails.sort()
            payForLastSixMonth = 0
            for lastSixWeek, lastSixWeekPay in payDetails[-6:]:
                if lastSixWeek >= previousDate:
                    payForLastSixMonth += lastSixWeekPay
            #print(f"Six-week rolling Average gross pay for {staffID} is {payForLastSixMonth/6}")
            SGP.writelines(f"Six-week rolling Average gross pay for Employee {staffID} is {payForLastSixMonth / 6}\n")
print(staffwisePayDict)