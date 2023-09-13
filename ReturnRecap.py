# 한줄 주석
"""
두줄
주석
"""

myName = "nico"
my_age = 12
my_color_eyes = "brown"

# todo
print(f"Hello I'm {myName}, I have {my_age} years in the earth, {my_color_eyes} is my eye color")

def add_juice(fruit):
 return f"{fruit}+🥛"
def add_ice(juice):
 return f"{juice}+🧊"
def add_sugar(juice):
 return f"{juice}+🍬"

juice = add_juice("🍊")
ice_juice = add_ice(juice)
perfect_juice = add_sugar(ice_juice)

print(perfect_juice)