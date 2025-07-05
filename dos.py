import pandas as pd
import csv
import re
from collections import Counter
import copy
import os
from tqdm import tqdm

#This is the latest version of dos.py
##prerequisites
# * pandas 
# * tqdm   
# tqdm can be installed using pip as "pip install tqdm"
#This programme requires DOSCAR and POSCAR in the working directory. The number of formula units will be prompted while execution
print("######################################################################################################################################")
print('#################################################################DOS.PY###############################################################')
print("######################################################################################################################################")

print('Reading DOSCAR......')
reader = csv.reader(open('DOSCAR','r'))
rows = list(reader)
first_line = str(rows[0])
a = first_line.strip().split()
no_ions = a[1]
no_elements = int(a[2])
if str(a[3])== 1:
    spin_pol = True
sixth_line = str(rows[5]).strip().split()    
E_max = sixth_line[1]
E_min = sixth_line[2]
n_dos = int(sixth_line[3])
E_fermi = float(sixth_line[4]) 
tot_dos = rows[6:n_dos+6]   
r = n_dos+6
d = {}
for i in range(no_elements):
    d["element_{}".format(i+1)]=(rows[r+1:r+(n_dos+1)])
    r = r+n_dos+1



f = open("POSCAR", "r")
lines = f.readlines()
an = lines[0]
sh = lines[5]


def getitems(firstline):
    a_0= firstline.split()
    vp = a_0[len(a_0)-1].split()
    p= list(filter(lambda x: 'VASPAtoms:' in x, a_0))
    pn = p[0]
    print(pn)
    if pn in a_0:
       idx = a_0.index(pn)
    b = a_0[idx:]
    a = str(b[0])
    stop=['{VASPAtoms:','}']
    c = [(lambda x: re.sub(r'|'.join(stop), '', x))(x) for x in b]
    print(c)
    def mysplit(s):
        elements = s.strip('0123456789')
        tail = s[:-len(elements)]
        return(elements+" "+  tail)
    d = [mysplit(s) for s in c]
#for elem in d:
    print(d)
    global elements
    global numbers
    elements= []
    number = []
    for i in range(len(d)):
       dh = list(d[i].split())
       if i<len(d):
          elements.append(dh[0])
          number.append(dh[1])
    print(number)
#
## For finding the number of types of elements
    brh = lines[5].split()
    numbers = ["0"]
    for i in range(len(number)):
        ele = int(numbers[i])
        brh= brh[ele:]
        re_number = 0
        for ele in range(len(brh)):
            re_number = re_number + int(brh[ele])
            if (int(re_number)==int(number[i])):
               numbers.append(ele+1)
               break
    numbers = numbers[1:]
    print(re_number)
def getelem_and_num(ele):
    print('Extracting the elements and their types......')
    global numbers
    global elements
    global re_number
    re_number = {i:ele.count(i) for i in ele}
    print(re_number)
    no_elem = len(ele)
    elements = []

    for x in ele:
        if x not in elements:
            elements.append(x)
    numbers= []
    for elem in elements:
         numbers.append(re_number[elem])
    return numbers, elements
lines[5] = lines[5].strip()
ele = lines[5].split()
if (str(ele[0]).isdigit()):
   print("sixth line contains numbers ")
   types_ele = lines[5].strip().split()
   print(types_ele)
   getitems(an)
else:
   print("Sixth line contains elements")
   types_ele = lines[6].strip().split()
   print(types_ele)

   getelem_and_num(ele)

print(numbers)
print (elements)

foo1 =[]
mylist = list(dict.fromkeys(elements))
print(mylist)
foo = Counter(ele)
for i in range(len(mylist)):
    if foo[mylist[i]] >1:
        for j in range(1, foo[mylist[i]]+1):
            foo1.append(mylist[i]+"_"+str(j))
    else:
        foo1.append(mylist[i])
print(foo1)
h=0
p = copy.deepcopy(d)

for i in range(len(types_ele)): 
    h = h+int(types_ele[i])
    p[foo1[i]] = p.pop("element_"+str(h))
   
dos_spin = ["el_energy", "s_u", "s_d", "py_u", "py_d","pz_u", "pz_d", "px_u", "px_d", "dxy_u", "dxy_d", "dyz_u", "dyz_d", "dz2_u", "dz2_d", "dxz_u", "dxz_d", "dx2-y2_u", "dx2-y2_d"]

foo2 = copy.deepcopy(foo1)
data = []
data1 =pd.DataFrame()
print('Extracting DOS for each elements')
for i in tqdm(range(len(foo2)), desc= 'exctraction progress'):
    for j in tqdm(range(n_dos), desc= 'extraction of '+foo2[i]+' DOS'):
        data.append(pd.DataFrame([str(p[foo2[i]][j]).strip("['").strip("']").strip().split()], columns=dos_spin)) 
foo3 = 0
for j in range(len(foo2)):
    for i in range(foo3, len(data)):        
        data1 = pd.concat([data1, data[i]], axis=0)    
        if i==(n_dos*(j+1))-1:
            foo3 = foo3+n_dos
            p[foo2[j]] = data1
            data1 = pd.DataFrame()
            break
