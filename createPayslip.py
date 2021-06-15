import datetime
import os

# makedirs is used to create folder in hierarical order e.g /python-CA1/Accounts/Payslips.
#To check if Payslips folder exits, if not then it will create that folder.
def createFolder(pathToCreateFolder):
    if (not os.path.isdir(pathToCreateFolder)):
        os.makedirs(pathToCreateFolder)

#Need to update base path where createPayslip.py file is kept.
basePath = "/home/tushar/StudyMaterial/pythonProject-CA1_Final"

payslipPath = f"{basePath}/Accounts/Payslips"
createFolder(payslipPath)

avgGrossPaypath = f"{basePath}/Accounts/AvgGrossPay"
createFolder(avgGrossPaypath)

errorPath = f"{basePath}/Accounts/Errors"
createFolder(errorPath)

#Dictionaries to store weekwise and staffwise data
#list to store staffIds which are not present in employess.txt file or staff id is present but data is not in required format.
weekwisePayDict = {}
staffwisePayDict = {}
staffIDwithError = []

#date is converted from YYYY-MM-DD format to YYYY_MM_DD format
#timedelta is used to get date 6 weeks before.
currentDate = "_".join(str(datetime.datetime.today()).split()[0].split("-"))
previousDate = "_".join(str(datetime.datetime.today() - datetime.timedelta(days=42)).split()[0].split("-"))


#Creating Blank Error File.
with open(f"{errorPath}/Errors_{currentDate}.txt","w") as err:
    pass

#This function will write errors into Errors_{currentDate} file.
#some rows will have only error message where as some rows will have staffID and Error Message
#Hence *args is used as number of arguments are not fixed.
def writeError(*args):
    with open(f"{errorPath}/Errors_{currentDate}.txt","a") as err:
        if len(args) == 1:
            err.writelines(f"{args[0]}\n")
        elif len(args) == 2:
            err.writelines(f"Staff ID {args[0]} | {args[1]}\n")

#This function will check if all required files are present.
#if some file is not available then it will change allfilesAvailable flag to False.
allFilesAvailable = True
def isFileAvailable(path):
    if (not os.path.exists(path)):
        writeError(f"{path} file is not Available.")
        globals()['allFilesAvailable'] = False


employeeFile = f"{basePath}/Accounts/Employees.txt"
isFileAvailable(employeeFile)

taxRateFile = f"{basePath}/Accounts/Taxrates.txt"
isFileAvailable(taxRateFile)

hoursFile = f"{basePath}/Accounts/Hours.txt"
isFileAvailable(hoursFile)


