
# importing the required module
import matplotlib.pyplot as plt
 
# x axis values
x = [1,2,3]
# corresponding y axis values
y = [2,4,1]
 
# plotting the points
fig, ax = plt.subplots(figsize =(10, 7))
ax.plot(x, y)
 
# naming the x axis
plt.xlabel('x - axis')
# naming the y axis
plt.ylabel('y - axis')
 
# giving a title to my graph
plt.title('My first graph!')
 
# function to show the plot
# plt.show()
fig.savefig("image.png")


# ax.plot(x=timestamp, y=value, kind="line")
# plt.xlabel('Marks')
# plt.ylabel('Frequency')
# # plt.show()
# fig.savefig('../../static/histogram.png')