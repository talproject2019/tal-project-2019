import numpy as np
import matplotlib.pyplot as plt
#this function finds the chi squared and reduced
def chi(table,a,b):
    chi2=0
    for n in range(1,len(table[2])):
        chi2=chi2+((table[2][n]-(a*table[0][n]+b))**2)/\
                    (table[3][n]**2)
    chi2_red=chi2/(len(table[0])-3)
    chi2=chi2+0.000000000000002
    return [chi2,round(chi2_red,15)]

#this function calculates the a and b parameters and their errors
def parameters(xy,x,y,x2,dy2,table):
    a=(xy-x*y)/(x2-x**2)
    da2=dy2/((len(table[0])-1)*(x2-x**2))
    da=np.sqrt(abs(da2))
    b=y-a*x
    db2=(dy2*x2)/((len(table[0])-1)*(x2-x**2))
    db = np.sqrt(abs(db2))
    return [a,da,b,db]

#this calculates the average
def calculate_average(table,subject):
    for n in range(0,len(table)):
        if subject==table[n][0]:
            target=n
    sub_top=0
    sub_bot=0
    for n in range(1,len(table[target])):
        sub_top=sub_top+(table[target][n])/(table[3][n]**2)
        sub_bot=sub_bot+1/(table[3][n]**2)
    result=sub_top/sub_bot
    return result

#this calculates the squared average for x2 and dy2
def squared_average(table,subject):
    for n in range(0,len(table)):
        if subject==table[n][0]:
            target=n
    sub_top=0
    sub_bot=0
    for n in range(1,len(table[target])):
        sub_top=sub_top+((table[target][n])**2)/\
                        (table[3][n]**2)
        sub_bot=sub_bot+1/(table[3][n]**2)
    result=sub_top/sub_bot
    return result
def xy_average(table):
    sub_top = 0
    sub_bot = 0
    for n in range(1, len(table[0])):
        sub_top = sub_top + ((table[0][n]) *(table[2][n])) /\
                            (table[3][n] ** 2)
        sub_bot = sub_bot + 1 / (table[3][n] ** 2)
    result = sub_top / sub_bot
    return result

#this function checks the uncertainties
def check_errors(table):
    for n in range(1,len(table[1])):
        if not table[1][n]>0:
            return False
    for n in range(1,len(table[3])):
        if not table[3][n]>0:
            return False
    return True
#this function checks that there are an equal amount of x and y coordinates
def check_length(table):
    for n in range(0,len(table)):
        for j in range(0,len(table)):
            if len(table[n])!=len(table[j]):
                return False
    return True

#this programs turns column format input into a table
def columns_to_table(file_name):
    #creating initial list
    open_sesame = open(file_name,'r+')
    source = open_sesame.readlines()
    x_line=[]
    dx_line=[]
    y_line=[]
    dy_line=[]
    for n in range(0,len(source)):
        source[n]=source[n].split()
    #remove empty lists created by split
    try:
        for n in range(0,len(source)):
            if source[n]==[]:
                source.remove(source[n])
    except:
        None
    #lowercase
    for n in range(0,4):
        source[0][n]=source[0][n].lower()
    #line check and append
    for n in range(0,4):
        if source[0][n]=='x':
            for i in range(0,len(source)-2):
                x_line.append(source[i][n])
        if source[0][n]=='y':
            for i in range(0,len(source)-2):
                y_line.append(source[i][n])
        if source[0][n]=='dx':
            for i in range(0,len(source)-2):
                dx_line.append(source[i][n])
        if source[0][n]=='dy':
            for i in range(0,len(source)-2):
                dy_line.append(source[i][n])
    table=[x_line,dx_line,y_line,dy_line]
    for n in range(0,len(table)):
        k=1
        while k<len(table[n]):
            try:
                x=float(table[n][k])
                k=k+1
            except:
                del table[n][k]
    return table

