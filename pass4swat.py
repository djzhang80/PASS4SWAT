import subprocess
import os
import shutil
import sys
def run_command(command):
  # Get the directory of the current script
  script_dir = os.path.dirname(os.path.realpath(__file__))
  print(script_dir)
  os.chdir(script_dir)
  subprocess.call(command, shell=True)

def get_simulation_number(filename):
  try:
    with open(filename, 'r') as file:
      lines = file.readlines()
      if len(lines) >= 2:
        # Split the second line by colon and convert the first token to a number
        try:
          number_string, *_ = lines[1].strip().split(':')
          return int(number_string)
        except ValueError:
          print(f"Error: Second line value '{number_string}' is not a valid number.")
          return None
      else:
        print(f"Error: File '{filename}' has less than two lines.")
        return None
  except FileNotFoundError:
    print(f"Error: File '{filename}' not found.")
    return None

def update_trk_file(filename, content):
  try:
    # Open the file in append mode (creates if not existing)
    with open(filename, 'a') as file:
      # Clear the file content if it already exists
      file.truncate(0)
      # Write the provided content to the file
      file.write(content)
      print(f"File '{filename}' recreated (if necessary) and content written successfully.")
  except FileNotFoundError:
    print(f"Error: Failed to create file '{filename}'.")
    
    
def replace_in_file(filepath, **kwargs):
  try:
        # Open the file in read mode
    with open(filepath, 'r') as file:
      # Read the entire file content
      file_content = file.read()

    # Replace occurrences of old content with new content
    for key, value in kwargs.items():
      file_content = file_content.replace(key, value)

    # Open the file again in write mode (truncates existing content)
    filepath=filepath.replace(".tpl","");
    with open(filepath, 'w') as file:
      # Write the modified content to the file
      file.write(file_content)
      print(f"Content replaced in '{filepath}'.")

  except FileNotFoundError:
    print(f"Error: File '{filepath}' not found.")

##preprocessing tasks
###you project path should change according to the same pattern gievn at next line, where d is your dirver name, if you put you directory in c driver change it to c

if len(sys.argv) < 2:
  print(f"Usage: pass4sway.py <paralle_count>")
  exit(1)

pcount=sys.argv[1]

script_dir = os.path.dirname(os.path.realpath(__file__))

project_path="/run/desktop/mnt/host/"+script_dir.replace("\\","/").replace(":","").lower();

replace_in_file(script_dir+"/rabbitmq-initializer.yaml.tpl",path_to_your_project=project_path)

run_command("SUFI2_LH_sample.exe < SUFI2.IN/response_to_SUFI2_LH_sample.txt")
scount = get_simulation_number(script_dir+"/SUFI2.IN/par_inf.txt")

arguments = {'path_to_your_project': project_path, 'scount': str(scount), 'pcount': str(pcount),'mount_path_in_container':'/model','execution_script':'/model/model_simulation.sh','execution_image':'jannyarj/base:1.0'}
replace_in_file(script_dir+"/model-paralllel-simulation-job.yaml.tpl",**arguments)


for i in range(1, scount+1):
  update_trk_file(script_dir+"/SUFI2.IN/trk.txt", str(i))
  run_command("SUFI2_make_input.exe")
  shutil.copy2(script_dir+"/model.in", script_dir+"/parameter/model.in."+str(i))
  
  
##parallel simulations
'''
run_command("kubectl --force=true delete pods queue-initializer")
run_command("kubectl --force=true delete jobs job-swat")
run_command("kubectl --force=true delete services rabbitmq-service")
run_command("kubectl --force=true delete replicationcontrollers rabbitmq-controller")
'''
run_command("kubectl delete all --all --force=true --wait")

run_command("kubectl create -f "+script_dir+"/rabbitmq-controller.yaml")
run_command("kubectl create -f "+script_dir+"/rabbitmq-service.yaml")
run_command("kubectl create -f "+script_dir+"/rabbitmq-initializer.yaml")
#run_command("kubectl create -f "+script_dir+"/test.yaml")
run_command("kubectl create -f "+script_dir+"/model-paralllel-simulation-job.yaml")

#run_command("kubectl wait --for=condition=complete --timeout=30000s job/job-swat")

##postprocessing
try:
    os.remove(script_dir+"/output.rch")
    print("delete file successfully!")
except OSError as error:
    print(f"Error deleting file: {error}")
    

for i in range(1,scount+1):
    try:
      os.remove(script_dir+"/output.rch")
    except OSError as error:
      print(f"Error deleting file: {error}")
    os.link(script_dir+"/output.rch.model.in."+str(i),script_dir+"/output.rch")
    update_trk_file(script_dir+"/SUFI2.IN/trk.txt", str(i))
    run_command("SUFI2_extract_rch.exe")

run_command("SUFI2_Post.bat")

###warning: change your project name to sufi2.Sufi2.SwatCup if you want to open in swat-cup

  