for key in list(p.keys()):
    if "element" in key:
        del p[key]
for i in range(len(foo2)):
    p[foo2[i]] = p[foo2[i]].astype(float)

for i in range(len(foo2)):
    p[foo2[i]]["s_t"] = p[foo2[i]]["s_u"]+p[foo2[i]]["s_d"]
    p[foo2[i]]["p_u"] = p[foo2[i]]["pz_u"]+p[foo2[i]]["px_u"]+p[foo2[i]]["py_u"]
    p[foo2[i]]["p_d"] = -(p[foo2[i]]["pz_d"]+p[foo2[i]]["px_d"]+p[foo2[i]]["py_d"])
    p[foo2[i]]["p_t"] = p[foo2[i]]["p_u"]-p[foo2[i]]["p_d"]
    p[foo2[i]]["d_u"] = p[foo2[i]]["dxy_u"]+p[foo2[i]]["dyz_u"]+p[foo2[i]]["dxz_u"]+p[foo2[i]]["dz2_u"]+p[foo2[i]]["dx2-y2_u"]
    p[foo2[i]]["d_d"] = -(p[foo2[i]]["dxy_d"]+p[foo2[i]]["dyz_d"]+p[foo2[i]]["dxz_d"]+p[foo2[i]]["dz2_d"]+p[foo2[i]]["dx2-y2_d"])
    p[foo2[i]]["d_t"] = p[foo2[i]]["d_u"]-p[foo2[i]]["d_d"]
    p[foo2[i]]["t"] = p[foo2[i]]["d_t"]+p[foo2[i]]["p_t"]+p[foo2[i]]["s_t"]
    p[foo2[i]]["el_energy"] = p[foo2[i]]["el_energy"] - E_fermi
    p[foo2[i]]["dxy_d"] = -(p[foo2[i]]["dxy_d"])
    p[foo2[i]]["dxz_d"] = -(p[foo2[i]]["dxz_d"])
    p[foo2[i]]["dyz_d"] = -(p[foo2[i]]["dyz_d"])
    p[foo2[i]]["dz2_d"] = -(p[foo2[i]]["dz2_d"])
    p[foo2[i]]["dx2-y2_d"] = -(p[foo2[i]]["dx2-y2_d"])
    p[foo2[i]]["t2g_u"] = p[foo2[i]]["dxy_u"]+p[foo2[i]]["dyz_u"]+p[foo2[i]]["dxz_u"]
    p[foo2[i]]["t2g_d"] = p[foo2[i]]["dxy_d"]+p[foo2[i]]["dyz_d"]+p[foo2[i]]["dxz_d"]
    p[foo2[i]]["t2g"] =  p[foo2[i]]["t2g_u"] -  p[foo2[i]]["t2g_d"]
    p[foo2[i]]["eg_u"] = p[foo2[i]]["dz2_u"]+p[foo2[i]]["dx2-y2_u"]
    p[foo2[i]]["eg_d"] = p[foo2[i]]["dz2_d"]+p[foo2[i]]["dx2-y2_d"]
    p[foo2[i]]["eg"]  = p[foo2[i]]["eg_u"] - p[foo2[i]]["eg_d"]


print("\n Writing files.....")
for i in range(len(foo2)):
    p[foo2[i]][foo2[i]+'_u'] = p[foo2[i]]["s_u"]+p[foo2[i]]["p_u"]+p[foo2[i]]["d_u"]
    p[foo2[i]][foo2[i]+'_d'] = -(p[foo2[i]]["s_d"])+p[foo2[i]]["p_d"]+p[foo2[i]]["d_d"]

f.u = input("Enter the number of formula units: ")
f.u = int(f.u)

#for getting data for total dos    
data2 = []
t_dos_columns = ["Energy", "DOS_u", "DOS_d", "int_DOS_u", "int_DOS_d"]
for i in range(n_dos):
    data2.append(pd.DataFrame([str(tot_dos[i]).strip("['").strip("']").split()], columns=t_dos_columns))
t_dos=pd.DataFrame()
for i in range(n_dos):
    t_dos = pd.concat([t_dos, data2[i]], axis = 0)
t_dos = t_dos.astype(float)

t_dos["DOS_u"] = t_dos["DOS_u"]/f.u
t_dos["DOS_d"] = t_dos["DOS_d"]/f.u
t_dos["int_DOS_u"] = t_dos["int_DOS_u"]/f.u
t_dos["int_DOS_d"] = t_dos["int_DOS_d"]/f.u
t_dos["t_dos"] = t_dos["DOS_u"]+ t_dos["DOS_d"]
t_dos["Energy"] = t_dos["Energy"] - E_fermi
t_dos["DOS_d"] = - (t_dos["DOS_d"])

#writing files in DOS_data directory
cwd = os.getcwd()
path_dir = os.path.join(cwd, "DOS_data")
if os.path.exists(path_dir):
	pass
else:
	os.mkdir(path_dir)

for i in range(len(foo2)):
        p[foo2[i]].to_csv(str(cwd)+"/DOS_data/"+foo2[i]+'.csv')

t_dos.to_csv(str(cwd)+'/DOS_data/total.csv')        
