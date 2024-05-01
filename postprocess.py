
import os
import subprocess
import shutil
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
    
def run_command(command):
  # Get the directory of the current script
  script_dir = os.path.dirname(os.path.realpath(__file__))
  print(script_dir)
  os.chdir(script_dir)
  subprocess.call(command, shell=True)
  
  
script_dir = os.path.dirname(os.path.realpath(__file__))
scount=8
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
