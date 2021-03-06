from physics   import Enthalpy, Density, FullDensity, Velocity, Age
from plot      import Plot
from termcolor import colored, cprint
from pylab     import plt, linspace, ones, hstack


class TransientSolver(object):
  """
  """
  def __init__(self, firn, config):
    """
    """
    self.firn   = firn
    self.config = config
    
    # form the physics :
    self.fe = Enthalpy(firn, config)
    self.fv = Velocity(firn, config)
    self.fd = FullDensity(firn, config)
    if config['age']['on']:
      self.fa = Age(firn, config)

    if config['plot']['on']:
      #plt.ion()
      self.plot = Plot(firn, config)
      #plt.show()

  def solve(self):
    """
    """
    s    = '::: solving TransientSolver :::'
    text = colored(s, 'blue')
    print text
    
    firn   = self.firn
    config = self.config

    fe     = self.fe
    fv     = self.fv
    fd     = self.fd
    if config['age']['on']:
      fa     = self.fa
    
    t0      = config['t_start']
    tm      = config['t_mid']
    tf      = config['t_end']
    dt      = config['time_step']
    dt_list = config['dt_list']
    if dt_list != None:
      numt1   = (tm-t0)/dt_list[0] + 1       # number of time steps
      numt2   = (tf-tm)/dt_list[1] + 1       # number of time steps
      times1  = linspace(t0,tm,numt1)   # array of times to evaluate in seconds
      times2  = linspace(tm,tf,numt2)   # array of times to evaluate in seconds
      dt1     = dt_list[0] * ones(len(times1))
      dt2     = dt_list[1] * ones(len(times2))
      times   = hstack((times1,times2))
      dts     = hstack((dt1, dt2))
    
    else: 
      numt   = (tf-t0)/dt + 1         # number of time steps
      times  = linspace(t0,tf,numt)   # array of times to evaluate in seconds
      dts    = dt * ones(len(times))
      firn.t = t0
   
    self.times = times
    self.dts   = dts

    for t,dt in zip(times[1:], dts[1:]):
      
      # update timestep :
      firn.dt = dt
      firn.dt_v.assign(dt)

      # update boundary conditions :
      firn.update_Hbc()
      firn.update_rhoBc()
      firn.update_wBc()
      #firn.update_omegaBc()
    
      # newton's iterative method :
      fe.solve()
      fd.solve()
      fv.solve()
      if config['age']['on']:
        fa.solve()
      
      # update firn object :
      firn.update_vars(t)
      firn.update_height_history()
      if config['free_surface']['on']:
        if dt_list != None:
          if t > tm+dt:
            firn.update_height()
        else:
          firn.update_height()
      
      # update model parameters :
      if t != times[-1]:
         firn.H_1.assign(firn.H)
         firn.U_1.assign(firn.U)
         firn.omega_1.assign(firn.omega)
         firn.w_1.assign(firn.w)
         firn.a_1.assign(firn.a)
         firn.m_1.assign(firn.m)
    
      # update the plotting parameters :
      if config['plot']['on']:
        self.plot.update_plot()
        #plt.draw()
        
      s = '>>> Time: %i yr <<<'
      text = colored(s, 'red', attrs=['bold'])
      print text % (t / firn.spy)
    
    if config['plot']['on']:
      pass
      #plt.ioff()
      #plt.show()



