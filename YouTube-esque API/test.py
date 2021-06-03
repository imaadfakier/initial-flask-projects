import requests

BASE = "http://127.0.0.1:5000/"

# PUT request
# response = requests.put(BASE + "video/1", {"likes":10})
# response = requests.put(BASE + "video/1", {"name":"Imaad Fakier", "views":1000000000000, "likes":10})
# print(response.json())

# input()

# GET request
# response = requests.get(BASE + "video/6")
# print(response.json())

# data = [{"name":"Joe Davis", "views":1000, "likes":150},
# 		{"name":"Michael Douglas", "views":500, "likes":99},
# 		{"name":"Michelle Obama", "views":8000000, "likes":10000}]

# PUT
# for i in range(len(data)):
# 	response = requests.put(BASE + "video/" + str(i), data[i])
# 	print(response.json())
# response = requests.patch(BASE + "video/2", {"views":990})
# response = requests.patch(BASE + "video/2", {"views":99, "likes":10146})
# response = requests.patch(BASE + "video/2", {})
# print(response.json())

# input()

# DELETE
response = requests.delete(BASE + "video/1")
# print(response.json())
print(response)

# input()

# GET
# response = requests.get(BASE + "video/2")
# response = requests.get(BASE + "video/6")
# print(response.json())