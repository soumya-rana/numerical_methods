import numpy as np
import os, sys
# set working directory of python to the current folder
os.chdir(os.path.dirname(sys.argv[0]))

# function to switch two rows (indices i and j) of a given matrix of size n-by-n and the RHS column vector
def row_switch(matrix, vector, i, j, n):
    if (i!=j):
        temp=np.zeros((1,n), dtype=float)
        temp=np.copy(matrix[i,:])
        matrix[i,:]=np.copy(matrix[j,:])
        matrix[j,:]=temp
        temp=np.copy(vector[i])
        vector[i]=np.copy(vector[j])
        vector[j]=temp
        
# function to perform pivoting by switching the current row with the row having max. column element
def pivoter(matrix, vector, i, n):
    pivot_row=i
    pivot_element=matrix[i,i]
    j=i+1
    while j<n:
        if abs(matrix[j,i])>abs(pivot_element):
            pivot_element=matrix[j,i]
            pivot_row=j
        j+=1
    row_switch(matrix, vector, i,pivot_row,n)
    return([i,pivot_row])

# function to perform row operations to get upper triangular marix
def column_elimination(matrix, vector, i, n):
    j=i+1
    while j<n:
        if (matrix[i,i]==0):
            return
        else:
            factor = matrix[j,i]/matrix[i,i]
            np.subtract(matrix[j,:], matrix[i,:]*factor, out = matrix[j,:])
            vector[j,0] = vector [j,0]- vector[i,0]*factor
            j+=1

# perform gaussian elimination using the above functions
def gaussian_elimination(matrix, vector, n):
    i=0
    while (i<n):
        pivoter(matrix, vector, i, n)
        column_elimination(matrix, vector, i, n)
        i+=1

# find rank of augmented matrix using rank of A matrix and b vector
def rank_augmented(vector, matrix_rank,n):
    i=n-1
    while i>=0:
        if vector[i]!=0:
            break
        i-=1
    return max(matrix_rank, i+1)

# perform backward sweep to obtain solution
def backward_sweep(matrix, vector, solution, n):
    i=n-1
    while i>=0:
        solution[i]=vector[i]/matrix[i,i]
        i-=1
    i=n-2
    while i>=0:
        j=i+1
        while j<n:
            solution[i]-=solution[j]*matrix[i,j]/matrix[i,i]
            j+=1
        i-=1

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
        b=np.zeros((n,1), dtype=float)
        print("Enter b (as a row vector): \n")
        b[:,0]=list(map(float,input().rstrip().split()))
    elif (x==0):
        filename=input("Enter filename (with file extension). Make sure last row of file contains b:\n")
        fID=open(filename,'r')
        n=int(input("Enter the number of rows of A: \n"))
        A=np.zeros((n,n), dtype=float)
        b=np.zeros((n,1), dtype=float)
        i=0
        for line in fID:
            if (i==n):
                b[:,0]=list(map(float,line.rstrip().split()))
            else:
                A[i,:]=list(map(float, line.rstrip().split()))
            i+=1
    else:
        print("Error!! Rerun and choose valid option!!")
        return
    gaussian_elimination(A, b, n)
    print("The upper triangular matrix is: ")
    print(A)
    rank_A=np.linalg.matrix_rank(A)
    rank_A_b=rank_augmented(b,rank_A, n)
    if (rank_A!=rank_A_b):
        print("Inconsistent set of equations!! No solution exists!! ")
        return
    elif (rank_A !=n):
        print(" No unique solution exists!! ")
        return
    else:
        x=np.zeros((n,1), dtype=float)
        backward_sweep(A, b, x, n)
        print("The solution is: ")
        print(x)
main()
