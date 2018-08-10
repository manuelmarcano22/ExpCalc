import numpy as np
#Sympy to solve the CCD equation to solve for t
from sympy import Eq, solve, Symbol
#Bokeh
from bokeh.resources import CDN, INLINE
from bokeh.plotting import figure
from bokeh.embed import autoload_static, components
from bokeh.models import  ColumnDataSource
import bokeh.plotting as bk
from bokeh.models import Span


def flux(zeropoint, magnitude):
    """Return the expected count rate for an object of magnitude m in electron per second.
    Need to specify the zeropoint to use. We assume a normalized to a 20 magnitude star. """
    normalizationmag = 20.0
    f = zeropoint*10**(0.4*(normalizationmag-magnitude))
    return f

def nonlinear(flux):
    '''Retrun the point that it will become nonlinear'''
    non=45000/flux
    return non

def saturated(flux):
    '''Retrun the point that it will become saturated'''
    non=60000/flux
    return sat

def fluxsky(zeropoint, pixelscale, skybrightness):
    """Return the sky background in electrons/sec/pix. It needs the sky brightness in mag/arcsec^2, the pixel scale of the CCD in arcsec/pixel and the zeropoint (filter) to calculate the flux."""
    magnitudepixel = skybrightness - 2.5*np.log10(pixelscale**2)
    fsky = flux(zeropoint,magnitudepixel)
    return fsky


def npixel(pixelscale, radiusaperture):
    """Return the number of pixel given the pixel scale in arcsec/pixel and photometric radius of aperture given in arcseconds."""
    npixel = (np.pi * radiusaperture**2)/(pixelscale**2)
    return npixel

def skynoise(zeropoint, radiusaperture,pixelscale,skybrightness,time):
    """Return the sky noise. The product of number of pixel, integration time, and sky brightness."""
    n = npixel(pixelscale, radiusaperture)
    fsky = fluxsky(zeropoint, pixelscale, skybrightness)
    skyn = fsky * time * n
    return skyn



def calcsnr(zeropoint, magnitude, pixelscale, skybrightness, 
        radiusaperture, time, readnoise, gain,darkcurrent):
    """Given the exposure time calculate the SNR. Needs the zeropoint (e-/sec), magnitude,
    pixel scale (arsec/pixel), sky brightness (mag/arcsec^2), radius aperture (arcsec),
    time in seconds, readnoise (e-/pix), Gain (e-/adu), darkcurrent (e-/pix/sec).
    Given this in that unit and that in that unit
    """
    n = npixel(pixelscale, radiusaperture)
    signal = flux(zeropoint, magnitude) * time
    skyn = skynoise(zeropoint, radiusaperture,pixelscale,skybrightness,time)
    rn = readnoise**2+(gain/2.0)**2 * n
    dn = darkcurrent*n*time
    snr = signal/ (signal + rn + dn)**(1/2.)
    return snr

def calctime(zeropoint, magnitude, pixelscale, skybrightness, radiusaperture, snr , readnoise, gain,darkcurrent):
    """Calculate the exposure time needed given the SNR. It uses sympy to find the solution of the function calcsnr() defined above. There are probable better ways ..."""
    tt = Symbol('t')
    n = npixel(pixelscale, radiusaperture)
    signal = flux(zeropoint, magnitude) * tt
    skyn = skynoise(zeropoint, radiusaperture,pixelscale,skybrightness,tt)
    rn = readnoise**2+(gain/2.0)**2 * n
    dn = darkcurrent*n*tt
    s = signal/ (signal + rn + dn)**(1/2.)
    sol = solve(Eq(s,snr),tt)
    return sol[0] 



def snrarray(zeropoint, magnitude, pixelscale, skybrightness, radiusaperture,readnoise, gain,darkcurrent):
    """Creates an array of time and calculates the SNR. Use this to create a plot SNR vs exposure time"""
    upperlimit = 200
    tarray = np.arange(0,upperlimit)
    sarray = [ calcsnr(zeropoint, magnitude, pixelscale, skybrightness, radiusaperture, i, readnoise, gain,darkcurrent) for i in tarray ]
    return tarray,sarray


def bplot(x,y):
    """From a 2D array it returns the Bokeh <script> that contains the data for your plot, together with an accompanying <div> tag that the plot view is loaded into. These tags can be used in HTML documents"""

    #Define data
    Span(location=0, dimension='height', line_color='red', line_width=3)
    x = np.array(x)
    y = np.array(y)
    source = ColumnDataSource(data=dict(x=x,y=y))
    plot = figure(sizing_mode='scale_width',plot_width=1000, plot_height=500, title="SNR vs Integration Time",toolbar_location="above")
    plot.xaxis.axis_label = 'Time (s)'
    plot.yaxis.axis_label = 'SNR'
    plot.line('x','y',source=source, line_width=2.)
   
    
    #JS
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()
    script, div = components(plot)
    
    return script, div, js_resources, css_resources
