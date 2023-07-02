#%%
import numpy as np
import pandas as pd
import matplotlib

#%%
datafile='zeta_zeros10e5'

df=pd.read_csv(datafile, header=None, names=['zeroes'])

# %%
print(df.head())
# %%
with open(datafile, 'r') as my_file:
    print(my_file.readlines())

#%%
df['round']=np.floor(df['zeroes'])%10
df.hist('round', bins=10)


#%%
import os
directory='./histogram'
os.mkdir(directory)

#%%
df['fractional']=np.modf(df['zeroes'])[0]
hist_fractional=df.hist('fractional', bins=10)

hist_fractional[0][0].figure.savefig('histogram/fractional_parts')

# %%
df['spacings']=df['zeroes'].diff()

# %%
hist_spacings=df.hist('spacings', bins=1000)
hist_spacings[0][0].figure.savefig('histogram/spacings')
# %%
df.spacings.describe()