import base64
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np

def set_bit(v, index, x):
    """
        Set the index:th bit of v to 1 if x is truthy,
        else to 0, and return the new value.
    """
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v &= ~mask          # Clear the bit indicated by the mask (if x is False)
    if x:
        v |= mask         # If x was True, set the bit indicated by the mask.
    return v            # Return the result, we're done.

def decode_wave(wave, gain, offset):
    wave = base64.b64decode(wave)
    binwave = []
    # Convert the SmallInt array into Int values
    # pairs of the wave array --> single int value
    for i in range (0,len(wave)-1,2):
        t = (wave[i]) + wave[i+1]*256
        # This is dense: left side CLEARS the 15th bit. Right side
        #    substracts -32768 from the number if that bit was '1'
        #    before it was cleared
        # (t >> 15) grabs the last bit (shifts), leaving 1 or 0
        t = set_bit(t,15,0) + (-32768)*(t >> 15)

        # Adjust by gain & offset then add to bin array
        t = t*gain + offset
        binwave.append(t)
    return binwave

tree = ET.parse('data/696793e068608e7c/18-30-01-000Z.xml')
root = tree.getroot()

data_dict = {}

for meas in root.iter('cpc'):
    time = meas.get('datetime')
    # for assetType in meas.findall("./m[@name='POLLTIME']"):
    #     time = assetType.text
    cur_dict = {}
    for mg in meas.iter('mg'):
        name = mg.get('name')
        cur_dict[name] = {}
        offset = 0
        gain = 0
        hz = 0
        points = 0
        for m in mg.iter('m'):
            if (m.attrib["name"] == 'Offset'):
                offset = int(m.text)
                cur_dict[name]['offset'] = offset
            elif (m.attrib["name"] == 'Gain'):
                # GAIN is not correct in the XML for pressures
                if (mg.get('name') == 'GE_ART'):
                    gain = 0.25
                elif (mg.get('name') == 'INVP1'):
                    gain = 0.01
                else:
                    gain = float(m.text)
                cur_dict[name]['gain'] = gain
            elif (m.attrib["name"] == 'Wave'):
                wave = m.text
            elif (m.attrib["name"] == 'Hz'):
                hz = int(m.text)
                cur_dict[name]['hz'] = hz
            elif (m.attrib["name"] == 'Points'):
                points = int(m.text)
                cur_dict[name]['points'] = points
            cur_dict[name]['wave'] = decode_wave(wave, gain, offset)
            
    data_dict[time] = cur_dict

all_ecg = []
for each_time in data_dict:
    for each_sensor in data_dict[each_time]:
        if 'ECG' in each_sensor:
            all_ecg += data_dict[each_time][each_sensor]['wave']
print(all_ecg)
plt.plot(all_ecg)
plt.savefig('ecg2.png')
plt.show()