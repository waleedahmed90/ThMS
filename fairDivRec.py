import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import time
import sys


def CustomerUtility(A,AddVal,V,k):
	
	phi_u = {}
	n = len(A)
	for a in range(len(A)):
		#pick a list of all available goods
		available_goods = list(V.iloc[a,:])
		#sorting their relevance score in descending order
		available_goods.sort(reverse=True)
		#top k desired goods by the agent from the available goods
		top_k = available_goods[:k]
		#aditive valuation of the desired goods
		desired_relevance_score = sum(top_k)
		#utility from recommendation set relative to the desired goods
		utility = AddVal[a]/desired_relevance_score
		#storing it in phi_u dictionary
		phi_u[a] = utility
	

	#extracting values sorted utilities in descending order
	utility_scores = list(phi_u.values())
	utility_scores.sort(reverse=False)

	endScore = len(utility_scores)

	temp = np.array(utility_scores)
	sum_outer = 0;
	
	for i in range(0,endScore-1):
		sum_inner=0
		pivot = temp[i]
		rest = temp[(i+1):]
		sum_outer = sum_outer + ((np.sum(rest-pivot))/(endScore-1))

	Y = sum_outer/endScore

	return Y

def ProdExp(A,n,MMS):
    
	P = [0] * n
	
	for p in range(n):
		for u in A:
			if (p in A[u]):
				P[p] = P[p]+1	



	#for u in A:
	#	for p in range(n):
	#		if (p in A[u]):
	#			P[p] = P[p]+1

	H = 0    
	for p in P:
		if (P[p]>=MMS):
			H = H+1        
	H = H/n
	return H        

#returns a topological sort
def DAG_EnvyGraph(AddVal, A):
	#x = {}

	#for i in A.keys():
	#    if(len(A[i])>0):
	#        x[i] = sum(valuations(i,A[i],V))
	##    else:
	#        x[i]=0

	sigma = {k: v for k, v in sorted(AddVal.items(), key=lambda item: item[1])}
	return list(sigma.keys())

#new GRR
def GRR(C_h, AddVal, sigma, P1, F, c, k, Count_agents,V, allocation_counter):
	#temporary Allocations
	B={}
	for i in range(len(AddVal)):
		B[i] = []

	for u in sigma:
		
		#If there is no more goods left in this category
		if ((P1[c] == 0)):
			return B, P1, Count_agents, F, AddVal, allocation_counter

		#If the recommendation list for this agent has reached its capacity k
		if (Count_agents[u] == k):
			#return B, P1, Count_agents, F, AddVal, allocation_counter
			continue
		#If category exists in the Feasibility Set of user u and Items are available in the Category
		elif ((c in F[u]) and (P1[c]>0) and (Count_agents[u]<k)):
			B[u].append(c)
			F[u].remove(c)
			P1[c]=P1[c]-1
			Count_agents[u] = Count_agents[u]+1

			AddVal[u] = AddVal[u]+V.iloc[u,c]

			allocation_counter = allocation_counter+1

	return B, P1, Count_agents, F, AddVal, allocation_counter


def FairRec(U, P, k, V, alpha, m, n, l):

#U: Customers
#P: Producers
#k: Size of Recommendation Set
#V: Relevance Scores Matrix
#m: Number of Customers
#n: Number of Producers
#l: Copiers of every product
   
