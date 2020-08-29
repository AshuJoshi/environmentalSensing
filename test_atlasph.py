import sys
sys.path.append('./atlasph')

import atlasph.ezophi2c as ezophi2c

while True:
    atlasph = ezophi2c.get_ezo_ph()
    atlasph = float(atlasph.rstrip('\x00'))
    print(atlasph)
    
    