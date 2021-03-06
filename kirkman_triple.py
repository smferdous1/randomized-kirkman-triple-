#kirkman triple system generator
import networkx as nx
import random as rand
import time

#whether the induced subgraph by vert creates a clique in G
def is_clique(G,vert):
    size = len(vert)
    for i in range(size):
        for j in range(i+1,size,1):
            if G.has_edge(vert[i],vert[j]) == False:
                return False

    return True

#deleting a clique generated by the vertices of vert
def delete_clique(G,vert):
    size = len(vert)
    for i in range(size):
        for j in range(i+1,size,1):
            G.remove_edge(vert[i],vert[j])

#adding a clique to the graph
def add_clique(G,vert):
    size = len(vert)
    for i in range(size):
        for j in range(i+1,size,1):
            G.add_edge(vert[i],vert[j])

#If we get stuck in a partial partition, its better to roll back
def rollback(G,S):
    for s in S:
        add_clique(G,s)


#number of times we want to run for a particular n
ntest = 1
#the start m
start = 5
#the end m
end = 100
k = 4


#looping for each m
for m in range(start,end):
    # n must be such that n mod 6 = 3
    #n = 6*m+3
    n = k*m
  #number of element in each block; if k is changed n must be adjusted accordingly. e.g., k=4, a possible n could be 4*m
    #for averaging the number of permutation accross different test
    totcount = 0
    abort_count = 0
    start = time.time()

    for test in range(ntest):
      #the universe is the set U={1,2,...,n}
        U = set(range(n))

        G = nx.complete_graph(n)
        #for saving the actual permutation.
        S = [[] for i in range(5000)]
        count = 0

        #number of unsuccessfull trials allowed
        L = 1000000*m
        for i in range(L):
            #randomly sample withour replacement from U
            vert = rand.sample(U, k)
            if is_clique(G, vert) is True:
                abort_count = 0
                U = U.difference(set(vert))
                #successfull trials; compensate L
                L = L + 1
                #delete the edges of the clique so that it can not appear in next permutation
                delete_clique(G, vert)
                #append in the partial permutation
                S[count].append(vert)
                # we got a full permutation.
                if len(S[count]) == n/k:
                    #print(S[count])
                  #print(count)
                    count = count + 1
                  #reset the U for next permuation
                    U = set(range(n))
      #unsuccessfull trials
            else:
                abort_count = abort_count + 1
                #too many unsuccessfull trials; so roll back and abort the partial permuation
                if abort_count == 1000:
                    abort_count = 0
                    U = set(range(n))
                    rollback(G, S[count])
                    S[count].clear()
    totcount = totcount + count
    end = time.time()
    #print the result; the m, n, theoretical bound on number of permutation, average number of permutation, average time to get it
    #print(m,",",n,",",3*m+1,",",float(totcount)/ntest,(end-start)/ntest)
    print(m, ",", n, ",", float(totcount)/ntest, (end-start)/ntest)

  #print(S)

