from Tkinter import *
import csv

#root = Tk()
#root.withdraw()
print 'hidden table'

def getTable():
    root = Tk()
    table = []

    with open('../gameRecord/ranking.csv', 'r') as csvfile:
        obj = csv.reader(csvfile)

        for row in obj:
            table.append(row)

        class Table:	
            def __init__(self,root):
                for i in range(1, total_rows+1):
                    for j in range(1, total_columns+1):
                        if i==1:
                            self.e = Entry(root, width=18, fg='red', font=('Arial',13,'bold'))
                        else:
                            self.e = Entry(root, width=18, fg='blue', font=('Arial',13,'bold'))
                        self.e.grid(row=i, column=j)               
                        if j==total_columns and i!=1:
                            self.e.insert(END, table[i-1][j-1] + 's')
                        else:
                            self.e.insert(END, table[i-1][j-1])
                                             
    total_rows = len(table)
    total_columns = len(table[0])

    root.title("Ranking Table of Top 10")
    t = Table(root)
    
    root.mainloop()
 
def showTable():
    #root.deiconify()
    print 'show table'
 
if __name__ == '__main__':
    getTable()