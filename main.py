import sqlite3

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi

def calculate_bmr(weight, height, age, sex):
    if sex == "male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    return bmr


def calculate_blood_pressure(systolic, diastolic):
    if systolic < 120 and diastolic < 80:
        return "Normal"
    elif systolic < 130 and diastolic < 80:
        return "High Blood Pressure - Stage 1"
    else:
        return "High Blood Pressure - Stage 2"


def calculate_heart_rate(age):
    max_heart_rate = 220 - age
    lower_limit = max_heart_rate * 0.50
    upper_limit = max_heart_rate * 0.85
    return max_heart_rate, lower_limit, upper_limit


def calculate_whr(waist, hip):
    whr = waist / hip
    return whr

connection = sqlite3.connect("medical_data.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT,
age INTEGER,
weight REAL,
height REAL,
bmi REAL,
bmr REAL,
systolic REAL,
diastolic REAL,
heart_rate REAL,
waist REAL,
hip REAL,
whr REAL
)
""")
connection.commit()

print()
print("NOTE: This calculator is for educational purposes only.")
print("The results are estimates and should not be used as a medical diagnosis.")
print()


while True:
    print()
    print("=============================")
    print("   Medical Data Calculator")
    print("==============================")
    print("   Health & Wellness Tools")
    print("==============================")
    print("1. Calculate BMI")
    print("2. Calculate BMR")
    print("3. Calculate Blood Pressure")
    print("4. Calculate Heart Rate")
    print("5. Calculate Waist-to-Hip Ratio")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        try:
            weight = float(input("Enter your weight in kg: "))
            height = float(input("Enter your height in meters: "))
            if weight <= 0 or height <=0:
                print("Weight and height must be greater than 0.")
                continue

        except ValueError:
            print("Please enter a valid number.")
            continue

        bmi = calculate_bmi(weight, height)
        print("Your BMI is:", round(bmi, 2))

        if bmi < 18.5:
             print("Category: Underweight")
        elif bmi < 25:
             print("Category: Normal weight")
        elif bmi < 30:
             print("Category: Overweight")
        else:
             print("Category: Obesity")

        cursor.execute("""
        INSERT INTO patients (weight, height, bmi)
        VALUES (?, ?, ?)
        """, (weight, height, bmi))

        connection.commit()

        print("BMI result saved to database.")
        print("-------------------------------")

    elif choice == "2":
        try:
           weight = float(input("Enter your weight in kg: "))
           height = float(input("Enter your height in meters: "))
           age = int(input("Enter your age: "))
           if weight <= 0 or height <= 0 or age <= 0:
               print("Weight, height and age must be greater than 0.")
               continue

        except ValueError:
            print("Please enter a valid number.")
            continue
        sex = input("Enter your sex (male/female): ").lower()

        if sex not in ["male", "female"]:
            print("Please enter male or female.")
            continue

        height_cm = height * 100
        bmr = calculate_bmr(weight, height_cm, age, sex)
        print("Your BMR is:", round(bmr, 2), "calories/day")

        cursor.execute("""
        INSERT INTO patients (age, weight, height, bmr)
        VALUES (?,?,?,?)
        """, (age, weight, height_cm, bmr))

        connection.commit()

        print("BMR result saved to database.")
        print("-------------------------------")

    elif choice == "3":
        try:
            systolic = float(input("Enter systolic blood pressure (mmHg): "))
            diastolic = float(input("Enter diastolic blood pressure (mmHg): "))

            if systolic <= 0 or diastolic <= 0:
                print("Blood pressure values must be greater than 0.")
                continue

        except ValueError:
            print("Please enter valid numbers.")
            continue

        category = calculate_blood_pressure(systolic, diastolic)
        print("Blood Pressure Category:", category)

        cursor.execute("""
        INSERT INTO patients (systolic, diastolic)
        VALUES (?,?)
        """, (systolic, diastolic))

        connection.commit()
        print("Blood pressure result saved to database.")
        print("------------------------------------------")

    elif choice == "4":
        try:
            age = int(input("Enter your age: "))
            if age <= 0:
                print("Age must be greater than 0.")
                continue

        except ValueError:
            print("Please enter valid age.")
            continue

        max_heart_rate, lower_limit, upper_limit = calculate_heart_rate(age)

        print("Estimated Maximum Heart Rate:", round(max_heart_rate), "BPM")
        print("Target Heart Rate Range:", round(lower_limit), "-", round(upper_limit), "BPM")

        cursor.execute("""
        INSERT INTO patients (age, heart_rate)
        VALUES(?,?)
        """, (age, max_heart_rate))

        connection.commit()
        print("Heart rate result saved to database.")
        print("--------------------------------------")


    elif choice == "5":
        try:
            waist = float(input("Enter your waist circumference in cm: "))
            hip = float(input("Enter your hip circumference in cm: "))

            if waist <=0 or hip <=0:
                print("Waist and hip measurements must be greater than 0.")
                continue
        except ValueError:
            print("Please enter valid numbers.")
            continue

        whr = calculate_whr(waist, hip)
        print("Your Waist-to-Hip Ratio is:", round(whr, 2))

        cursor.execute("""
        INSERT INTO patients (waist, hip, whr)
        VALUES (?,?,?)
        """, (waist, hip, whr))

        connection.commit()
        print("WHR result saved to database.")
        print("-------------------------------")

    elif choice == "6":
        print("Thank you for using Medical Data Calculator!")
        break

    else:
        print("Invalid choice. Please select 1,2,3,4,5 or 6.")

connection.close()
