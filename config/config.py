#%%
import pandas as pd
import csv
#%%
"Network settings"
num_agents = 10
same_prob_connect = 0.5
other_prob_connect = 0.1
prob_connect = 0.5             #probabaility of connecting when in the same group

"Model settings/parameters"
socializeTime = 5      #number of time steps after which agents socialize
str_experience = 0.1
str_invest = 0.1
str_social = 0.1
str_crowding = 0.1

shareBikeOwners = 0.5
shareCarOwners = 0.5

"Initial state settings"
ICE_ini = 0.1          #internal combutions engine
PT_ini = 0.1           #public transport
BI_ini = 0.1           #bike
GF_ini = 0.1           #going on foot
FCS_ini = 0.1          #free floating car sharing
SCS_ini = 0.1          #stationary car sharing


"Initial group settings"
EL_share = 0.195
CP_share = 0.659
RT_share = 0.146

#%%
"Read in data on attitudes per cluster from Wolf et al. (2019)"
clusterData = pd.read_csv("../data/processed/Cluster_data.CSV", delimiter=';', index_col = [0], header=[0,1])
"access data in this format: "
#clusterData.loc['ICE',('EL','Mean')]#"

##reader = csv.DictReader(open('State_data.csv'))

#d = {}
#for row in reader:
##   k, v = row
#   d[k] = v

#dictobj = next(reader) 

# %%
#with open('State_data.csv', mode='r') as infile:
#    reader = csv.reader(infile)
#    with open('State_data_new.csv', mode='w') as outfile:
#        writer = csv.writer(outfile)
#        mydict = {rows[0]:rows[1] for rows in reader}
# %%

# opening the file using "with"
# statement
#filename = 'State_data.csv'
#with open(filename, 'r') as data:
##  for line in csv.DictReader(data):
#      print(line)

# %%
