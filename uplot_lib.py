from IPython.display import IFrame, HTML
import json
from jinja2 import Template

# def uplot_data(data=[], options='{}', html=False):
def uplot_data(data=[], labels=[], html=False, **kwargs):
    """ Wrapper to use javascript library uplot in jupyter

    Keyword arguments:
        data:  List of data to be plotted, the format is [x, y1, y2, ...]
                x, y1, y2, etc are all lists of values.   They all need to be
                the same length.   If there are no values of y for an x value,
                None can be used as the y-value for that x-value
        labels: List of Labels for each y-list in data.
        html: instead of returning rendered HTML, return string of html to be
                renedered
        **kwargs:  Extra arguments to be passed to the uplot library
                e.g. title='Title', size=10, etc.

    Javascript library source code
    https://github.com/leeoniya/uPlot
    """

    h = '''
        <link rel="stylesheet" href="https://leeoniya.github.io/uPlot/dist/uPlot.min.css">
        <script src="https://leeoniya.github.io/uPlot/dist/uPlot.iife.js"></script>

        <div id="plot"></div>

        <script>
        data = {{data}}
        options = {{options}};

        if (typeof options.scatter == 'undefined') {
            options.scatter = false
        }
        if (options.scatter) {
            for (i=1; i<data.length; i++) {
                options['series'][i]["paths"] = u => null;
            }
        }
        u2 = new uPlot(options, data, document.getElementById("plot"))
        </script>
'''
    options = build_uplot_options(len(data)-1, labels, **kwargs)
    h2 = Template(h).render(data=json.dumps(data), options=options)
    h2 = h2.replace('"', "'")
    # print(h2)
    iframe = '''<iframe srcdoc="{source}" src="" 
                width={w} height="{h}" frameborder="0" sandbox="allow-scripts">
                </iframe>'''
    if html:
        return h2
    else:
        # return HTML(h2)
        return HTML(iframe.format(source=h2, w=800, h=400))

def build_uplot_options(num_yseries, labels=[], **kwargs):
    #  If plot shows up but no points, the number of lables/series may mismatch
    #  the number y-series values
    colors = ["lavender",
              "thistle",
              "plum",
              "violet",
              "orchid",
              "fuchsia",
              "magenta",
              "mediumorchid",
              "mediumpurple",
              "blueviolet",
              "darkviolet",
              "darkorchid",
              "darkmagenta",
              "purple",
              "indigo"
             ]
    colors.reverse()
    options_dict = {'title': '',
                    'width': 750,
                    'height': 300,
                    'scales': {'x': {'time': False}, 'y': {'auto': True}},
                    'series': [{'label': 'x'}]}
    for key in kwargs.keys():
        if key in options_dict.keys():
            options_dict[key] = kwargs[key]
    if 'scatter' in kwargs.keys():
        options_dict['scatter'] = kwargs['scatter']
    if 'size' in kwargs.keys():
        size = kwargs['size']
    else:
        size = 2
    #  Check that length of labels matches length in data
    # build options
    if (len(labels)<(num_yseries)):
        extra = [f'y_{i}' for i in range(num_yseries-len(labels))]
        labels += extra
    else:
        labels = labels[:num_yseries]
    if len(labels):
        y_series = [{'label': labels[i], 
                     'stroke': colors[i], 
                     'points': {'space': 0, 'size': size}}
                    for i in range(len(labels))]
        # print(y_series)
        options_dict['series'] += y_series
    return json.dumps(options_dict)

def uplot_scatter(data, labels=[], html=False, **kwargs):
    """ Wrapper to use javascript library uplot in jupyter to make a
    scatterplot

    Keyword arguments:
        data:  List of data to be plotted, the format is [x, y1, y2, ...]
                x, y1, y2, etc are all lists of values.   They all need to be
                the same length.   If there are no values of y for an x value,
                None can be used as the y-value for that x-value
        labels: List of Labels for each y-list in data.
        html: instead of returning rendered HTML, return string of html to be
                renedered
        **kwargs:  Extra arguments to be passed to the uplot library
                e.g. title='Title', size=10, etc.

    Javascript library source code
    https://github.com/leeoniya/uPlot
    """
    return uplot_data(data, labels, html=html, scatter=True, **kwargs)

def uplot_multixy(data=[], labels=[], html=False, **kwargs):
    """ Wrapper to use javascript library uplot in jupyter to make a
    scatterplot with multiple x and y values

    Keyword arguments:
        data:  List of data to be plotted, the format is [x1, y1, x2, y2, ...]
                x1, y1, y2, etc are all lists of numbers.   The x_n and y_n
                need to be the same length.  But, the different sets of x and
                y values do not need to be the same.   The wrapper merges all
                of the x values into one large x list.
        labels: List of Labels for each y-list in data.
        html: instead of returning rendered HTML, return string of html to be
                renedered
        **kwargs:  Extra arguments to be passed to the uplot library
                e.g. title='Title', size=10, etc.

    Javascript library source code
    https://github.com/leeoniya/uPlot
    """

    h = '''
        <link rel="stylesheet" href="https://leeoniya.github.io/uPlot/dist/uPlot.min.css">
        <script src="https://leeoniya.github.io/uPlot/dist/uPlot.iife.js"></script>
        
        <div id="plot"></div>

        <script>
        function build_data(d) {
          data = [d[0], d[1]]
          if (d.length>2) {
            i=2
            while(i<d.length) {
              data = merge(data, [d[i], d[i+1]])
              i += 2
            }
          }
          return data
        }

        function sorted(input, argsort) {
          let sorted = new Array(argsort.length)
          for(let i=0; i<argsort.length; i++) {
            sorted[i] = input[argsort[i]]
          }
          return sorted
        }

        function merge(a,b) {
          // build t, but don't sort yet
          t = a[0]
          t = t.concat(b[0])
          //
          argsort = t.map((item,idx)=>[item,idx]).sort((a,b)=>(a[0]-b[0])).map(item=>item[1])
          // console.log('argsort',argsort)

          t = sorted(t, argsort)
          data = [t]
          // console.log('a.length', a.length);
          for (let i=1; i<a.length; i++) {
            let y1 = [...a[i]] // shallow copy
            y1.length += b[0].length;
            let s = sorted(y1, argsort)
            data.push(s)
            // console.log('push s', i, s)
          }
          y2 = new Array(a[0].length)
          y2 = y2.concat(b[1])
          s = sorted(y2, argsort)
          data.push(s)
          return data
        }

        data_in = {{data}}
        data = build_data(data_in)
        // console.log(data)
        options = {{options}};
        for (i=1; i<data.length; i++) {
            options['series'][i]["paths"] = u => null;
        }
        u2 = new uPlot(options, data, document.getElementById("plot"))
        </script>
'''
    options = build_uplot_options(len(data)>>1, labels, **kwargs)
    h2 = Template(h).render(data=data, options=options)
    h2 = h2.replace('"', "'")
    # print(h2)
    iframe = '''<iframe srcdoc="{source}" src="" 
                width={w} height="{h}" frameborder="0" sandbox="allow-scripts">
                </iframe>'''
    if html:
        return h2
    else:
        # return HTML(h2)
        return HTML(iframe.format(source=h2, w=800, h=400))

