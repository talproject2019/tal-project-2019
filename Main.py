import numpy as np
import matplotlib.pyplot as plt
from module1 import *
def fit_linear(filename):
    format_check=row_or_column(filename)
    if format_check=='columns':
        try:
            table = columns_to_table(filename)
        except IndexError:
            return print('Input file error: Data lists are not the same length')
    else:
        table=rows_to_table(filename)
    table = table_str_to_float(table)
    if check_length(table)==False:
        return print('Input file error: Data lists are not the same length')
    if check_errors(table)==False:
        return print('Input file error: Not all uncertainties are positive')
    x=calculate_average(table,'x')
    y=calculate_average(table,'y')
    xy=xy_average(table)
    x2=squared_average(table,'x')
    dy2=squared_average(table,'dy')
    if a_b_steps(filename)!=False:
        axis_names = file_to_axis_names(filename)
        x_axis = axis_names[0]
        y_axis = axis_names[1]
        a_and_b=a_b_steps(filename)
        [best_a, best_b, best_chi2, graph_a, graph_chi2]=\
            chi2_for_given_parameters(a_and_b,table)
        chi2_red = best_chi2 / (len(table[0]) - 3)
        plot_chi2_vs_a(graph_a, graph_chi2, best_b)
        plot(table, best_a, best_b, x_axis, y_axis)
        return final_output(best_a,a_and_b[0][3]
                            ,best_b,a_and_b[1][3],
                            best_chi2,chi2_red)
    #the parameters function will give output [a, da, b, db]
    [a, da, b, db]=parameters(xy,x,y,x2,dy2,table)
    chi2=chi(table,a,b)
    axis_names=file_to_axis_names(filename)
    x_axis=axis_names[0]
    y_axis=axis_names[1]
    plot(table,a,b,x_axis,y_axis)
    return final_output(a,da,b,db,chi2[0],chi2[1])