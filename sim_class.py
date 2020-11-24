#=============================================================================
import os, sys, time, shutil, subprocess
#=============================================================================
sys.path.insert(1,os.getcwd()+'/src/tables/')

from cheb import save_cheb
#=============================================================================
class Sim:
#=============================================================================
   def __init__(self,args):
      self.data_dir= '/mnt/grtheory/jripley-data'
      self.home_dir= str(os.getcwd())
      assert len(args) > 1, (
         'argv[1] is empty-meed a run_type to run!'
      )	
      self.run_type = args[1]
      if (len(args)>2 and args[2]=='debug'):
         self.debug=True
      else:
         self.debug=False
#=============================================================================
   def set_derived_params(self):
      self.dx= float(
         self.compactification_length/(self.nx-1)
      )
      self.dt= float(
         self.cfl*self.dx
      )
      self.nt= int(
         self.bh_mass*self.evolve_time/self.dt
      )
      self.t_step_save= int(
         self.nt/float(self.num_saved_times)
      )	
      self.initial_exc_i= 0
      if (self.initial_data_type.endswith('bh')):
         self.initial_exc_i= int(
            (
               (2.0*self.excision_ratio*self.bh_mass)
            /  (1+(2.0*self.excision_ratio*self.bh_mass/self.compactification_length))
            )/self.dx
         )
      if (self.t_step_save==0):
         self.t_step_save= 1
#-----------------------------------------------------------------------------
### memory to give each run (for slurm script)
      self.memory= '12' ### MB 
      if (self.nx>(pow(2,10)+1)):
         self.memory= '14' 
      if (self.nx>(pow(2,11)+1)):
         self.memory= '16' 
      if (self.nx>(pow(2,12)+1)):
         self.memory= '18' 
      if (self.nx>(pow(2,13)+1)):
         self.memory= '20' 
#=============================================================================
   def write_sim_params(self):
      with open(self.output_dir+'/sim_params.txt','w') as f:
         attrs= vars(self)
         for param in attrs:
            f.write('{} {}\n'.format(param,attrs[param]))	
#=============================================================================
   def make_output_dir(self):
      self.output_dir= str(
         self.data_dir+'/'
      +  '_'.join('_'.join(time.asctime().split(' ')).split(':'))
      +  '_nx_'+str(self.nx)
      )
      os.makedirs(self.output_dir)
      os.makedirs(self.output_dir+'/cheb_tables')
#=============================================================================
   def make_output_file(self):
      self.output_file= self.output_dir+'/'+'output.out'
      with open(self.output_file, 'w') as f:
         pass
#=============================================================================
   def write_slurm_script(self):
      with open('{}/run.slurm'.format(self.home_dir), 'w') as f:
         f.write('#!/bin/sh\n')
         f.write('#SBATCH -N 1\t\t# nodes=1\n')
         f.write('#SBATCH --ntasks-per-node=1\t\t# ppn=1\n')
         f.write('#SBATCH -J {}\t\t# job name\n'.format('gbs'))
         f.write('#SBATCH -t {}\t\t# walltime (dd:hh:mm:ss)\n'.format(self.walltime))
         f.write('#SBATCH -p dept\t\t# partition/queue name\n')
         f.write('#SBATCH --mem={}MB\t\t# memory in MB\n'.format(self.memory))
         f.write('#SBATCH --output={}\t\t# file for STDOUT\n'.format(self.output_file))
         f.write('#SBATCH --mail-user=jripley@princeton.edu\t\t# Mail  id of the user\n')
         f.write('\n./bin/run {}\n\n'.format(self.output_dir))

         shutil.copyfile(
            '{}/run.slurm'.format(self.home_dir),
            '{}/run.slurm'.format(self.output_dir)
         )
#=============================================================================
   def init_record(self,gbc2_range):
      self.record= (
         self.data_dir
      +	'/record_amp_'+str(self.amp)
      +	'_nx_'+str(self.nx)
      +	'.txt'
      )
      with open(self.record,'w') as rec:
         rec.write('nx ' +str(self.nx)+'\n')
         rec.write('initial_data_type '+str(self.initial_data_type)+'\n')
         rec.write('amp '+str(self.amp)+'\n')
         rec.write('r_l '+str(self.r_l)+'\n')
         rec.write('r_u '+str(self.r_u)+'\n')
         rec.write('bh_mass '+str(self.bh_mass)+'\n')	
         rec.write('gbc2 initial range '+str(gbc2_range)+'\n')	
#=============================================================================
   def write_gbc2_to_record(self,result):
      with open(self.record,'a') as rec:
         rec.write('gbc2 '+str(self.gbc2)+' '+str(result)+'\n')
#=============================================================================
   def delete_output_dir(self):
      subprocess.call('rm -rf '+self.output_dir, shell='True')
#=============================================================================
   def search_for_elliptic(self,gbc2_range):
      try:
         os.makedirs(self.data_dir)
      except FileExistsError:
         pass
      self.init_record(gbc2_range)
      first_time= True
# put some condition here
#      while ((gbc2_range[1]-gbc2_range[0])/(gbc2_range[1]+gbc2_range[0])>1e-3): 
#
#         self.launch()
#
#         done= False
#         while not done:
#            time.sleep(10)
#            with open(self.output_dir+'/output.out','r') as f:
#               for line in f:
#                  if line.startswith('naked_elliptic_region'):
#                     gbc2_range[1]= self.gbc2
#                     done= True
#                     self.write_gbc2_to_record('naked_elliptic_region')
#                  if line.startswith('run_finished_successfully'):
#                     gbc2_range[0]= self.gbc2
#                     done= True	
#                     self.write_gbc2_to_record('run_finished_successfully')
#=============================================================================
   def launch(self):
      self.set_derived_params()
      self.make_output_dir()
      self.make_output_file()
      self.write_sim_params()
      self.write_slurm_script()

#      save_cheb(self.output_dir+'/cheb_tables',self.nx)

      subprocess.call('\n./bin/default.run {} > {}/output.out'.format(self.output_dir,self.output_dir), shell=True)
#      subprocess.call('sbatch run.slurm', shell='True')		
