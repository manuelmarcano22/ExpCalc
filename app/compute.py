import math
import numpy as np
from sympy import Eq, solve, Symbol
#Bokeh
from bokeh.resources import CDN, INLINE
from bokeh.plotting import figure
from bokeh.embed import autoload_static, components
from bokeh.models import  ColumnDataSource

def sin(x):
    return math.sin(x)




def flux(zeropoint, magnitude):
    """Return the expected count rate for an object of magnitude m in electron per second.
    Need to specify the zeropoint to use. We assume a normalized to a 20 magnitude star. """
    normalizationmag = 20.0
    f = zeropoint*10**(0.4*(normalizationmag-magnitude))
    return f

def fluxsky(zeropoint, pixelscale, skybrightness):
    """Return the sky background in electrons/sec/pix. I needs the skybrightness in mag/arcsec^2, the pixelscale of the CCD in arcsec/pixel and the zeropoint (filter) to calculate the flux."""
    magnitudepixel = skybrightness - 2.5*np.log10(pixelscale**2)
    fsky = flux(zeropoint,magnitudepixel)
    return fsky


def npixel(pixelscale, radiusaperture):
    """Return the number of pixel given the pixel scale in arcsec/pixel and photometric radius of aperture given in arcseconds. """
    npixel = (np.pi * radiusaperture**2)/(pixelscale**2)
    return npixel

def skynoise(zeropoint, radiusaperture,pixelscale,skybrightness,time):
    n = npixel(pixelscale, radiusaperture)
    fsky = fluxsky(zeropoint, pixelscale, skybrightness)
    skyn = fsky * time * n
    return skyn



def calcsnr(zeropoint, magnitude, pixelscale, skybrightness, 
        radiusaperture, time, readnoise, gain,darkcurrent):
    """Given the exposure time calculate the SNR. 
    Given this in that unit and that in that unit
    """
    n = npixel(pixelscale, radiusaperture)
    signal = flux(zeropoint, magnitude) * time
    skyn = skynoise(zeropoint, radiusaperture,pixelscale,skybrightness,time)
    rn = readnoise**2+(gain/2.0)**2 * n
    dn = darkcurrent*n*time
    snr = signal/ (signal + rn + dn)**(1/2.)
    return snr


def exposuret(zeropoint, magnitude, pixelscale, skybrightness, 
                radiusaperture, snr, readnoise, gain,darkcurrent):
    """Calculate the exposure time needed given the SNR. """
    n = npixel(pixelscale, radiusaperture)
    fsky = fluxsky(zeropoint, pixelscale, skybrightness)
    f = flux(zeropoint, magnitude)
    p1 = (f+(darkcurrent+fsky)*n)*snr**2  
    p2 = f**2*(gain**2*n+4*readnoise**2)*snr**2
    p3 = (f+(darkcurrent+fsky)*n)**2 * snr**4

    t = (p1 +  np.sqrt(p2 + p3) )/(2*f**2)

    return t

def calctime(zeropoint, magnitude, pixelscale, skybrightness, radiusaperture, snr , readnoise, gain,darkcurrent):
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
    tarray = np.arange(0,1000)
    sarray = [ calcsnr(zeropoint, magnitude, pixelscale, skybrightness, radiusaperture, i, readnoise, gain,darkcurrent) for i in tarray ]
    return tarray,sarray

#a,b = snrarray(zeropoint, magnitude, pixelscale, skybrightness, radiusaperture, readnoise, gain,darkcurrent)


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
