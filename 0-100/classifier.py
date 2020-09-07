

from sklearn.preprocessing import StandardScaler  
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import classification_report, mean_squared_error
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
import numpy as np 
from operator import itemgetter 
import random
#from mpl_toolkits.mplot3d import Axes3D
 
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

class Classifier():
	
	def __init__(self, full_train_set, X_train_ix, num_neighbors=2):
		
		self.train_point_df=full_train_set.loc[X_train_ix,:].copy()#here its not objectives_to_sample_from because it was changed
		X_train=self.train_point_df[['lat', 'lon', 'unix time']]
		y_train=self.train_point_df[['label']]
		X_train_ix=self.train_point_df.index
		
		test_df=full_train_set.copy().drop(X_train_ix )
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
		self.GP_clf=GaussianProcessClassifier()
		#self.classifier.fit(self.X_train, self.y_train.values.ravel())  
		self.mse=self.classify()
	
		
	def plot_train(self, i, j):
		
		'''plt.title('training set')
		plt.plot(self.X_train[self.y_train==0,0], self.X_train[self.y_train==0,1], '.', label='class 1')
		plt.plot(self.X_train[self.y_train==1,0], self.X_train[self.y_train==1,1], '.', label='class 2')
		plt.legend()
		plt.savefig('problem_%s_iteration_%s.png' %(i, j))
		plt.clf()'''
		
	def classify(self, mode='random',X_train_ix=None):
		
		self.clf.fit(self.X_train, self.y_train) 
		self.GP_clf.fit(self.X_train, self.y_train) 
		if mode=='GP': 
			y_pred = self.GP_clf.predict(self.X_test)
			return mean_squared_error(self.y_test, y_pred, multioutput='raw_values')[0]
		y_pred = self.clf.predict(self.X_test)
		
		'''fig = plt.figure(1, figsize=(4, 3))
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
		plt.savefig('fig.png')'''
		
		#print(classification_report(self.y_test, y_pred))
		return mean_squared_error(self.y_test, y_pred, multioutput='raw_values')[0]
	def choose_new_objective(self, mode, banned_set):
		
		if mode=='random':
			ix_list_sorted=random.sample(list(self.X_test_ix), len(self.X_test_ix))
			return ix_list_sorted
		
		kneighbors=self.clf.kneighbors(self.X_test)
		proba=self.clf.predict_proba(self.X_test)
		GP_proba=self.GP_clf.predict_proba(self.X_test)
		
		prob_list=[]
		GP_prob_list=[]
		kneighbors_list=[]
		expected_mse_list=[]
        
		for row_number, ix in enumerate(self.X_test_ix):
			if ix in banned_set: continue
			
			if proba.shape[1]==1: 
				print([proba[0,0]])
				prob_list=list(zip(self.X_test_ix, [proba[0,0]]*len(self.X_test_ix)))
				GP_prob_list=list(zip(self.X_test_ix, [GP_proba[0,0]]*len(self.X_test_ix)))
				kneighbors_list=prob_list
				expected_mse_list=prob_list
				break
			
			kneighbors_list.append((ix, kneighbors[0][row_number,0]/kneighbors[0][row_number,1] ) )
			prob_list.append( (ix, abs(proba[row_number,0]-0.5) ) )
			GP_prob_list.append( (ix, abs(GP_proba[row_number,0]-0.5) ) )

			train_point_df_zero=self.train_point_df.copy()
			added_sample_df_zero=self.full_train_set.loc[ix].copy()
			added_sample_df_zero.loc['label']=0
			train_point_df_zero=train_point_df_zero.append(added_sample_df_zero)
			mse_zero=Classifier(self.full_train_set, train_point_df_zero.index).mse
		


			train_point_df_one=self.train_point_df.copy()
			added_sample_df_one=self.full_train_set.loc[ix].copy()
		
			added_sample_df_one.loc['label']=0
			train_point_df_one=train_point_df_one.append(added_sample_df_one)
			mse_one=Classifier(self.full_train_set, train_point_df_one.index).mse
			
			
			ix_mse = mse_zero*proba[row_number,0] + mse_one*proba[row_number,1]
			expected_mse_list.append((ix, ix_mse))
		
		
		if mode == 'greedy':
			prob_list_sorted=sorted(prob_list, key = lambda x: x[1])
			ix_list_sorted = [el[0] for el in prob_list_sorted]
		elif mode == 'uncertainty':
			kneighbors_list_sorted=sorted(kneighbors_list, key = lambda x: x[1])
			ix_list_sorted = [el[0] for el in kneighbors_list_sorted]
		elif mode == 'lookahead':
			expected_mse_list_sorted=sorted(expected_mse_list, key = lambda x: x[1])
			
			ix_list_sorted = [el[0] for el in expected_mse_list_sorted]
		##### this is new mode- Gaussian Process:
		elif mode == 'GP':
			GP_prob_list_sorted=sorted(GP_prob_list, key = lambda x: x[1])
			
			ix_list_sorted = [el[0] for el in GP_prob_list_sorted]
		return ix_list_sorted