if allFilesAvailable:
    #created a list for all staff ids from employees.txt file.
    #This list will be used for searching staffid from hours.txt file into employess.txt file.
    #sorting is used as we have to use binary search algorithm.
    #next(empData) is used to skip the header row.
    allStaffIds = []
    if len(allStaffIds) == 0:
        with open(f"{basePath}/Accounts/Employees.txt") as empData:
            next(empData)
            for empDetails in empData:
                empDetailsList = empDetails.split()
                allStaffIds.append(empDetailsList[0])
            allStaffIds.sort()


    # Used binary search algo for identifying if any particular staff id is present in allStaffIds list.
    # It will be helpful if we have large data in employees.txt file
    # if particular staff id is not present then it will return False else it will return True.
    # We have assumed staff Id can contain character as well, hence haven't converted it to int.
    # def isStaffIdAvailable(staffID):
    #     left_index = 0
    #     right_index = len(allStaffIds) - 1
    #     mid_index = 0
    #
    #     while left_index <= right_index:
    #         mid_index = (left_index + right_index) // 2
    #
    #         if staffID < allStaffIds[mid_index]:
    #             right_index = mid_index - 1
    #         elif staffID > allStaffIds[mid_index]:
    #             left_index = mid_index + 1
    #         else:
    #             return True
    #     return False
    #

    # Used binary search algo for identifying if first parameter is present in list which is passed in second parameter.
    # It will be helpful if we have large data in which we have to find value passed in first parameter.
    # if value passed in first parameter is not present in list then it will return False.
    # We have assumed staff Id can contain character as well, hence haven't converted it to int.
    def isPresent(tofind,listName):
        left_index = 0
        right_index = len(listName) - 1
        mid_index = 0

        while left_index <= right_index:
            mid_index = (left_index + right_index) // 2

            if tofind < listName[mid_index]:
                right_index = mid_index - 1
            elif tofind > listName[mid_index]:
                left_index = mid_index + 1
            else:
                return True
        return False

    #This function will read the data from Employees.txt file.
    def getStaffDetails(staffID):
        with open(f"{basePath}/Accounts/Employees.txt") as empData:
            next(empData)

            for empDetails in empData:
                empDetailsList = empDetails.split()

                if staffID == empDetailsList[0]:
                    surname = empDetailsList[1]
                    firstName = empDetailsList[2]
                    PPSNumber = empDetailsList[3]
                    try:
                        stdHrs = float(empDetailsList[4])
                        hrRate = float(empDetailsList[5])
                        overTimeRate = float(empDetailsList[6])
                        taxCredit = float(empDetailsList[7])
                        stdBand = float(empDetailsList[8])
                    except:
                        writeError(forStaffID,f"Payslip Not Generated for {forStaffID}, Reason - Incorrect Data in Employee.txt file")
                        staffIDwithError.append(forStaffID)
                        continue
                    return surname, firstName, PPSNumber, stdHrs, hrRate, overTimeRate, taxCredit, stdBand


    #This function will read the data from Taxrates.txt
    def getTaxRates():
        with open(f"{basePath}/Accounts/Taxrates.txt") as tr:
            next(tr)
            for data in tr:
                taxRate = data.split()
                stdRate = float(taxRate[0])
                highRate = float(taxRate[1])

                return stdRate,highRate



    #It will be a starting point of the code.
    #Every Record from Hours.txt file will be checked in Employees.txt file and Payslip will be generated.
    with open(f"{basePath}/Accounts/Hours.txt") as hrs:
        next(hrs)
        for data in hrs:

            dataInList = data.split()
            forWeek = dataInList[0]
            forStaffID = dataInList[1]
            try:
                hrsWorked = float(dataInList[2])
            except:
                writeError(forStaffID,f"Payslip Not Generated for week {forWeek}, Reason - Incorrect Data in Hours.txt file")
                continue

            #if there is an error for some staffid then it will be added in staffIDwithError list.
            #for loop will not be executed for remaining occurances for that staff it.
            if forStaffID not in staffIDwithError:

                #Convert DD/MM/YYYY into YYYY_MM_DD format.
                try:
                    date_format = '%d/%m/%Y'
                    if not datetime.datetime.strptime(forWeek,date_format):
                        writeError(forStaffID,f"Payslip Not Generated for week {forWeek}, Reason - Incorrect Date Format in Hours.txt file")
                        continue
                    else:
                        date, month, year = forWeek.split("/")


                except ValueError:
                    # StaffID is not added in staffIDwithError list as
                    #there might be another record for same employee in Hours.txt with correct/required date format.
                    writeError(forStaffID, f"Payslip Not Generated for week {forWeek}, Reason - Incorrect Date Format in Hours.txt file")
                    continue
                except:
                    writeError(forStaffID,f"Payslip Not Generated for week {forWeek}")
                    continue

                formatedDate = "_".join([year, month, date])

                #Below lines will call functions and data will be stored in approriate variables
                #if isStaffIdAvailable(forStaffID):
                if isPresent(forStaffID,allStaffIds):
                    try:
                        surname, firstName, PPSNumber, stdHrs, hrRate, overTimeRate, taxCredit, stdBand = getStaffDetails(forStaffID)
                    except ValueError:
                        writeError(forStaffID,"Payslip Not Generated, Reason - Data is not provided in required format in Employee.txt file")
                        staffIDwithError.append(forStaffID)
                        continue
                    except:
                        writeError(forStaffID,"Payslip Not Generated.")
                        staffIDwithError.append(forStaffID)
                        continue
                    finally:
                        if stdHrs < 0 or hrRate <= 0 or overTimeRate <= 0 or taxCredit < 0:
                            writeError(forStaffID, "Payslip Not Generated, Reason - Incorrect Data in Employees.txt file")
                            staffIDwithError.append(forStaffID)
                            continue
                else:
                    writeError(forStaffID, "Payslip Not Generated, Reason - Details Not Found in Employees.txt file")
                    staffIDwithError.append(forStaffID)
                    continue

                try:
                    stdRate, highRate = getTaxRates()
                except TypeError:
                    writeError("Data Missing in Taxrates.txt file.")
                    break
                except ValueError:
                    writeError("Data in Taxrates.txt file is not in required format.")
                    break
                except:
                    writeError("Error While getting data for Tax Rate.")
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
                    writeError(forStaffID, f"Payslip Not Generated  for week {forWeek}, Reason - Regular Hours greater than Standard Hours or Hours Worked")
                    break
                elif overTimeHrs < 0:
                    writeError(forStaffID,f"Payslip Not Generated  for week {forWeek}, Reason - Negative overtime hours")
                    break

                #Creating payslips
                payslipFolder = f"{payslipPath}/Week_{formatedDate}"
                createFolder(payslipFolder)
                with open(f"{payslipFolder}/{forStaffID}_{formatedDate}.txt", "w") as ps:

                    #Calculations to be used while printing Payslip
                    salFromRegHrs = regHrs*hrRate
                    salFromOvertimeHrs = overTimeHrs * overTimeRate
                    grossPay = salFromRegHrs + salFromOvertimeHrs
                    partOfSalForStdRate = stdBand if (grossPay > stdBand) else grossPay
                    partOfSalForHighRate = 0 if (grossPay <= stdBand) else grossPay - stdBand
                    dedFromStdRate = round(((partOfSalForStdRate * stdRate) / 100),2)
                    dedFromHighRate = 0 if (grossPay <= stdBand) else round(((highRate * partOfSalForHighRate ) / 100),2)
                    totalDeduction = dedFromStdRate + dedFromHighRate
                    netDeduction = totalDeduction - taxCredit if (totalDeduction - taxCredit > 0) else 0
                    netPay = grossPay - netDeduction


                    if partOfSalForStdRate > stdBand or partOfSalForStdRate > grossPay or partOfSalForStdRate <= 0 or partOfSalForStdRate > grossPay:
                        writeError(forStaffID,f"Payslip Not Generated  for week {forWeek}, Reason - Incorrect Standard Band")
                        break
                    elif partOfSalForHighRate < 0 or partOfSalForHighRate > grossPay:
                        writeError(forStaffID,f"Payslip Not Generated  for week {forWeek}, Reason - Incorrect Higher Rate")
                        break
                    elif netDeduction < 0:
                        # it will never be less than 0 as while calculating its value is already being taken care.
                        # However it has been mentioned here just to be on a safer side.
                        writeError(forStaffID, f"Payslip Not Generated  for week {forWeek}, Reason - Negative Net Deduction")
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
                #if data is present then it will add gross pay of current staff to gross pay and count of staff will be increase by 1 for that week
                #if data is not present then it will add a list containing gross pay and initial count as 1 for that week.
                #used sort function as we are using binary search algo.
                #if formatedDate in weekwisePayDict.keys():
                weekwisePayDictToList = list(weekwisePayDict.keys())
                weekwisePayDictToList.sort()
                if isPresent(formatedDate, weekwisePayDictToList):
                    weekwisePayDict[formatedDate][0] += grossPay
                    weekwisePayDict[formatedDate][1] += 1
                else:
                    weekwisePayDict[formatedDate] = [grossPay, 1]

                #it will check if data for that staff is present in staffwisePayDict
                #if it is present then it will append a list for date and gross pay for that week in list of list format.
                #if it is not present then it will add a new item to dictionary with date and gross pay for that week for that staff.
                # used sort function as we are using binary search algo.
                #if forStaffID in staffwisePayDict.keys():
                staffwisePayDictToList = list(staffwisePayDict.keys())
                staffwisePayDictToList.sort()
                if isPresent(forStaffID, staffwisePayDictToList):
                    staffwisePayDict[forStaffID].append([formatedDate,grossPay])
                else:
                    staffwisePayDict[forStaffID] = [[formatedDate, grossPay]]

    #to print weekly average gross pay
    #it will read the data from weekwisePayDict. Items will provide key and value pair for week data and gross salary
    #data[0] is total of gross pay calculated for that staff and data[1] is total number of weeks that employee is worked.
    with open("./Accounts/AvgGrossPay/WeekwiseGrossPayForAllWorkers.txt", "w") as WGP:
        for week, data in weekwisePayDict.items():
            WGP.writelines(f"Weekly Average Gross Pay of all workers for week {week} is {round((data[0]/data[1]),2)}\n")



    #to print rolling avg Staff wise Gross pay for staff who are working for more than 6 weeks in a company.
    #len(payDetailsForStaff) >= 6 is used to check if we have data for more than or equal to 6 weeks for that staff.
    #payDetailsForStaff.sort() will sort the data as week need to consider only 6 recent weeks for calculating rolling avg
    #payDetailsForStaff[-6] will consider only last 6 weeks data.
    #weekInLastSixWeeks >= previousDate is used to compare if date is within last 6 weeks.
    with open(f"{avgGrossPaypath}/StaffwiseGrossPay.txt", "w") as SGP:
        for staffID, payDetailsForStaff in staffwisePayDict.items():
            if len(payDetailsForStaff) >= 6:
                payDetailsForStaff.sort()
                payForLastSixMonth = 0
                for weekInLastSixWeeks, payInlastSixWeeks in payDetailsForStaff[-6:]:
                    if weekInLastSixWeeks >= previousDate:
                        payForLastSixMonth += payInlastSixWeeks
                SGP.writelines(f"Six-week rolling Average gross pay for Employee {staffID} is {round((payForLastSixMonth / 6),2)}\n")

    #Will be executed if no errors found while creating payslips.
    #it will first read the data in file and then it will write hence 'r+' is used.
    with open(f"{errorPath}/Errors_{currentDate}.txt","r+") as err:
        text = err.read()
        if text == "":
            err.writelines("No Errors Found !")

    print("Payslips are stored in folder 'Accounts/Payslips_YYYY_MM_DD/Payslips'\n"
          "Average Gross Pay Data is stored in folder 'Accounts/AvgGrossPay'\n"
          "Please check 'Error_YYYY_MM_DD.txt' file in 'Accounts/Error' folder for errors(if any).\n"
          "Thank you ! ")
else:
    print("Required files are not available. Please check 'Accounts/Error' folder for more details.")
