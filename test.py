# coding: utf-8


def tri(n=10):
	L = [1]
	for x in range(n):
		print(L)
		k = [L[i]+L[i+1] for i in range(x)]
		L = [1] + k + [1]


tri()

a = [x for x in []]
print(a)
