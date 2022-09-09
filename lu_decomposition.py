import numpy as np
import os, sys
# set working directory of python to the current folder
os.chdir(os.path.dirname(sys.argv[0]))

# function to switch two rows (indices i and j) of a given matrix of size n-by-n
def row_switch(matrix, i, j, n):
    if (i!=j):
        temp=np.zeros((1,n), dtype=float)
        temp=np.copy(matrix[i,:])
        matrix[i,:]=np.copy(matrix[j,:])
        matrix[j,:]=np.copy(temp)
        
# function to perform pivoting by switching the current row with the row having max. column element
def pivoter(matrix, i, n):
    pivot_row=i
    pivot_element=matrix[i,i]
    j=i+1
    while j<n:
        if abs(matrix[j,i])>abs(pivot_element):
            pivot_element=matrix[j,i]
            pivot_row=j
        j+=1
    row_switch(matrix, i,pivot_row,n)
    if(i!=pivot_row):
        return([i,pivot_row])
    else:
        return([])

# function to perform row operations to get upper triangular marix
# also uses the row operation multiplier factors to populate lower triangular matrix L
def column_elimination(matrix, L, i, n):
    j=i+1
    while j<n:
        if (matrix[i,i]==0):
            return
        else:
            factor = matrix[j,i]/matrix[i,i]
            np.subtract(matrix[j,:], matrix[i,:]*factor, out = matrix[j,:])
            L[j,i]=factor
            j+=1

# perform gaussian elimination using the above functions
def gaussian_elimination(matrix, L,  n, row_switch_list):
    i=0
    while (i<n):
        temp=pivoter(matrix, i, n)
        row_switch_list.append(temp)
        column_elimination(matrix, L, i, n)
        i+=1

# shuffle L matrix to account for pivoting
def lower_triang_shuffler(matrix, row_switch_list):
    for item in row_switch_list:
        if len(item)==0 or item[0]==0:
            pass
        else:
            k=0
            i=item[0]
            j=item[1]
            while k<i:
                temp=np.copy(matrix[i,k])
                matrix[i,k]=np.copy(matrix[j,k])
                matrix[j,k]=temp
                k+=1

# main function
def main():
    x=int(input("Enter 1 if you want to input matrix manually and 0 if you want to provide text file: \n"))
    if (x==1):
        n=int(input("Enter the number of rows of A: \n"))
        A=np.zeros((n,n), dtype=float)
        i=1
        print("Enter the rows one after another: ")
        while i<=n:
            temp=list(map(float, input().rstrip().split()))
            A[i-1,:]=temp
            i+=1
    elif (x==0):
        filename=input("Enter filename (with file extension):\n")
        fID=open(filename,'r')
        n=int(input("Enter the number of rows of A: \n"))
        A=np.zeros((n,n), dtype=float)
        i=0
        for line in fID:
            A[i,:]=list(map(float, line.rstrip().split()))
            i+=1
    else:
        print("Error!! Rerun and choose valid option!!")
        return
    row_switch_list=list()
    L=np.identity(n)
    gaussian_elimination(A, L, n, row_switch_list)
    print("Upper triangular matrix (U) is")
    print(A)
    print("Lower triangular matrix (L) is")
    lower_triang_shuffler(L, row_switch_list)
    print(L)
    print("Reconstructed matrix (LU) is")
    print(np.matmul(L,A))
    
main()