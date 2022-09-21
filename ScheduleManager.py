import random

class Proctors:

    def __init__(self, name):
        self.name = name
        self.workSchedule = [["Monday"], ["Tuesday"], ["Wednesday"], ["Thursday"], ["Friday"]]
        self.currentHours = 0
        self.totalHours = 20

    def classScheduleSetter(self, proctorClassSchedule):
        self.mondaySchedule = proctorClassSchedule[0]
        self.tuesdaySchedule = proctorClassSchedule[1]
        self.wednesdaySchedule = proctorClassSchedule[2]
        self.thursdaySchedule = proctorClassSchedule[3]
        self.fridaySchedule = proctorClassSchedule[4]

    def setWorkSchedule(self, name, startTime, endTime, day):
        #when day = 0, it goes to monday, day = 1 goes to tuesday, and so on...
        self.workSchedule[day].append([name, startTime, endTime])

    def setPreferredHours(self, preferredHours):
        self.preferredHours = preferredHours

    def addHours(self, name, time, hours, startTime = False):
        availableHours = name.totalHours - name.currentHours
        if availableHours == 0:
            print(f"{name.name} has no available hours left.")
            return 0
        elif availableHours >= hours:
            name.currentHours += hours
            print(f"{name.name} now has {name.currentHours} working hours.")
            #If updating endTime, need to submit startTime as "time", and vice versa
            if startTime == False:
                return time + hours
            else:
                return time
        elif availableHours < hours:
            print(f"{hours} hours exceed remaining {availableHours} available hours.")
            name.currentHours += availableHours
            print(f"{name.name} now has {name.currentHours} working hours.")
            return time + availableHours

    #Converts time from string to float, for easy time calculations
    def timeConverter(self, proctorClassSchedule):
        timeSlot = []
        for x in range(len(proctorClassSchedule)):
            for y in range(len(proctorClassSchedule[x])):
                str = proctorClassSchedule[x][y]
                if str.lower() == "none" or str.lower() == "n":
                    break
                str = str.replace(":", "")
                str = str.replace("-", " ")
                str = str.replace(":", "")
                while str.__contains__("am"):
                    str = str.replace("am", "")
                while str.__contains__("pm"):
                    str = str.replace("pm", "")

                for i in range(len(str)):
                    if str[i] == " ":
                        firstString = str[0:i]
                        secondString = str[i + 1:len(str)]

                #Finally translate the times over
                firstTime = 0.0
                if len(firstString) == 3:
                    firstTime += float(firstString[0:1])
                    firstTime += (float(firstString[1:3]) / 60)
                elif len(firstString) == 4:
                    firstTime += float(firstString[0:2])
                    firstTime += (float(firstString[2:4]) / 60)

                secondTime = 0.0
                if len(secondString) == 3:
                    secondTime += float(secondString[0:1])
                    secondTime += (float(secondString[1:3]) / 60)
                elif len(secondString) == 4:
                    secondTime += float(secondString[0:2])
                    secondTime += (float(secondString[2:4]) / 60)

                timeSlot.append([firstTime, secondTime])

            if x == 0:  # We are in monday
                self.convertedMondaySchedule = timeSlot
            elif x == 1:  # We are in tuesday
                self.convertedTuesdaySchedule = timeSlot
            elif x == 2:  # We are in wednesday
                self.convertedWednesdaySchedule = timeSlot
            elif x == 3:  # We are in thursday
                self.convertedThursdaySchedule = timeSlot
            elif x == 4:  # We are in friday
                self.convertedFridaySchedule = timeSlot

            timeSlot = []

    # Converts time from float to string, used to display in end result
    def reverseTimeConverter(self, time, amOrPm):
        hour = int(time)
        minutes = int((time - int(time)) * 60)
        if minutes == 0:
            return f"{hour}:{minutes}{minutes}{amOrPm}"
        else:
            return f"{hour}:{minutes}{amOrPm}"

    def priorityHoursPreferences(self, proctors):
        morningPreference = []
        afternoonPreference = []
        noonPreference = []
        nonePreference = []

        for i in proctors:
            if i.preferredHours == "morning":
                morningPreference.append(i)
            elif i.preferredHours == "noon":
                noonPreference.append(i)
            elif i.preferredHours == "afternoon":
                afternoonPreference.append(i)
            elif i.preferredHours == "none":
                nonePreference.append(i)

        self.morningPreference = morningPreference
        self.noonPreference = noonPreference
        self.afternoonPreference = afternoonPreference
        self.nonePreference = nonePreference

    #Decide who gets first dibs on morning priority hours
    def morningHoursSetter(self):
        lst = []
        randLst = []
        for i in range(1, len(self.morningPreference) + 1):
            randLst.append(i)
        random.shuffle(randLst)

        #Assign random numbers to proctors
        if len(self.morningPreference) > 0:
            for x in range(len(self.morningPreference)):
                lst.append([self.morningPreference[x], randLst[x]])

        #Sort using numbers with greatest numbers coming first
        sortedLst = []
        nextHighest = len(lst)
        for x in range(len(lst)):
            for y in range(len(lst)):
                if lst[y][1] == nextHighest:
                    sortedLst.append(lst[y])
                    nextHighest -= 1

        #Setting priority hours for monday morning
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].mondaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedMondaySchedule) == 0:
                    self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 0)
                    set = True
                    break

                str = sortedLst[x][0].mondaySchedule[y][0:7]
                num = sortedLst[x][0].convertedMondaySchedule[y][0]
                if str.__contains__("12:") and str.__contains__("pm"):
                    if  num - 0.5 >= 12:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 0)
                        set = True
                        break
                    elif num - 0.5 < 12 and num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 0)
                        set = True
                        break
                elif str.__contains__("pm"):
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 0)
                        set = True
                        break
                elif str.__contains__("am"):
                    if num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 0)
                        set = True
                        break
                    else:
                        pass
            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        #Setting priority hours for tuesday morning
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].tuesdaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedTuesdaySchedule) == 0:
                    self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 1)
                    set = True
                    break

                str = sortedLst[x][0].tuesdaySchedule[y][0:7]
                num = sortedLst[x][0].convertedTuesdaySchedule[y][0]
                if str.__contains__("12:") and str.__contains__("pm"):
                    if  num - 0.5 >= 12:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 1)
                        set = True
                        break
                    elif num - 0.5 < 12 and num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 1)
                        set = True
                        break
                elif str.__contains__("pm"):
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 1)
                        set = True
                        break
                elif str.__contains__("am"):
                    if num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 1)
                        set = True
                        break
                    else:
                        pass
            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        #Setting priority hours for wednesday morning
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].wednesdaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedWednesdaySchedule) == 0:
                    self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 2)
                    set = True
                    break

                str = sortedLst[x][0].wednesdaySchedule[y][0:7]
                num = sortedLst[x][0].convertedWednesdaySchedule[y][0]
                if str.__contains__("12:") and str.__contains__("pm"):
                    if  num - 0.5 >= 12:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 2)
                        set = True
                        break
                    elif num - 0.5 < 12 and num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 2)
                        set = True
                        break
                elif str.__contains__("pm"):
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 2)
                        set = True
                        break
                elif str.__contains__("am"):
                    if num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 2)
                        set = True
                        break
                    else:
                        pass
            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        #Setting priority hours for thursday morning
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].thursdaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedThursdaySchedule) == 0:
                    self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 3)
                    set = True
                    break

                str = sortedLst[x][0].thursdaySchedule[y][0:7]
                num = sortedLst[x][0].convertedThursdaySchedule[y][0]
                if str.__contains__("12:") and str.__contains__("pm"):
                    if  num - 0.5 >= 12:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 3)
                        set = True
                        break
                    elif num - 0.5 < 12 and num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 3)
                        set = True
                        break
                elif str.__contains__("pm"):
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 3)
                        set = True
                        break
                elif str.__contains__("am"):
                    if num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 3)
                        set = True
                        break
                    else:
                        pass
            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        #Setting priority hours for friday morning
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].fridaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedFridaySchedule) == 0:
                    self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 4)
                    set = True
                    break

                str = sortedLst[x][0].fridaySchedule[y][0:7]
                num = sortedLst[x][0].convertedFridaySchedule[y][0]
                if str.__contains__("12:") and str.__contains__("pm"):
                    if  num - 0.5 >= 12:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 4)
                        set = True
                        break
                    elif num - 0.5 < 12 and num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 4)
                        set = True
                        break
                elif str.__contains__("pm"):
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8.0, 4), "pm"), 4)
                        set = True
                        break
                elif str.__contains__("am"):
                    if num - 0.5 >= 9.5:
                        self.setWorkSchedule(name.name, "8:00am", self.reverseTimeConverter(self.addHours(name, 8, (num - 0.5) - 8), "am"), 4)
                        set = True
                        break
                    else:
                        pass
            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

    # Decide who gets first dibs on noon hours
    def noonHoursSetter(self):
        lst = []
        randLst = []
        for i in range(1, len(self.noonPreference) + 1):
            randLst.append(i)
        random.shuffle(randLst)

        #Assign random numbers to proctors
        if len(self.noonPreference) > 0:
            for x in range(len(self.noonPreference)):
                lst.append([self.noonPreference[x], randLst[x]])

        #Sort using numbers with greatest numbers coming first
        sortedLst = []
        nextHighest = len(lst)
        for x in range(len(lst)):
            for y in range(len(lst)):
                if lst[y][1] == nextHighest:
                    sortedLst.append(lst[y])
                    nextHighest -= 1

        # Setting priority hours for Monday noon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].mondaySchedule)):
                set = False
                name = sortedLst[x][0]
                if len(name.convertedMondaySchedule) == 0:
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 0)
                    set = True
                    break

                str1 = sortedLst[x][0].mondaySchedule[y][0:7]
                str2 = sortedLst[x][0].mondaySchedule[y][8:len(sortedLst[x][0].mondaySchedule[y])]
                num1 = sortedLst[x][0].convertedMondaySchedule[y][0]
                num2 = sortedLst[x][0].convertedMondaySchedule[y][1]

                if str1.__contains__("am") and str2.__contains__("am"):
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 0)
                    set = True
                    break
                if str1.__contains__("am") and str2.__contains__("pm"):
                    if int(num2) == 12:
                        endClassTime = num2 - int(num2)
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 0)
                        set = True
                        break
                    elif int(num2) >= 1:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 0)
                        set = True
                        break
                #Past this point, lots of issues, but easy fix
                if str1.__contains__("pm") and str2.__contains__("pm"):
                    if int(num1) == 12 and num2 + 0.5 <= 6:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 0)
                        set = True
                        break
                    #A bit buggy when multiple hours are entered within this time frame
                    elif num1 - 1.5 >= 0 and num2 + 1.5 <= 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 0)
                        addHours = self.addHours(name, num2 + 0.5, 6 - (num2 + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 0)
                        set = True
                        break
                    elif num1 - 1.5 >= 0 and int(num2) == 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 0)
                        set = True
                        break
                    elif num1 - 0.5 >= 6:
                        addHours = self.addHours(name, 0, 6)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 0)
                        set = True
                        break
                    elif num1 == 6:
                        addHours = self.addHours(name, 0, 5.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 0)
                        set = True
                        break
                    else:
                        pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Tuesday noon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].tuesdaySchedule)):
                set = False
                name = sortedLst[x][0]
                if len(name.convertedTuesdaySchedule) == 0:
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 1)
                    set = True
                    break

                str1 = sortedLst[x][0].tuesdaySchedule[y][0:7]
                str2 = sortedLst[x][0].tuesdaySchedule[y][8:len(sortedLst[x][0].tuesdaySchedule[y])]
                num1 = sortedLst[x][0].convertedTuesdaySchedule[y][0]
                num2 = sortedLst[x][0].convertedTuesdaySchedule[y][1]

                if str1.__contains__("am") and str2.__contains__("am"):
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 1)
                    set = True
                    break
                if str1.__contains__("am") and str2.__contains__("pm"):
                    if int(num2) == 12:
                        endClassTime = num2 - int(num2)
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 1)
                        set = True
                        break
                    elif int(num2) >= 1:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 1)
                        set = True
                        break
                if str1.__contains__("pm") and str2.__contains__("pm"):
                    if int(num1) == 12 and num2 + 0.5 <= 6:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 1)
                        set = True
                        break
                    # A bit buggy when multiple hours are entered
                    elif num1 - 1.5 >= 0 and num2 + 1.5 <= 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 1)
                        addHours = self.addHours(name, num2 + 0.5, 6 - (num2 + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 1)
                        set = True
                        break
                    elif num1 - 1.5 >= 0 and int(num2) == 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 1)
                        set = True
                        break
                    elif num1 - 0.5 >= 6:
                        addHours = self.addHours(name, 0, 6)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 1)
                        set = True
                        break
                    elif num1 == 6:
                        addHours = self.addHours(name, 0, 5.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 1)
                        set = True
                        break
                    else:
                        pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Wednesday noon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].wednesdaySchedule)):
                set = False
                name = sortedLst[x][0]
                if len(name.convertedWednesdaySchedule) == 0:
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 2)
                    set = True
                    break

                str1 = sortedLst[x][0].wednesdaySchedule[y][0:7]
                str2 = sortedLst[x][0].wednesdaySchedule[y][8:len(sortedLst[x][0].wednesdaySchedule[y])]
                num1 = sortedLst[x][0].convertedWednesdaySchedule[y][0]
                num2 = sortedLst[x][0].convertedWednesdaySchedule[y][1]

                if str1.__contains__("am") and str2.__contains__("am"):
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 2)
                    set = True
                    break
                if str1.__contains__("am") and str2.__contains__("pm"):
                    if int(num2) == 12:
                        endClassTime = num2 - int(num2)
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 2)
                        set = True
                        break
                    elif int(num2) >= 1:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 2)
                        set = True
                        break
                if str1.__contains__("pm") and str2.__contains__("pm"):
                    if int(num1) == 12 and num2 + 0.5 <= 6:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 2)
                        set = True
                        break
                    # A bit buggy when multiple hours are entered
                    elif num1 - 1.5 >= 0 and num2 + 1.5 <= 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 2)
                        addHours = self.addHours(name, num2 + 0.5, 6 - (num2 + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 2)
                        set = True
                        break
                    elif num1 - 1.5 >= 0 and int(num2) == 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 2)
                        set = True
                        break
                    elif num1 - 0.5 >= 6:
                        addHours = self.addHours(name, 0, 6)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 2)
                        set = True
                        break
                    elif num1 == 6:
                        addHours = self.addHours(name, 0, 5.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 2)
                        set = True
                        break
                    else:
                        pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Thursday noon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].thursdaySchedule)):
                set = False
                name = sortedLst[x][0]
                if len(name.convertedThursdaySchedule) == 0:
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 3)
                    set = True
                    break

                str1 = sortedLst[x][0].thursdaySchedule[y][0:7]
                str2 = sortedLst[x][0].thursdaySchedule[y][8:len(sortedLst[x][0].thursdaySchedule[y])]
                num1 = sortedLst[x][0].convertedThursdaySchedule[y][0]
                num2 = sortedLst[x][0].convertedThursdaySchedule[y][1]

                if str1.__contains__("am") and str2.__contains__("am"):
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 3)
                    set = True
                    break
                if str1.__contains__("am") and str2.__contains__("pm"):
                    if int(num2) == 12:
                        endClassTime = num2 - int(num2)
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 3)
                        set = True
                        break
                    elif int(num2) >= 1:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 3)
                        set = True
                        break
                if str1.__contains__("pm") and str2.__contains__("pm"):
                    if int(num1) == 12 and num2 + 0.5 <= 6:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 3)
                        set = True
                        break
                    # A bit buggy when multiple hours are entered
                    elif num1 - 1.5 >= 0 and num2 + 1.5 <= 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 3)
                        addHours = self.addHours(name, num2 + 0.5, 6 - (num2 + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 3)
                        set = True
                        break
                    elif num1 - 1.5 >= 0 and int(num2) == 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 3)
                        set = True
                        break
                    elif num1 - 0.5 >= 6:
                        addHours = self.addHours(name, 0, 6)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 3)
                        set = True
                        break
                    elif num1 == 6:
                        addHours = self.addHours(name, 0, 5.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 3)
                        set = True
                        break
                    else:
                        pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Friday noon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].fridaySchedule)):
                set = False
                name = sortedLst[x][0]
                if len(name.convertedFridaySchedule) == 0:
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 4)
                    set = True
                    break

                str1 = sortedLst[x][0].fridaySchedule[y][0:7]
                str2 = sortedLst[x][0].fridaySchedule[y][8:len(sortedLst[x][0].fridaySchedule[y])]
                num1 = sortedLst[x][0].convertedFridaySchedule[y][0]
                num2 = sortedLst[x][0].convertedFridaySchedule[y][1]

                if str1.__contains__("am") and str2.__contains__("am"):
                    addHours = self.addHours(name, 0, 6)
                    if addHours == 0:
                        break
                    self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 4)
                    set = True
                    break
                if str1.__contains__("am") and str2.__contains__("pm"):
                    if int(num2) == 12:
                        endClassTime = num2 - int(num2)
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 4)
                        set = True
                        break
                    elif int(num2) >= 1:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 4)
                        set = True
                        break
                if str1.__contains__("pm") and str2.__contains__("pm"):
                    if int(num1) == 12 and num2 + 0.5 <= 6:
                        endClassTime = num2
                        addHours = self.addHours(name, endClassTime + 0.5, 6 - (endClassTime + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 4)
                        set = True
                        break
                    # A bit buggy when multiple hours are entered
                    elif num1 - 1.5 >= 0 and num2 + 1.5 <= 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 4)
                        addHours = self.addHours(name, num2 + 0.5, 6 - (num2 + 0.5), True)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, self.reverseTimeConverter(addHours, "pm"), "6:00pm", 4)
                        set = True
                        break
                    elif num1 - 1.5 >= 0 and int(num2) == 6:
                        addHours = self.addHours(name, 0, num1 - 0.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 4)
                        set = True
                        break
                    elif num1 - 0.5 >= 6:
                        addHours = self.addHours(name, 0, 6)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 4)
                        set = True
                        break
                    elif num1 == 6:
                        addHours = self.addHours(name, 0, 5.5)
                        if addHours == 0:
                            break
                        self.setWorkSchedule(name.name, "12:00pm", self.reverseTimeConverter(addHours, "pm"), 4)
                        set = True
                        break
                    else:
                        pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

    # Decide who gets first dibs on afternoon priority hours
    def afternoonHoursSetter(self):
        lst = []
        randLst = []
        for i in range(1, len(self.afternoonPreference) + 1):
            randLst.append(i)
        random.shuffle(randLst)

        #Assign random numbers to proctors
        if len(self.afternoonPreference) > 0:
            for x in range(len(self.afternoonPreference)):
                lst.append([self.afternoonPreference[x], randLst[x]])

        #Sort using numbers with greatest numbers coming first
        sortedLst = []
        nextHighest = len(lst)
        for x in range(len(lst)):
            for y in range(len(lst)):
                if lst[y][1] == nextHighest:
                    sortedLst.append(lst[y])
                    nextHighest -= 1

        # Setting priority hours for Monday afternoon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].mondaySchedule)):
                set = False
                name = sortedLst[x][0]
                if len(name.convertedMondaySchedule) == 0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 0)
                    set = True
                    break

                str = sortedLst[x][0].mondaySchedule[y][7:len(sortedLst[x][0].mondaySchedule[y])]
                num = sortedLst[x][0].convertedMondaySchedule[y][1]
                if str.__contains__("12:"):
                    minutes = num - 12
                    endTime = minutes
                    if endTime + 0.5 <= 6.0:
                        self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 0)
                        set = True
                        break
                    elif endTime + 0.5 > 6.0:
                        pass
                elif num + 0.5 <= 6.0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 0)
                    set = True
                    break
                elif num + 0.5 > 6.0:
                    pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Tuesday afternoon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].tuesdaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedTuesdaySchedule) == 0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 1)
                    set = True
                    break

                str = sortedLst[x][0].tuesdaySchedule[y][7:len(sortedLst[x][0].tuesdaySchedule[y])]
                num = sortedLst[x][0].convertedTuesdaySchedule[y][1]

                if str.__contains__("12:"):
                    minutes = num - 12
                    endTime = minutes
                    if endTime + 0.5 <= 6.0:
                        self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 1)
                        set = True
                        break
                    elif endTime + 0.5 > 6.0:
                        pass
                elif num + 0.5 <= 6.0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 1)
                    set = True
                    break
                elif num + 0.5 > 6.0:
                    pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Wednesday afternoon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].wednesdaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedWednesdaySchedule) == 0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 2)
                    set = True
                    break

                str = sortedLst[x][0].wednesdaySchedule[y][7:len(sortedLst[x][0].wednesdaySchedule[y])]
                num = sortedLst[x][0].convertedWednesdaySchedule[y][1]

                if str.__contains__("12:"):
                    minutes = num - 12
                    endTime = minutes
                    if endTime + 0.5 <= 6.0:
                        self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 2)
                        set = True
                        break
                    elif endTime + 0.5 > 6.0:
                        pass
                elif num + 0.5 <= 6.0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 2)
                    set = True
                    break
                elif num + 0.5 > 6.0:
                    pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Thursday afternoon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].mondaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedThursdaySchedule) == 0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 3)
                    set = True
                    break

                str = sortedLst[x][0].thursdaySchedule[y][7:len(sortedLst[x][0].thursdaySchedule[y])]
                num = sortedLst[x][0].convertedThursdaySchedule[y][1]

                if str.__contains__("12:"):
                    minutes = num - 12
                    endTime = minutes
                    if endTime + 0.5 <= 6.0:
                        self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 3)
                        set = True
                        break
                    elif endTime + 0.5 > 6.0:
                        pass
                elif num + 0.5 <= 6.0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 3)
                    set = True
                    break
                elif num + 0.5 > 6.0:
                    pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

        # Setting priority hours for Friday afternoon
        for x in range(len(sortedLst)):
            for y in range(len(sortedLst[x][0].fridaySchedule)):
                set = False
                name = sortedLst[x][0]

                if len(name.convertedFridaySchedule) == 0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 4)
                    set = True
                    break

                str = sortedLst[x][0].fridaySchedule[y][7:len(sortedLst[x][0].fridaySchedule[y])]
                num = sortedLst[x][0].convertedFridaySchedule[y][1]

                if str.__contains__("12:"):
                    minutes = num - 12
                    endTime = minutes
                    if endTime + 0.5 <= 6.0:
                        self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 4)
                        set = True
                        break
                    elif endTime + 0.5 > 6.0:
                        pass
                elif num + 0.5 <= 6.0:
                    self.setWorkSchedule(name.name, "6:00pm", self.reverseTimeConverter(self.addHours(name, 6.0, 4), "pm"), 4)
                    set = True
                    break
                elif num + 0.5 > 6.0:
                    pass

            if set == True:
                sortedLst.append(sortedLst.pop(0))
                break

    def remainingHoursSetter(self, proctors):
        lst = []
        hoursLst = []
        for i in proctors:
            if i.currentHours < 20:
                lst.append([i, i.currentHours])

        print(f"List of proctors with hours remaining: {lst}")

        #sorts proctors based on current hours to give those with less priority
        sortedLst = []
        for x in range(len(lst)):
            for y in range(len(lst)):
                if lst[x][1] < lst[y][1]:
                    lst.insert(y + 1, lst.pop(lst[x]))
                    break

        print(f"List of sorted proctors: {sortedLst}")

    def __str__(self):
        day = 0
        for dayOfWeek in range(0, 5):
            print(f"{self.workSchedule[dayOfWeek][day]}:", end="")
            for timeSlot in range(1, len(self.workSchedule[dayOfWeek])):
                print(
                    f" {self.workSchedule[dayOfWeek][timeSlot][0]} - ({self.workSchedule[dayOfWeek][timeSlot][1]}-{self.workSchedule[dayOfWeek][timeSlot][2]}) ",
                    end="//")
            print()