#this function extracts the axis names from file
def file_to_axis_names(file_name):
    #creating initial list
    open_sesame = open(file_name,'r+')
    source = open_sesame.readlines()
    for n in source:
        if 'y axis' in n:
            y_name=n
        if 'x axis' in n:
            x_name=n
    temp_name = [y_name.split(': '),x_name.split(': ')]
    for n in temp_name:
        if n[0]=='x axis':
            x_axis_name=n[1]
        if n[0]=='y axis':
            y_axis_name=n[1]
    return (x_axis_name[:-1],y_axis_name[:-1])

#this does the graph
def plot(table,a,b,x_axis_name,y_axis_name):
    x_values=table[0][1::]
    dx_values=table[1][1::]
    y_values = table[2][1::]
    dy_values = table[3][1::]
    max_x=max(table[0][1::])
    min_x=min(table[0][1::])
    fit_x=[min_x,max_x]
    fit_y=[min_x*a+b,max_x*a+b]
    graph=plt.plot(fit_x,fit_y,'r',zorder=0)
    grapherr = plt.errorbar(x_values, y_values, yerr=dy_values,
                            xerr=dx_values, fmt='none',
                            ecolor='blue',zorder=5)
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)
    plt.savefig('linear_fit.svg')
    return plt.show()

#this program checks whether the input is in row or in columns
def row_or_column(file_name):
    #creating initial list
    open_sesame = open(file_name,'r+')
    source = open_sesame.readlines()
    for n in range(0,len(source)):
        source[n]=source[n].split()
    #remove empty lists created by split
    try:
        for n in range(0,len(source[:])):
            if [] in source:
                source.remove([])
    except:
        None
    #lowercase
    for n in range(0,len(source)):
        for j in range(0,len(source[n])):
            source[n][j]=source[n][j].lower()
    #here we'll check whether input is in rows or in columns by checking
    #that x and y aren't both in the first list in source
    y_condition='y' in source[0]
    x_condition='x' in source[0]
    if y_condition and x_condition:
        return 'columns'
    else:
        return 'rows'
#this programs turns row format input into a table
def rows_to_table(file_name):
    #creating initial list
    open_sesame = open(file_name,'r+')
    source = open_sesame.readlines()
    x_line=[]
    dx_line=[]
    y_line=[]
    dy_line=[]
    for n in range(0,len(source)):
        source[n]=source[n].split()
    #remove empty lists created by split
    try:
        for n in range(0,len(source)):
            if source[n]==[]:
                source.remove(source[n])
    except:
        None
    #lowercase and table
    table=[]
    for n in range(0,4):
        source[n][0]=source[n][0].lower()
        if source[n][0] == 'x':
            table.insert(0,source[n])
        if source[n][0] == 'dx':
            table.insert(1,source[n])
        if source[n][0] == 'y':
            table.insert(2,source[n])
        if source[n][0] == 'dy':
            table.insert(3,source[n])
    return table
#this function turns all of the number string in the table into floats
def table_str_to_float(table):
    for n in range(0,4):
        for i in range(1,len(table[n])):
            table[n][i]=float(table[n][i])
    return table
#this function prints the final output
def final_output(a,da,b,db,chi2,chi2_red):
    print('a = {} +- {}'.format(a,da))
    print('b = {} +- {}'.format(b,db))
    print('chi2 = {}'.format(chi2))
    print('chi2_reduced = {}'.format(chi2_red))
#this function handles the file and checks whether it
# has a,b and step values and returns them
def a_b_steps(file_name):
    #creating initial list
    open_sesame = open(file_name,'r+')
    source = open_sesame.readlines()
    for n in range(len(source)):
        if 'a' in source[n][0]:
            given_a=source[n].split(' ')
        if 'b' in source[n][0]:
            given_b=source[n].split(' ')
    try:
        if '\n' in given_a[3]:
            given_a[3]=given_a[3][0:-1]
        if '\n' in given_b[3]:
            given_b[3] = given_b[3][0:-1]
        for n in range(1,4):
            given_a[n]=float(given_a[n])
            given_b[n]=float(given_b[n])
        a_and_b=[given_a,given_b]
    except:
        return False
    return a_and_b

