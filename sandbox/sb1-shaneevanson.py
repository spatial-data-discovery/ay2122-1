def floatinator(prompt):
    while True:
        print(prompt)
        userInput = input(" > ")
        try:
            return float(userInput)
        except:
            print("||ERROR|| Input not a valid float!\n")

print("""
*************************************
ADDITION-INATOR 9000
This script lets you... add numbers!
*************************************
"""
)

a = floatinator("Input the first number below:")
b = floatinator("Input the second number now:")

print("And the sum of " + str(a) + " and " + str(b) + " is...")
print(str(a+b) + "!!!!! Holy cow!")

input("Press ENTER to exit the program.")



