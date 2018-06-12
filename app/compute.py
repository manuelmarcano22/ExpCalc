import math
import numpy as np
#Bokeh
from bokeh.resources import CDN, INLINE
from bokeh.plotting import figure
from bokeh.embed import autoload_static, components
from bokeh.models import  ColumnDataSource

def sin(x):
    return math.sin(x)


def damped_vibrations(t, A, b, w):
    return A*np.exp(-b*t)*np.cos(w*t)

def compute(A, b, w, T, resolution=500):
    """Return t,u of plot of the damped_vibration function."""
    t = np.linspace(0, T, resolution+1)
    u = damped_vibrations(t, A, b, w)
    return t,u

def computeexptime(snr):
    """Return Exposure time given the noisees and snr desired."""
    exptime = snr*2.0
    return exptime


def bplot(x,y):
    """Descript Function"""

    #Define data
    x = np.array(x)
    y = np.array(y)
    source = ColumnDataSource(data=dict(x=x,y=y))
    plot = figure(sizing_mode='scale_width',plot_width=100, plot_height=50)
    plot.line('x','y',source=source)
    #JS
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script, div = components(plot)
    
    return script, div, js_resources, css_resources