####Phase-1
        
	#Total Exposure/aka Total number of items to be allocated
	T = l*n
	print("T = ", T)

	#Allocation set for each customer: Same size the number of customers: A dictionary of lists
	A = {}
	#Feasibility set for each customer: Initialized with P: A dictionary of lists
	F = {}
	#Initialization
	for i in range(len(U)):
		A[i] = []	#each location has a list of size k (recommended items)
		F[i] = [j for j in range(n)] #each location is populated with all the products, each index has a list of size n



	#keeps a count of how many objects have been assigned to an agent
	Count_agents = [0] * m

	#set of additive valuations
	AddVal = {}

	for i in range(len(U)):
		AddVal[i] = 0

	sigma = list(AddVal.keys())

    #Call Greedy Round Robin from FairDiv for each category
	P1=P
	allocation_counter=0
	for h in range(len(P)):
	#pick a category
	    	
		C_h = list(V.iloc[:,h])
		#Calls GRR
		[B, P1, Count_agents, F, AddVal, allocation_counter]=GRR(C_h, AddVal, sigma, P1, F, h, k, Count_agents,V, allocation_counter)
		#extend B to A
		for u in range(m):
			A[u].extend(B[u])
		#AddVal k through topological sorting aur DAG Envy Graph
		sigma = DAG_EnvyGraph(AddVal, A)
    	#naya sigma
	#print("Count agents")
	#print(Count_agents)
	#Calling Greedy Round Robin##################################################
	#print("Total Allocatable Goods:",T)
	#print("Total Allocated Goods:",allocation_counter)
	#print("Total Unallocated Goods:",(T-allocation_counter))
	#print("Total Total Agents Left:",(len(A)-allocation_counter))

	#[B,F1,P1]=GRR(m,n,R,l,T,V,U,F,P)
	print("GRR DONE FOR ALL CATEGORIES")
	#A=B
	#sys.exit()
####Phase-2
	#agents with less than k products
	left_out_agents = []
	#print("Count_agents")
	#print(Count_agents)
	for a in range(len(Count_agents)):
		if (Count_agents[a]<k):
			left_out_agents.append(a)
		#print(a,", ",Count_agents[a])
		#if (Count_agents[a]<k):
		#	left_out_agents.append(a) 	
	#print("left_out_agents",left_out_agents)
	
	#print("left_out_agents")
	#print(left_out_agents)

	left_out_producers = []

	for p in range(len(P1)):
		if (P1[p]!=0):
			left_out_producers.append(p)


	for a in left_out_agents:
		relv_scores = V.iloc[a,:]
		new_relv = relv_scores.argsort()[-(k+k):][::-1]
		#print("NEW Relevance")
		#print(new_relv)

		for g in new_relv:
			if g not in A[a]:
				#print(g)
				A[a].append(g)
				P1[g] = P1[g]-1
				AddVal[a] = AddVal[a]+V.iloc[a,g]
				Count_agents[a] = Count_agents[a]+1
			if len(A[a])==k:
				break
				#sys.exit()
	return A, P1, AddVal

if __name__== "__main__":
	start_time = time.time()
    #Relevance scoring set
	V = pd.read_csv("GL-CUSTOM.csv")
    
	print(">>>>> Dataset loaded")

	#recommendation size
	#k=10
	k=20
	#alpha=0.5
	alpha=1.0
    #cardinality_constraint
	k_h=1

	#Every product with l copies is considered as 1
	#category
	(m,n) = V.shape
	#Rows(m):No of Customers   |U|
	print(">>>>> Number of Customers determined",m)
	#Columns(n): No of Producers |P|
	print(">>>>> Number of Products determined",n)

	#Copies of each product 
	l = math.ceil(alpha*int((m*k)/n))

	#Exposure Guarantee
	MMS = math.floor((m*k)/n)
    
    
	print(">>>>> Copies per product: l = "+str(l))
    
	#Creating Customers/list
	U = [i for i in range(m)]
	print(">>>>> Customers list created")
    
	P = [l] * n
	print(">>>>> Producers list created")
	#print(P)
	print("##############################")
    
	##Calling FairRec Algorithm
	[A,P1,AddVal] = FairRec(U,P,k,V,alpha,m,n,l)
	print("Allocations")
	print(A)

	
	
	H = ProdExp(A,n,MMS)
	Y = CustomerUtility(A,AddVal,V,k)
	print("k:",k)
	
	print("Mean Average Envy: (Y): ",Y)
	print ("Fraction of Satisfied Producers: (H):",H)
	print("Elapsed Time")
	print("--- %s seconds ---" % (time.time() - start_time))