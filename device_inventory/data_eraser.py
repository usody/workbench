#!/usr/bin/env python
import subprocess
import os
import sys
try:
    import ConfigParser as configparser  # Python2
except ImportError:
    import configparser

def load_config():
    # https://docs.python.org/3.4/library/configparser.html
    path = os.path.dirname(__file__)
    config_file = os.path.join(path, 'config.ini')
    assert os.path.exists(config_file), config_file

    config = configparser.ConfigParser()
    config.read(config_file)  # donator.cfg merged here
    
    #print(config['DEFAULT']['DISC'])
    #print(config['DEFAULT'].getboolean('DISC'))
    #print(config['donator']['email'])
    
    # TODO set fallback values if config is empty
    # https://docs.python.org/3.4/library/configparser.html#fallback-values
    
    return config

def get_hdinfo(path,value):
    return subprocess.Popen(["lsblk",path,"--nodeps","-no",value], stdout=subprocess.PIPE)

def get_user_input(sdx_path):
    size = get_hdinfo(sdx_path,"size").stdout.read()
    model = get_hdinfo(sdx_path,"model").stdout.read()
    print "Erasing %s (Model: %s) (Size: %s)" % (sdx_path,model.rstrip(" \n"),size.rstrip(" \n"))
    config_erase = raw_input("Are you sure to erase \"{0}\"? [y/N] ".format(sdx_path))
    return config_erase

def erasetor(dev):
    #erasuring with 0 bits all the harddrive
    #subprocess.call(["shred","-zvn","o",dev"])
    subprocess.call(["ls",dev])

def do_erasure(sdx):
    config = load_config()
    erase = config.get('DEFAULT', 'ERASE')

    if erase == "yes":
        print erasetor(sdx)
    elif erase == "ask":
        erase = get_user_input(sdx)
        if erase.lower().strip() == "y" or erase.lower().strip() == "yes":
            print erasetor(sdx)

def main(argv=None):
    device = sys.argv[1]
    do_erasure(device)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
