import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap




fig = plt.figure(1)
ax = fig.add_subplot(121)
x = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 2, 1, 1], [0, 0, 0, 0, 0, 1], [0, 1, 1, 1, 1, 1]]
cax = ax.matshow(x, cmap=plt.cm.gray_r)
bx = fig.add_subplot(122)
cmap = ListedColormap(['w', 'b', 'r'])
cat = bx.matshow(x, cmap=cmap)
plt.show()



