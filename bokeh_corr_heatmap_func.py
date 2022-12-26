#Importing libraries

from bokeh.plotting import figure
from bokeh.layouts import  row
from bokeh.io import show
from bokeh.models.annotations import Label

from math import pi

import pandas
import numpy

df = pandas.read_csv("...your_path_to_your_file.../your_table_for_correlation_analysis.csv", sep=",")

#Checking the dataframe you loaded.
print(df.head())
def render_correlation_plot_bokeh(my_data_frame):
    df_numerical = df.select_dtypes(exclude="object")

    correlation_matrix = df_numerical.corr()
    
    #Get how many values will be in each dimension. It will be a square.
    table_one_dimension = correlation_matrix.shape[1]

    #Create an array from available correlations. Creating this from Numpy array as reshaping from Pandas is not practical.
    correlation_matrix_numpy = correlation_matrix.to_numpy()
    correlation_array = correlation_matrix_numpy.reshape(-1)

    #Create a list that will include the colors from the values in the correlation array in the order of correlation array
    correlation_color_list = [
    "lime" if (value<=0 and value>-.25) or (value>=0 and value<.25)
    else "green" if (value<=-0.25 and value>-.50) or (value>=0.25 and value<.50)
    else "orangered" if (value<=-0.50 and value>-.75) or (value>=0.50 and value<.75)
    else "red" for value in correlation_array]


    #Create a Numpy matrix as a layer to show only the colors defined in the correlation_color_list
    color_matrix = numpy.array(correlation_color_list)
    color_matrix = color_matrix.reshape((table_one_dimension,table_one_dimension))
    #Flip the color matrix to start from top to bottom; not from bottom to top.
    color_matrix = numpy.flip(color_matrix, axis=0)

    #For aligning the position of the cell squares representing each cell on the heat-map. 0.5 shift fits perfectly.
    alignment_list_for_rows = []
    for i in range(table_one_dimension):
        alignment_list_for_rows.append(i+0.5) 

    #Create x and y ranges to be used in Bokeh plot
    x_range_ = list(df_numerical.columns)
    y_range_ = list(df_numerical.columns)

    #Reverse y range for fitting to the heat map. 
    #Otherwise first item starts from bottom, while we want it to start from top and the x range start from left.
    y_range_.reverse()

    #Define the Bokeh figure and assign ranges. Some small adjustments for x axis labels.
    f = figure(title="Correlation Heat Map", x_range=x_range_, y_range=y_range_)
    f.xaxis.major_label_orientation = pi/6
    f.xaxis.major_label_text_font_size = "8pt"

    #Create the color layer for each cell one by one with two for loops.
    #One loop for rows and other for columns. Each cell has a width and height of one unit. Colors are defined according to color matrix.
    for row in range(table_one_dimension):
        for col in range(table_one_dimension):
            f.rect(x=alignment_list_for_rows[col], y=alignment_list_for_rows[row], width=1, height=1, color=color_matrix[row,col])


    #Reversing/flipping the correlation matrix to start from top to bottom rather than from bottom to top.
    #This fits the numpy matrix to the plot as we want.

    correlation_matrix_numpy = numpy.flip(correlation_matrix_numpy, axis=0)


    #Creating text layer via two for loops; one for each row other for each column
    #This creates a value for all cells one by one and uses the values in correlation_dataframe_numpy
    for row in range(table_one_dimension):
        for col in range(table_one_dimension):
            mytext = Label(x=col+0.3, y=row + 0.5, text=str(round(correlation_matrix_numpy[row, col], 2)), text_font_size="10px")
            f.add_layout(mytext)
    show(f)
#Test your function
render_correlation_plot_bokeh(df)

