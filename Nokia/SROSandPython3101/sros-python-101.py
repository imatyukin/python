#!./venv/bin/python3

## Import the external libraries required
import argparse
from ncclient import manager
from ncclient.xml_ import *

## create_connection
# In: Hostname and Commandline arguments
# Out: NCClient Connection
def create_connection(host, args):
  conn = manager.connect(host=host,
                           port=args.port,
                           username=args.username,
                           password=args.password,
                           hostkey_verify=False,
                           device_params={'name':'alu'})
  return conn

## read_file
# In: filename
# Out: List containing all non-blank lines from filename
def read_file(filename):
  f = open(filename, 'r')
  output = f.read().splitlines()
  output = [ line for line in output if line ]
  f.close()
  return output

## write_file
# In: filename and contents to be written to the file
# Out: Nothing (returns 0 on completion)
def write_file(filename, contents):
  f = open(filename, 'w+')
  f.write(contents)
  f.close()
  return 0

## get_arguments
# In: Nothing
# Out: The command line arguments
def get_arguments():
  parser = argparse.ArgumentParser()
  parser.add_argument("-i", "--inventory", help="Inventory Filename", required=True)
  parser.add_argument("-u", "--username", help="NETCONF SSH Username", required=False, default='admin')
  parser.add_argument("-w", "--password", help="NETCONF SSH Password", required=False, default='admin')
  parser.add_argument("-p", "--port", help="NETCONF TCP Port", required=False, default=830)
  args = parser.parse_args()
  return args

### The main procedure.  This is a springboard for the individual functions that
### are to be performed
def main():
  ## Get the commandline arguments
  args = get_arguments()
  try:
    ## Read in the inventory filename provided on the command line and receive a list
    ## of hosts within it
    inventory = read_file(args.inventory)
  except Exception as error:
    print(error)
  ## For every host in the inventory file perform these actions
  for host in inventory:
    try:
      ## Create a NETCONF connection to the host
      conn = create_connection(host, args)
      ## Issue the get-config RPC over our NETCONF connection and receive the running config
      config = conn.get_config(source='running')
      ## Close the NETCONF connection with the host
      conn.close_session()
      try:
        ## Write the obtained running configuration (from the data/configure xpath) to a file
        write_file(host, to_xml(config.xpath('data/configure')[0]))
      except Exception as error:
        print(error)
      ## Provide an on-screen prompt that the program has processed this host
      print('Processed',host)
    except Exception as error:
      print(host,'Error',error)

### Start here.  If called directly from the command line then run the main procedure
if __name__ == "__main__":
  main()