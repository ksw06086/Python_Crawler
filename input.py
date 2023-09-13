# answer : type - str
answer = input("why Number? ") 
print(f"im {answer}")

# answer : type = int
answer = int(answer)
print(type(answer))

# and, or
if answer < 18:
    print(answer, "is younger")
elif answer > 18 and answer < 23:
    print(answer, "bigger")
elif answer > 99 or answer < 103:
    print(answer, "or")
else:
    print("dsfhsdjkhfsdjf")