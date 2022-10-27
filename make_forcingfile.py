import xarray as xr 
import os
import datetime
from tqdm import tqdm

def make_forcingfile(filename,unit_height,year,month,day,heure,ground_height,path_data,compteur=1):
    file = open(filename,"a")
    if compteur ==0:
        file.write(unit_height)
        file.write("\n")
    if compteur ==0:
        file.write("25")
        file.write("\n")
    file.write(year+" "+month+" "+day+" "+str(float(heure)*3600))
    file.write("\n")
    file.write(ground_height)
    file.write("\n")
    data = xr.open_dataset(path_data)
    P = data['PABST'].values
    file.write(str(P[0,1,8,8]))
    Theta = data['THT'].values
    file.write("\n")
    file.write(str(Theta[0,1,8,8]))
    file.write("\n")
    Rv = data['RVT'].values
    file.write(str(Rv[0,1,8,8]))
    file.write("\n")
    file.write(str(len(P[0,1:-1,8,8])))
    file.write("\n")
    U = data['UT'].values
    V = data['VT'].values
    Z = data['level'].values
    for i in range(1,len(P[0,:-1,8,8])):
        file.write(str(Z[i])+" "+str(U[0,i,8,8])+" "+str(V[0,i,8,8])+" "+str(Theta[0,i,8,8])+" "+str(Rv[0,i,8,8])+" "+"0 0 0 0 0")
        file.write("\n")


def convert(str_time):
    format = '%Y%m%d%H'
    datetime_value = datetime.datetime.strptime(str_time, format)
    return datetime_value

list_filename = os.listdir('/home/newton/ienm2020/henona/Bureau/UE_2_MESO_NH/ARO_ARP_GFS/AROME/AN/')
delta = datetime.timedelta(hours=1)
date = convert("2022091921")
os.system('rm *.txt')
compteur = 0
for x in tqdm(list_filename):
    make_forcingfile('forcing_file_'+date.strftime('%Y%m%d%H')+'.txt','ZFRC',str(date.year),str(date.month),str(date.day),str(date.hour),'0','/home/newton/ienm2020/henona/Bureau/UE_2_MESO_NH/ARO_ARP_GFS/AROME/AN/'+x,compteur)
    date = date +delta
    compteur = 1

os.system("rm FORCING_FILE.txt")
liste = os.listdir('/home/newton/ienm2020/henona/Bureau/UE_2_MESO_NH/')
list_txt = []
for x in liste:
    if x[:3] == "for":
        list_txt.append(x)
list_txt = sorted(list_txt)
os.system("cat "+list_txt[0]+">FORCING_FILE.txt")
for x in list_txt[1:]:
    os.system("cat "+x+">>FORCING_FILE.txt")
