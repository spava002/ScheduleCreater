from Proctors import Proctors


def scheduleChecker(scheduleInput):
    for x in scheduleInput:
        digitCounter = 0
        colonCounter = 0
        timeCounter = 0
        dashCounter = 0
        if x.lower() == "none" or x.lower() == "n":
            return True
        elif len(x) < 13 or len(x) > 15:
            return False
        for i in range(2):
            if len(x) == 13:
                if (x[4:6].lower() == "am" or x[4:6].lower() == "pm") and (
                        x[11:13].lower() == "am" or x[11:13].lower() == "pm"):
                    timeCounter += 1
                for y in x:
                    if y.isdigit():
                        digitCounter += 1
                    elif y == ":":
                        colonCounter += 1
                    elif y == "-":
                        dashCounter += 1
                if digitCounter == 6 and colonCounter == 2 and dashCounter == 1 and timeCounter == 1:
                    return True
                else:
                    return False
            elif len(x) == 14:
                if x[1].isdigit():
                    if (x[5:7].lower() == "am" or x[5:7].lower() == "pm") and (
                            x[12:14].lower() == "am" or x[12:14].lower() == "pm"):
                        timeCounter += 1
                elif not x[1].isdigit():
                    if (x[4:6].lower() == "am" or x[4:6].lower() == "pm") and (
                            x[12:14].lower() == "am" or x[12:14].lower() == "pm"):
                        timeCounter += 1
                for y in x:
                    if y.isdigit():
                        digitCounter += 1
                    elif y == ":":
                        colonCounter += 1
                    elif y == "-":
                        dashCounter += 1
                if digitCounter == 7 and colonCounter == 2 and dashCounter == 1 and timeCounter == 1:
                    return True
                else:
                    return False
            elif len(x) == 15:
                if (x[5:7].lower() == "am" or x[5:7].lower() == "pm") and (
                        x[13:15].lower() == "am" or x[13:15].lower() == "pm"):
                    timeCounter += 1
                for y in x:
                    if y.isdigit():
                        digitCounter += 1
                    elif y == ":":
                        colonCounter += 1
                    elif y == "-":
                        dashCounter += 1
                if digitCounter == 8 and colonCounter == 2 and dashCounter == 1 and timeCounter == 1:
                    return True
                else:
                    return False


def preferenceChecker(preference, key):
    for i in key:
        if preference == i:
            return True
    return False


while True:
    try:
        totalProctors = int(input("Input number of proctors working this semester: "))
        break
    except ValueError:
        print("Invalid input. Try again.")

proctors = []
for i in range(1, totalProctors + 1):
    if i == 1:
        name = input(f"Input name of the {i}st proctor: ")
        proctors.append(Proctors(name))
    elif i == 2:
        name = input(f"Input name of the {i}nd proctor: ")
        proctors.append(Proctors(name))
    elif i == 3:
        name = input(f"Input name of the {i}rd proctor: ")
        proctors.append(Proctors(name))
    else:
        name = input(f"Input name of the {i}th proctor: ")
        proctors.append(Proctors(name))
        break

print()
proctorClassSchedule = []
print("Format for inputting schedule: (ex. 6:15pm-9:30pm). If none, enter 'None'.")
for i in proctors:
    print()
    monday = input(f"Enter {i.name}'s Monday schedule: ").split()
    while not scheduleChecker(monday):
        monday = input(f"Invalid input. Enter {i.name}'s Monday schedule: ").split()
    proctorClassSchedule.append(monday)

    tuesday = input(f"Enter {i.name}'s Tuesday schedule: ").split()
    while not scheduleChecker(tuesday):
        tuesday = input(f"Invalid input. Enter {i.name}'s Tuesday schedule: ").split()
    proctorClassSchedule.append(tuesday)

    wednesday = input(f"Enter {i.name}'s Wednesday schedule: ").split()
    while not scheduleChecker(wednesday):
        wednesday = input(f"Invalid input. Enter {i.name}'s Wednesday schedule: ").split()
    proctorClassSchedule.append(wednesday)

    thursday = input(f"Enter {i.name}'s Thursday schedule: ").split()
    while not scheduleChecker(thursday):
        thursday = input(f"Invalid input. Enter {i.name}'s Thursday schedule: ").split()
    proctorClassSchedule.append(thursday)

    friday = input(f"Enter {i.name}'s Friday schedule: ").split()
    while not scheduleChecker(friday):
        friday = input(f"Invalid input. Enter {i.name}'s Friday schedule: ").split()
    proctorClassSchedule.append(friday)

    i.classScheduleSetter(proctorClassSchedule)
    i.timeConverter(proctorClassSchedule)
    proctorClassSchedule = []

    print()
    key = ['morning', 'noon', 'afternoon', 'none']
    preference = input(
        f"Does {i.name} have a preference in work hours: (Ex. 'morning', 'noon', 'afternoon', or 'none'): ").lower()
    preferenceChecker(preference, key)
    while not preferenceChecker(preference, key):
        preference = input("I didn't understand your input. Input 'morning', 'noon', 'afternoon', or 'none': ")
    i.setPreferredHours(preference)

print()

proctorsManager = Proctors("No Name")
proctorsManager.priorityHoursPreferences(proctors)
proctorsManager.morningHoursSetter()
proctorsManager.noonHoursSetter()
proctorsManager.afternoonHoursSetter()

workSchedule = proctorsManager.workSchedule

for i in range(len(proctorsManager.morningPreference)):
    print("Morning: " + proctorsManager.morningPreference[i].name + " ", end="")
print()
for i in range(len(proctorsManager.noonPreference)):
    print("Noon: " + proctorsManager.noonPreference[i].name + " ", end="")
print()
for i in range(len(proctorsManager.afternoonPreference)):
    print("Afternoon: " + proctorsManager.afternoonPreference[i].name + " ", end="")
print()
for i in range(len(proctorsManager.nonePreference)):
    print("None: " + proctorsManager.nonePreference[i].name + " ", end="")

# proctorsManager.remainingHoursSetter(proctors)

print()
print(workSchedule)
print()

# Print out the final schedule
proctorsManager.__str__()
