# sb5_caroline-wall.py

# By: Caroline Wall

# Version 1.0

# Last Edit: 2021-10-31

# This script reads an HDF5 file, extracts the data,
# and saves it in an ASCII raster file.

import os
import os.path
import numpy
import h5py

def get_attr(hf, attr, group_path):
        """
        Name:     get_attr
        Features: Returns the given attribute for the given path
        Inputs:   - open h5py file object (hf)
                  - str, attribute name (attr)
                  - str, group path (group_path)
        Outputs:  str, attribute value (val)
        """
        if group_path in hf:
            if attr in hf[group_path].attrs.keys():
                try:
                    tmp = hf[group_path].attrs[attr]

                    if isinstance(tmp, str):
                        val = tmp
                    elif isinstance(tmp, numpy.ndarray):
                        val = tmp
                    else:
                        try:
                            val = tmp.decode('UTF-8')
                        except:
                            val = tmp
                except KeyError:
                    print("'%s' has no attribute '%s'" % (group_path, attr))
                    val = "UNDEFINED"
                except:
                    print(
                        ("attribute '%s' could not be retrieved "
                         "from path '%s'!") % (attr, group_path))
                    val = "UNDEFINED"
            else:
                print("'%s' has no attribute '%s'" % (group_path, attr))
                val = "UNDEFINED"
        else:
            print('path not defined!')
            val = "UNDEFINED"

        return val

def get_object_attrs(hf, obj_path):
        """
        Name:     get_object_attrs
        Features: Returns dictionary of group/dataset attributes
        Inputs:   - open h5py file object (hf)
                  - str, object path (obj_path)
        Outputs:  dict, session attributes (attrs_dict)
        """
        attr_dict = {}
        if obj_path is not None and obj_path in hf:
            for key in hf[obj_path].attrs.keys():
                val = hf[obj_path].attrs[key]
                if isinstance(val, bytes):
                    attr_dict[key] = val.decode('UTF-8')
                else:
                    attr_dict[key] = val
        else:
            print(
                "could not get attributes for %s; object does not exist!",
                obj_path)

        return attr_dict

def list_objects(hf, parent_path):
        """
        Name:     list_objects
        Features: Returns a sorted list of HDF5 objects under a given parent
        Inputs:   - open h5py file object (hf)
                  - str, HDF5 path to parent object
        Outputs:  list, HDF5 objects
        """
        rlist = []
        if parent_path in hf:
            try:
                hf[parent_path].keys()
            except:
                # Dataset has no members
                rlist = 0
            else:
                for obj in sorted(list(hf[parent_path].keys())):
                    rlist.append(obj)
        else:
            wmgs = "'%s' does not exist!" % (parent_path)
            print(wmgs)
            print('returning empty list')

        return rlist

def print_attrs(hf, group):
    """
    Name:     print_attrs
    Inputs:   - open h5py file object (hf)
              - str, path to group or dataset (group)
    Outputs:  None.
    Features: Prints the attributes for a given HDF5 group/dataset
    Depends:  get_object_attrs
    """
    if group in hf:
        d = get_object_attrs(hf, group)
        for key in d:
            val = d[key]
            print("%s: %s: %s" % (group, key, val))


try:
    my_dir = os.environ['DS_WORKSPACE']
except:
    my_dir = "."

my_file = 'sandbox5.hdf'
hdf_path = os.path.join(my_dir, my_file)

# Reading root attributes
if os.path.isfile(hdf_path):
    hdfile = h5py.File(hdf_path, 'r')

    attrs = get_object_attrs(hdfile, '/data/assignment')
    dset = hdfile['/data/assignment']
    raster_data = dset[:,:]

    hdfile.close()

lines = []
row_vals = []

for row in range(648):
    for col in range(648):
        val = raster_data[row][col]
        row_vals.append(val)
    lines.append(row_vals)
    row = []

with open('caroline-wall.asc', 'w') as f:
    f.write('ncols ' + attrs['ncols'] + '\n')
    f.write('nrows ' + attrs['nrows'] + '\n')
    f.write('xllcorner ' + attrs['xllcorner'] + '\n')
    f.write('yllcorner ' + attrs['yllcorner'] + '\n')
    f.write('cellsize ' + attrs['cellsize'] + '\n')
    f.write('nodata_value ' + attrs['NODATA_value'] + '\n')
    for line in lines:
        for val in line:
            f.write(str(val))
            f.write(' ')
        f.write('\n')
