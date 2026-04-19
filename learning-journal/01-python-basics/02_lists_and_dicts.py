# nums =[1,2,3,4]
# print("1111:", 1111 + nums[0])
# nums.append(34)
# print("2222:", nums)

# nums.pop()
# print("3333:", nums)

# nums.append("shubham garg is the best")
# print("4444:", nums[0])

employees = {
    "shubham": {"name": "shubham", "sal": 1000},
    "rahul": {"name": "rahul", "sal": 2000},
    "priya": {"name": "priya", "sal": 3000},
}

# print(sal[0])
# del sal[2]
# print(sal[0]["name"])

# search = "shubham"
# for items in sal:
#     if items["name"] == search:
#         print(items)

# for items in sal:
#     for key in items.keys():
#         print(key)

for key, value in employees.items():
    print(value["name"])


# l =[]
# for i in range(0,5):
#     l.append(i)
# print(l)