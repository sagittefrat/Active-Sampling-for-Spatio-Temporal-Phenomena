

from sklearn.preprocessing import StandardScaler  
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import classification_report, mean_squared_error
import numpy as np 
from operator import itemgetter 
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')


class Classifier():
	
	def __init__(self, full_train_set, X_train_ix,  num_neighbors=2):
		
		train_df=full_train_set.ix[X_train_ix,:] #here its not objectives_to_sample_from because it was changed
		X_train=train_df[['lat', 'lon', 'unix time']]
		y_train=train_df[['label']]
		X_train_ix=train_df.index
		
		test_df=full_train_set.drop(X_train_ix )
		X_test=test_df[['lat', 'lon', 'unix time']]
		y_test=test_df[['label']]
		X_test_ix=test_df.index
		
		self.full_train_set=full_train_set
		self.scaler = StandardScaler()  
		self.scaler.fit(X_train)
		self.X_train=self.scaler.transform(X_train)
		self.y_train=y_train.values.ravel()
		self.X_train_ix=X_train_ix

		self.X_test = self.scaler.transform(X_test) 
		self.y_test=y_test
		self.X_test_ix=X_test_ix
		
		self.num_neighbors=num_neighbors
		self.clf = KNeighborsClassifier(n_neighbors=self.num_neighbors, weights='distance') 
		
		#print(self.y_train.values.ravel())
		#self.classifier.fit(self.X_train, self.y_train.values.ravel())  
		self.mse=self.classify()
		print('MSE ', self.mse)
		
		
	def classify(self, X_train_ix=None):
		
		print('len train, inside classifier: %s\n' %(len(self.y_train)))
		self.clf.fit(self.X_train, self.y_train) 

		y_pred = self.clf.predict(self.X_test)
		
		fig = plt.figure(1, figsize=(4, 3))
		plt.clf()
		ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
		for name, label in [('0', 0), ('1', 1)]:
			ax.text3D(self.X_train[self.y_train == label, 0].mean(),
					  self.X_train[self.y_train== label, 1].mean() + 1.5,
					  self.X_train[self.y_train == label, 2].mean(), name,
					  horizontalalignment='center',
					  bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))
		# Reorder the labels to have colors matching the cluster results
		y = np.choose(self.y_train, [1, 2, 0]).astype(np.float)
		ax.scatter(self.X_train[:, 0], self.X_train[:, 1], self.X_train[:, 2], c=y, cmap=plt.cm.nipy_spectral,
				   edgecolor='k')

		ax.w_xaxis.set_ticklabels([])
		ax.w_yaxis.set_ticklabels([])
		ax.w_zaxis.set_ticklabels([])
		plt.savefig('fig.png')
		
		#print(classification_report(self.y_test, y_pred))
		return mean_squared_error(self.y_test, y_pred, multioutput='raw_values')

	def choose_new_objective(self):
		
	
		proba=self.clf.predict_proba(self.X_test)
		prob_list=[]
		for row_number, ix in enumerate(self.X_test_ix):
			#print (row_number, ix)
			prob_list.append( (ix, abs(proba[row_number,0]-0.5) ) )
		prob_list_sorted=sorted(prob_list, key = lambda x: x[1])
		ix_list_sorted = [el[0] for el in prob_list_sorted]
		return ix_list_sorted
