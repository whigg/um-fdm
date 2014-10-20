#    Copyright (C) <2012>  <cummings.evan@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
enthPlot.py
Evan Cummings
07.09.12

Plotting for enthalby Firn Densification Model.

"""
from pylab import *
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['legend.fontsize'] = 'medium'
    
class FixedOrderFormatter(ScalarFormatter):
  """
  Formats axis ticks using scientific notation with a constant order of 
  magnitude
  """
  def __init__(self, order_of_mag=0, useOffset=True, useMathText=False):
    self._order_of_mag = order_of_mag
    ScalarFormatter.__init__(self, useOffset=useOffset, 
                             useMathText=useMathText)
  def _set_orderOfMagnitude(self, range):
    """
    Over-riding this to avoid having orderOfMagnitude reset elsewhere
    """
    self.orderOfMagnitude = self._order_of_mag


class Plot():
  """
  Plotting class handles all things related to plotting.
  """
  def __init__(self, firn, zMin, zMax, rhoMax, wMin, wMax, aMax, omegaMax):
    """
    Initialize plots with firn object as input.
    """   
    self.spy  = firn.spy
    Tw        = firn.Tw
    self.firn = firn
     
    # x-values :
    T      = firn.Tp
    omega  = firn.omegap
    rho    = firn.rhop
    w      = firn.wp * self.spy * 1e2 # cm/a
    a      = firn.ap /self.spy
    Ts     = firn.Ts - 273.15
    rhos   = rho[-1]
    adot   = firn.w_S.adot

    # y-value :
    z      = firn.z
    zs     = z[-1]
    zb     = z[0]
    
    # original surface height :
    zo     = firn.zo

    #zmax   = zs + (zs - zb) / 5                   # max z-coord
    zmax   = zMax
    zmin   = zMin                                 # min z-coord

    Tmin   = firn.Tavg - Tw - 20                  # T x-coord min
    Tmax   = firn.Tavg - Tw + 20                  # T x-coord max
    Th     = Tmin + 0.1*(Tmax - Tmin) / 2         # T height x-coord
    Tz     = zmax - 0.15*(zmax - zmin) / 2        # z-coord of Ts

    Omin   = 0.0
    Omax   = omegaMax

    rhoMin = 0.0                                  # rho x-coord min
    #rhoMax = 1000                                 # rho x-coord max
    rhoh   = rhoMin + 0.1*(rhoMax - rhoMin) / 2  # rho height x-coord
    
    #wMin   = -200
    #wMax   = 200
    wh     = wMin + 0.1*(wMax - wMin) / 2

    aMin   = 0.0
    #aMax   = 2007.0
    #kh     = kMin + 0.1*(kMax - kMin) / 2

    self.fig   = figure(figsize=(19,6))
    self.Tax   = self.fig.add_subplot(151)
    self.Oax   = self.fig.add_subplot(152)
    self.rhoax = self.fig.add_subplot(153)
    self.wax   = self.fig.add_subplot(154)
    self.aax   = self.fig.add_subplot(155)

    # format : [xmin, xmax, ymin, ymax]
    self.Tax.axis([Tmin, Tmax, zmin, zmax])
    self.Tax.grid()
    self.Oax.axis([Omin, Omax, zmin, zmax])
    self.Oax.grid()
    self.rhoax.axis([rhoMin, rhoMax, zmin, zmax])
    self.rhoax.grid()
    self.rhoax.xaxis.set_major_formatter(FixedOrderFormatter(2))
    self.wax.axis([wMin, wMax, zmin, zmax])
    self.wax.grid()
    self.aax.axis([aMin, aMax, zmin, zmax])
    #self.aax.xaxis.set_major_formatter(FixedOrderFormatter(3))
    self.aax.grid()

    # plots :
    self.Tsurf    = self.Tax.text(Th, Tz, r'$T_S$: %.1E $\degree$C' % Ts)
    self.phT,     = self.Tax.plot(T - 273.15, z, '0.3', lw=1.5,
                                  drawstyle='steps-post')
    self.phTs,    = self.Tax.plot([Tmin, Tmax], [zs, zs], 'k-', lw=3)
    self.phTs_0,  = self.Tax.plot(Th, zo, 'ko')
    self.phTs_dot,= self.Tax.plot(Ts, zs, 'ro')
    self.phTsp,   = self.Tax.plot(Th*ones(len(z)), z, 'r+')
    
    self.phO,     = self.Oax.plot(omega, z, '0.3', lw=1.5,
                                  drawstyle='steps-post')
    self.phOS,    = self.Oax.plot([Omin, Omax], [zs, zs], 'k-', lw=3)
    self.phOS_dot,= self.Oax.plot(omega[-1], zs, 'ro')
    
    self.rhoSurf  = self.rhoax.text(rhoh, Tz, r'$\dot{a}$: %.1E i.e.$\frac{\mathrm{m}}{\mathrm{a}}$' % adot)
    self.phrho,   = self.rhoax.plot(rho, z, '0.3', lw=1.5,
                                    drawstyle='steps-post')
    self.phrhoS,  = self.rhoax.plot([rhoMin, rhoMax], [zs, zs], 'k-', lw=3)
    self.phrhoS_dot, = self.rhoax.plot(rho[-1], zs, 'ro')
    #self.phrhoS_0,= self.rhoax.plot(rhoh, zo, 'ko')
    #self.phrhoSp, = self.rhoax.plot(rhoh*ones(len(z)), z, 'r+')

    self.wSurf    = self.wax.text(wh, Tz, r'$\rho_S$: %.1E $\frac{\mathrm{kg}}{\mathrm{m}^3}$' % rhos)
    self.phw,     = self.wax.plot(w, z, '0.3', lw=1.5,
                                  drawstyle='steps-post')
    self.phwS,    = self.wax.plot([wMin, wMax], [zs, zs], 'k-', lw=3)
    self.wS_dot,  = self.wax.plot(w[-1], zs, 'ro')
    #self.phws_0,  = self.wax.plot(wh, zo, 'ko')
    #self.phwsp,   = self.wax.plot(wh*ones(len(z)), z, 'r+')
    
    self.pha,     = self.aax.plot(a, z, '0.3', lw=1.5,
                                  drawstyle='steps-post')
    self.phaS,    = self.aax.plot([aMin, aMax], [zs, zs], 'k-', lw=3)
    #self.phks_0,  = self.kax.plot(kh, zo, 'ko')
    #self.phksp,   = self.kax.plot(kh*ones(len(z)), z, 'r+')

    # formatting :
    self.fig.canvas.set_window_title('Time = 0.0 yr')

    self.Tax.set_title('Temperature')
    self.Tax.set_xlabel(r'$T\ [\degree \mathrm{C}]$')
    self.Tax.set_ylabel('Depth [m]')

    self.Oax.set_title('Water Content')
    self.Oax.set_xlabel(r'$\omega\ [\%]$')

    self.rhoax.set_title('Density')
    self.rhoax.set_xlabel(r'$\rho\ \left[\frac{\mathrm{kg}}{\mathrm{m}^3}\right]$')
    
    self.wax.set_title('Velocity')
    self.wax.set_xlabel(r'$w\ \left[\frac{\mathrm{cm}}{\mathrm{a}}\right]$')

    self.aax.set_title('Age')
    self.aax.set_xlabel(r'$a\ [\mathrm{a}]$')
    tight_layout()
    

  def update_plot(self):
    """
    Update the plot for each time step at time t.
    """
    firn  = self.firn
    index = firn.index 
    T     = firn.Tp
    omega = firn.omegap
    Tw    = firn.Tw
    rho   = firn.rhop
    w     = firn.wp * self.spy * 1e2
    a     = firn.ap / self.spy
    z     = firn.z
    zo    = firn.zo
    Ts    = firn.Ts - Tw
    t     = firn.t / self.spy

    self.fig.canvas.set_window_title('Time = %.2f yr' % t)
    
    self.Tsurf.set_text(r'$T_S$: %.1E $\degree$C' % Ts)
    self.phT.set_xdata(T - Tw)
    self.phT.set_ydata(z)
    self.phTs.set_ydata(z[-1])
    self.phTs_0.set_ydata(zo)
    self.phTsp.set_ydata(z)
    self.phTs_dot.set_xdata(Ts)
    self.phTs_dot.set_ydata(z[-1])
    
    self.phO.set_xdata(omega)
    self.phO.set_ydata(z)
    self.phOS.set_ydata(z[-1])
    self.phOS_dot.set_xdata(omega[-1])
    self.phOS_dot.set_ydata(z[-1])
    
    self.rhoSurf.set_text(r'$\rho_S$: %.1E $\frac{\mathrm{kg}}{\mathrm{m}^3}$' % rho[-1])
    self.phrho.set_xdata(rho)
    self.phrho.set_ydata(z)
    self.phrhoS.set_ydata(z[-1])
    self.phrhoS_dot.set_xdata(rho[-1])
    self.phrhoS_dot.set_ydata(z[-1])
    
    self.wSurf.set_text(r'$\dot{a}$: %.1E i.e.$\frac{\mathrm{m}}{\mathrm{a}}$' % firn.w_S.adot)
    self.phw.set_xdata(w)
    self.phw.set_ydata(z)
    self.phwS.set_ydata(z[-1])
    self.wS_dot.set_xdata(w[-1])
    self.wS_dot.set_ydata(z[-1])
   
    self.pha.set_xdata(a)
    self.pha.set_ydata(z)
    self.phaS.set_ydata(z[-1])
    

  def plot_all(self, firns, titles, colors):
    """
    Plot the data from a list of firn objects with corresponding titles and
    colors array.
    """    
    Tmin   = -20                                 # T x-coord min
    Tmax   = 0                                   # T x-coord max
    Th     = Tmin + 0.1*(Tmax - Tmin) / 2        # T height x-coord

    rhoMin = 300                                 # rho x-coord min
    rhoMax = 1000                                # rho x-coord max
    rhoh   = rhoMin + 0.1*(rhoMax - rhoMin) / 2  # rho height x-coord

    wMin   = -22.0e-6
    wMax   = -7.5e-6
    wh     = wMin + 0.1*(wMax - wMin) / 2

    kMin   = 0.0
    kMax   = 2.2
    kh     = kMin + 0.1*(kMax - kMin) / 2
    
    zmax   = firns[0].zs + 20                    # max z-coord
    zmin   = firns[0].zb                         # min z-coord

    fig    = figure(figsize=(16,6))
    Tax    = fig.add_subplot(141)
    rhoax  = fig.add_subplot(142)
    wax    = fig.add_subplot(143)
    kax    = fig.add_subplot(144)

    # format : [xmin, xmax, ymin, ymax]
    Tax.axis([Tmin, Tmax, zmin, zmax])
    Tax.grid()
    rhoax.axis([rhoMin, rhoMax, zmin, zmax])
    rhoax.grid()
    rhoax.xaxis.set_major_formatter(FixedOrderFormatter(2))
    wax.axis([wMin, wMax, zmin, zmax])
    wax.grid()
    wax.xaxis.set_major_formatter(FixedOrderFormatter(-6))
    kax.axis([kMin, kMax, zmin, zmax])
    kax.grid()

    # plots :
    for firn, title, color in zip(firns, titles, colors):
      i = firn.index
      Tax.plot(firn.T[i] - 273.15, firn.z[i], color, label=title, lw=2)
      Tax.plot([Tmin, Tmax], [firn.z[i][-1], firn.z[i][-1]], color, lw=2)

      rhoax.plot(firn.rho[i], firn.z[i], color, lw=2)
      rhoax.plot([rhoMin, rhoMax], [firn.z[i][-1], firn.z[i][-1]], color, lw=2)

      wax.plot(firn.w[i], firn.z[i], color, lw=2)
      wax.plot([wMin, wMax], [firn.z[i][-1], firn.z[i][-1]], color, lw=2)

      kax.plot(firn.k2[i], firn.z[i], color, lw=2)
      kax.plot([kMin, kMax], [firn.z[i][-1], firn.z[i][-1]], color, lw=2)
    
    # formatting :
    fig_text = figtext(.85,.95,'Time = 0.0 yr')

    Tax.set_title('Temperature')
    Tax.set_xlabel(r'$T$ $[\degree C]$')
    Tax.set_ylabel(r'Depth $[m]$')

    rhoax.set_title('Density')
    rhoax.set_xlabel(r'$\rho$ $\left [\frac{kg}{m^3}\right ]$')
    #rhoax.set_ylabel(r'Depth $[m]$')

    wax.set_title('Velocity')
    wax.set_xlabel(r'$w$ $\left [\frac{mm}{s}\right ]$')
    #wax.set_ylabel(r'Depth $[m]$')

    kax.set_title('Thermal Conductivity')
    kax.set_xlabel(r'$k$ $\left [\frac{J}{m K s} \right ]$')
    #kax.set_ylabel(r'Depth $[m]$')
    
    # Legend formatting:
    leg    = Tax.legend(loc='upper right')
    ltext  = leg.get_texts()
    frame  = leg.get_frame()
    setp(ltext, fontsize='small')
    frame.set_alpha(0)

    show()


  def plot_height(self, x, ht, origHt):
    """
    Plot the height history of a column of firn for times x, current height ht, 
    and original surface height origHt.
    """
    x /= self.spy

    # plot the surface height information :
    plot(x,               ht,     'k-',  lw=1.5, label=r'Surface Height')
    plot(x[:len(origHt)], origHt, 'k--', lw=1.5, label=r'Original Surface')
    xlabel('time [a]')
    ylabel('height [m]')
    title('Surface Height Changes')
    grid()
  
    # Legend formatting:
    leg = legend(loc='lower left')
    ltext  = leg.get_texts()
    frame  = leg.get_frame()
    setp(ltext, fontsize='small')
    frame.set_alpha(0)
    show()


  def plot_all_height(self, xs, hts, origHts, titles, colors):
    """
    Plot the height history of a list of firn objects for times array xs, 
    current height array hts, original surface heights origHts, with 
    corresponding titles and colors arrays.
    """
    zMin = min(min(origHts))
    zMax = max(max(hts))
    zMax = zMax + (zMax - zMin) / 16.0
    xMin = min(min(xs))
    xMax = max(max(xs))
    
    fig = figure(figsize=(11,8))
    ax  = fig.add_subplot(111)
    
    # format : [xmin, xmax, ymin, ymax]
    ax.axis([xMin, xMax, zMin, zMax])
    ax.grid()
    
    # plot the surface height information :
    for x, ht, origHt, title, color in zip(xs, hts, origHts, titles, colors):
      ax.plot(x, ht,     color + '-',  label=title + ' Surface Height')
      ax.plot(x, origHt, color + '--', label=title + ' Original Surface')
    
    ax.set_xlabel('time [a]')
    ax.set_ylabel('height [m]')
    ax.set_title('Surface Height Changes')
    ax.grid()
  
    # Legend formatting:
    leg    = ax.legend(loc='lower left')
    ltext  = leg.get_texts()
    frame  = leg.get_frame()
    setp(ltext, fontsize='small')
    frame.set_alpha(0)
    show()



