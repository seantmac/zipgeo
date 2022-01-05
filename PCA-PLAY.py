import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import 'scikit-learn' as sklearn
from sklearn.preprocessing import StandardScaler # This package is used for standardization a data set.
from sklearn.decomposition import PCA  # This package is used for apply one descomposition of the multiivariate data
# to principal components.

# Call Excel Data to py.
data = pd.read_csv('C:\OPTMODELS\CSMY\Data\RAWDATASET.CSV')

data2 = np.array(data.drop(columns=data.columns[0],axis=1 ))


#Standardizing

x = StandardScaler().fit_transform(data2)
x.head(15)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
Dataf = pd.DataFrame(data = principalComponents
             , columns = ['SHIP_DATE', 'LOAD_DATE'])


#Join Target to Absorbance date
Datatarget = pd.concat([Dataf, data[['CONTAINER_CT']]], axis = 1)



fig = plt.figure(figsize = (5,5))
plt.xlabel('SHP')
plt.ylabel('LD')
plt.title('Principal Component Analysis (PCA)')
targets = [200, 400, 600, 800, 1000]
colors = ['red', 'green', 'blue', 'yellow', 'cyan']
for target, color in zip(targets,colors):
    Indicatetarget = Datatarget['CONTAINER_CT'] == target
    plt.scatter(Datatarget.loc[Indicatetarget, 'SHIP_DATE']
               ,Datatarget.loc[Indicatetarget, 'LOAD_DATE'])

plt.legend(targets)
plt.show()

print((pca.explained_variance_)) #Determination of variance by PCA