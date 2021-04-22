import datetime
import os

payslipPath = "/home/tushar/StudyMaterial/python-CA1/Accounts/Payslips"
if (not os.path.isdir(payslipPath)):
    os.makedirs(payslipPath)


#date conversion
currentDate = "_".join(str(datetime.datetime.today()).split()[0].split("-"))


#To read data from Employees.txt file.
def getStaffDetails(staffID):
    with open("/home/tushar/StudyMaterial/python-CA1/Accounts/Employees.txt") as empData:
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
    with open("/home/tushar/StudyMaterial/python-CA1/Accounts/Taxrates.txt") as tr:
        for data in tr:
            taxRate = data.split()
            stdRate = float(taxRate[0])
            highRate = float(taxRate[1])

            return stdRate,highRate

#Every Record from Hours.txt file will be checked in Employees.txt file and Payslip will be generated.
with open("/home/tushar/StudyMaterial/python-CA1/Accounts/Hours.txt") as hrs:
    for data in hrs:

        dataInList = data.split()
        forWeek = dataInList[0]
        forStaffID = dataInList[1]
        hrsWorked = float(dataInList[2])



        #Convert DD/MM/YYYY into YYYY_MM_DD format.
        try:
            date, month, year = forWeek.split("/")
        except ValueError:
            print(forStaffID, " | Payslip Not Generated for week", forWeek, "Reason - Incorrect Date Format in Hours.txt file")
            continue

        formatedDate = "_".join([year, month, date])

        #Below lines will call functions and data will be stored in approriate variables
        try:
            surname, firstName, PPSNumber, stdHrs, hrRate, overTimeRate, taxCredit, stdBand = getStaffDetails(forStaffID)
        except TypeError:
            print(forStaffID, " | Payslip Not Generated, Reason - Details Not Found in Employees.txt file")
            continue
        except FileNotFoundError:
            print("Employees.txt file is not available in 'Accounts' Folder")
            break
        except ValueError:
            print(forStaffID, " | Payslip Not Generated, Reason - Data is not provided in required format in Employee.txt file")
            continue
        finally:
            if stdHrs < 0 or hrRate <= 0 or overTimeRate <=0 or taxCredit < 0:
                print(forStaffID," | Payslip Not Generated, Reason - Incorrect Data in Employees.txt file")
                continue

        try:
            stdRate, highRate = getTaxRates()
        except TypeError:
            print("Data Missing in Taxrates.txt file.")
            break
        except FileNotFoundError:
            print("Taxrates.txt file is not available in 'Account' folder.")
            break
        except ValueError:
            print("Data in Taxrates.txt file is not in required format.")
            break
        finally:
            if (stdRate < 0 or stdRate > 100) or (highRate < 0 or highRate > 100):
                print("Incorrect Data in Taxrates.txt file.")
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
            print(forStaffID, " | Payslip Not Generated  for week", forWeek, "Reason - Regular Hours greater than Standard Hours or Hours Worked")
            break
        elif overTimeHrs < 0:
            print(forStaffID, "| Payslip Not Generated  for week", forWeek, "Reason - Negative overtime hours")
            break

        #Creating payslips
        with open(f"{payslipPath}/{forStaffID}_{formatedDate}.txt", "w") as ps:

            #Calculations to be used while printing Payslip
            salFromRegHrs = regHrs*hrRate
            salFromOvertimeHrs = overTimeHrs * overTimeRate
            grossPay = salFromRegHrs + salFromOvertimeHrs
            if (grossPay > stdBand):
                partOfSalForStdRate = stdBand
            else:
                partOfSalForStdRate = grossPay

            if (grossPay <= stdBand):
                partOfSalForHighRate = 0
            else:
                partOfSalForHighRate = grossPay - stdBand

            dedFromStdRate = ((partOfSalForStdRate * stdRate) / 100)

            if (grossPay <= stdBand):
                dedFromHighRate = 0
            else:
                dedFromHighRate = ((highRate * partOfSalForHighRate ) / 100)

            totalDeduction = dedFromStdRate + dedFromHighRate

            if (totalDeduction - taxCredit > 0):
                netDeduction = totalDeduction - taxCredit
            else:
                netDeduction = 0

            netPay = grossPay - netDeduction


            if partOfSalForStdRate > stdBand or partOfSalForStdRate > grossPay or partOfSalForStdRate <= 0 or partOfSalForStdRate > grossPay:
                print(forStaffID, " | Payslip Not Generated  for week", forWeek, " Reason - Incorrect Standard Band")
                break
            elif partOfSalForHighRate < 0 or partOfSalForHighRate > grossPay:
                print(forStaffID, " | Payslip Not Generated  for week", forWeek," Reason - Incorrect Higher Rate")
                break
            elif netDeduction < 0:
                print(forStaffID, " | Payslip Not Generated  for week", forWeek, "Reason - Negative Net Deduction")
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

print("Payslips Generated. Thank you !")