#this function defines the chi2 according to formula 1
def chi1(table,a,b):
    chi2=0
    for n in range(1,len(table[2])):
        chi2=chi2+((table[2][n]-(a*table[0][n]+b))/
                   (np.sqrt(((table[3][n]**2)+((2*a*table[1][n])**2)))))**2
    chi2_red=chi2/(len(table[0])-3)
    chi2=chi2+0.000000000000002
    return [chi2,round(chi2_red,15)]

#this function handles the chi computing and returns
#everything needed for chi2 graph
def chi2_for_given_parameters(a_and_b,table):
    round_factor_a=len(str(a_and_b[0][3]))
    round_factor_b=len(str(a_and_b[1][3]))
    current_a=a_and_b[0][1]
    current_b=a_and_b[1][1]
    graph_a=[]
    graph_chi2=[]
    best_chi2=float('inf')
    if a_and_b[0][3]<0:
        while current_a>=a_and_b[0][2]:
            if a_and_b[1][3]>0:
                while current_b<=a_and_b[1][2]:
                    current_chi2=chi(table,current_a,current_b)[0]
                    current_b=round(current_b+a_and_b[1][3],
                                    round_factor_b)
                    if current_chi2<best_chi2:
                        best_chi2=current_chi2
                        best_a=current_a
                        best_b=current_b
            if a_and_b[1][3] < 0:
                while current_b>=a_and_b[1][2]:
                    current_chi2=chi(table,current_a,current_b)[0]
                    current_b = round(current_b + a_and_b[1][3],
                                      round_factor_b)
                    if current_chi2<best_chi2:
                        best_chi2=current_chi2
                        best_a=current_a
                        best_b=current_b
            current_a = round(current_a + a_and_b[0][3],
                              round_factor_a)
            current_b=a_and_b[1][1]
    if a_and_b[0][3] > 0:
        while current_a<=a_and_b[0][2]:
            if a_and_b[1][3]>0:
                while current_b<=a_and_b[1][2]:
                    current_chi2=chi(table,current_a,current_b)[0]
                    current_b = round(current_b + a_and_b[1][3],
                                      round_factor_b)
                    if current_chi2<best_chi2:
                        best_chi2=current_chi2
                        best_a=current_a
                        best_b=current_b
            if a_and_b[1][3] < 0:
                while current_b>=a_and_b[1][2]:
                    current_chi2=chi(table,current_a,current_b)[0]
                    current_b = round(current_b + a_and_b[1][3],
                                      round_factor_b)
                    if current_chi2<best_chi2:
                        best_chi2=current_chi2
                        best_a=current_a
                        best_b=current_b
            current_a = round(current_a + a_and_b[0][3],
                              round_factor_a)
            current_b = a_and_b[1][1]
    current_a=a_and_b[0][1]
    if a_and_b[0][3]<0:
        while current_a>=a_and_b[0][2]:
            current_chi2=chi1(table,current_a,best_b)[0]
            graph_a.append(current_a)
            graph_chi2.append(current_chi2)
            current_a = round(current_a + a_and_b[0][3],
                              round_factor_a)
    if a_and_b[0][3] > 0:
        while current_a <= a_and_b[0][2]:
            current_chi2 = chi1(table, current_a, best_b)[0]
            graph_a.append(current_a)
            graph_chi2.append(current_chi2)
            current_a = round(current_a + a_and_b[0][3],
                              round_factor_a)
    return [best_a,best_b,best_chi2,graph_a,graph_chi2]

#this function plots the graph of chi2 vs a for best b
def plot_chi2_vs_a(graph_a,graph_chi2,best_b):
    plt.plot(graph_a,graph_chi2)
    plt.xlabel('a')
    plt.ylabel('chi2(a, b = {})'.format(best_b))
    plt.savefig('numeric_sampling.svg')
    return plt.show()