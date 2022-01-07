from matplotlib import pyplot as plt

d = {'a': 5, 'b': 2, 'c': 4, 'd': 4, 'e': 3, 'f': 2.5}

keys = [key for key in d]
vals = [y for x, y in d.items()]

# print(keys)
# print(vals)

# print(plt.style.available)
plt.title('Random plot')
# plt.style.use('seaborn')
plt.style.use('tableau-colorblind10')
# plt.style.use('fivethirtyeight')
# plt.xkcd()
# CHART
# plt.plot(keys, vals, color="#444444")
# plt.bar(keys, vals, width=0.6, color="#444444", label="Something")

# plt.legend()
# plt.xticks(ticks=keys)

# plt.xlabel('Letters')
# plt.ylabel('Numbers')
# plt.tight_layout()

# PIE
# plt.setp(vals)
colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']
font = {'family' : 'normal',
    #'weight' : 'bold',
    'size'   : 10}
plt.rc('font', **font)

plt.pie(vals, labels=keys, colors=colors) # textprops=dict(color="b"))

plt.show()