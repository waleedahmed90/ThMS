
import matplotlib.pyplot as plt
import numpy as np

k = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
H_FairRecDiv = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
Y = [0.0291, 0.0305, 0.0316, 0.0319, 0.0331, 0.0337, 0.0341, 0.0342, 0.0353, 0.0357, 0.0369, 0.0363, 0.0367, 0.0376, 0.0381, 0.0351, 0.0361, 0.0367, 0.0366, 0.0372]
H_FairRec = [0.4912, 0.3859, 0.35, 0.458, 0.409, 0.34, 0.409, 0.441, 0.351, 0.307, 0.364, 0.344, 0.352, 0.389, 0.367, 0.375, 0.37, 0.396, 0.423, 0.437]

plt.plot(H_FairRec, color = 'black', label = 'H: FairRec')
plt.plot(H_FairRecDiv, color = 'red', label = 'H: FairRecDiv')
plt.plot(Y, color = 'blue', label = 'Y: Mean Average Envy')
plt.title('Frac. of Satisfied Producers(H) & Mean Average Envy (Y) : FairRec vs FairDiv')
plt.xlabel('k: Size of recommendation set')
plt.yticks(np.arange(0, 1.05, 0.05))
plt.plot(k,Y)

plt.xticks(k,k)
plt.ylabel('Fraction of Satisfied Producers')
plt.legend(bbox_to_anchor=(0.86, 1.0, 0.1, 0.1), loc='lower center')
plt.show()


#k#####H_FairRecDiv########H_FairRec######Y_FairDiv###
#1	   	 1.0				0.4912			0.0291
#2		 1.0				0.3859			0.0305
#3		 1.0				0.350			0.0316
#4		 1.0				0.458			0.0319
#5		 1.0				0.409			0.0331
#6		 1.0				0.340			0.0337
#7		 1.0				0.409			0.0341
#8		 1.0				0.441			0.0342
#9		 1.0				0.351			0.0353
#10		 1.0				0.307			0.0357
#11		 1.0				0.364			0.0369
#12		 1.0				0.344			0.0363
#13		 1.0				0.352			0.0367
#14		 1.0				0.389 			0.0376
#15		 1.0				0.367 			0.0381
#16		 1.0				0.375 			0.0351
#17		 1.0				0.370 			0.0361
#18		 1.0				0.396 			0.0367
#19		 1.0				0.423 			0.0366
#20 	 1.0 				0.437			0.0372

