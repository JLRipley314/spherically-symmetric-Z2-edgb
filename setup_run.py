import sys, time
from sim_class import Sim
#############################################################################
args= sys.argv
##############################################################################
### input paramters: set these by hand 
##############################################################################
sim= Sim(args)
#-----------------------------------------------------------------------------
sim.compactification_length= float(100) 
#-----------------------------------------------------------------------------
sim.evolve_time=   float(300)  ### in units of initial black hole mass for ze field 
sim.num_saved_times= int(1000)
sim.cfl= 0.25
#-----------------------------------------------------------------------------
### scalar field potentials
#-----------------------------------------------------------------------------
sim.mu= 0.0
sim.la= 0.0

sim.gbc1= 0.0
sim.gbc2= 100.0
#-----------------------------------------------------------------------------
sim.phi_r= 21  ### where measuring phi
#-----------------------------------------------------------------------------
### initial data
#-----------------------------------------------------------------------------
#sim.initial_data_type= str("scalarized_bh")
sim.initial_data_type= str("bump_with_bh")
#sim.initial_data_type= str("bump")
#-----------------------------------------------------------------------------
sim.bh_mass= float(10.0)
#-----------------------------------------------------------------------------
### for the noncompact scalar profile
sim.charge= float(0.004)
#-----------------------------------------------------------------------------
### for the Gaussian-like pulse
sim.amp= float(1.0e-3)
sim.r_l= float(24.0)
sim.r_u= float(32.0)
#-----------------------------------------------------------------------------
sim.nx= pow(2,10)+1 
#-----------------------------------------------------------------------------
sim.set_derived_params()
##############################################################################
### for slurm script
##############################################################################
sim.walltime= '120:00:00' ### (hh:mm:ss)
sim.memory=   '10' ### MB 
##############################################################################
if (sim.run_type == "basic_run"):
	sim.launch()
##############################################################################
elif (sim.run_type == "convergence_test"):
	num_res= int(input("number of resolutions "))
	for i in range(num_res):	
		sim.launch()
		sim.nx= 2*(sim.nx-1)+1 
		time.sleep(5)
###############################################################################
### varying eta with a fixed initial phi amplitude
###############################################################################
elif (sim.run_type == "search_for_elliptic"):
	gbc2_range=[100.0,625.0]

	sim.mu_hat= 0.0
	sim.la_hat= 0.0

	sim.search_for_elliptic(gbc2_range)
##############################################################################
else:
	raise ValueError("run_type = "+str(sim.run_type)) 
