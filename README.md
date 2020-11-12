# Simple wrapper around the uplot javascript library for plotting in jupyter notebooks

* Primarily for quick looking at large datasets that cause matplotlib and
  plotly to struggle (i.e. 10,000 points or more)
* It is possible to zoom in on the plots by dragging the mouse across the plot
* Double clicking in the plot area resets the axis to the auto-scaled extents
* Very little parameter checking is implemented.  If there is an error in a
  parameter the plot will not render
* There are three functions:
    * uplot_data:  basic plotting, points are connected to each other with a
      line
    * uplot_scatter: same as above except only circles for each data point
    * uplot_multixy:  handles multiple x,y values

* For a better understanding of the plotting capabilities please go to the
  javascript source code for [uplot](https://github.com/leeoniya/uPlot)
