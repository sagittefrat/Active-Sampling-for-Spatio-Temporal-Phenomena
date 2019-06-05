
#import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import classification_report, mean_squared_error
from operator import itemgetter 

class Classifier():
	
	def __init__(self, full_train_set, X_train_ix,  num_neighbors=2):
		#print(X_train_ix)
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
		self.y_train=y_train
		self.X_train_ix=X_train_ix

		self.X_test = self.scaler.transform(X_test) 
		self.y_test=y_test
		self.X_test_ix=X_test_ix
		
		self.num_neighbors=num_neighbors
		self.classifier = KNeighborsClassifier(n_neighbors=self.num_neighbors, weights='distance') 

		#self.classifier.fit(self.X_train, self.y_train.values.ravel())  
		self.mse=self.classify()
		print('MSE ', self.mse)
		
		
	def classify(self, X_train_ix=None):
		
		print('len train, inside classifier: %s\n' %(len(self.y_train)))
		self.classifier.fit(self.X_train, self.y_train.values.ravel()) 

		y_pred = self.classifier.predict(self.X_test)

		#print(classification_report(self.y_test, y_pred))
		return mean_squared_error(self.y_test, y_pred, multioutput='raw_values')

	def choose_new_objective(self):
		
	
		proba=self.classifier.predict_proba(self.X_test)
		prob_list=[]
		for row_number, ix in enumerate(self.X_test_ix):
			#print (row_number, ix)
			prob_list.append( (ix, abs(proba[row_number,0]-0.5) ) )
		prob_list_sorted=sorted(prob_list, key = lambda x: x[1])
		ix_list_sorted = [el[0] for el in prob_list_sorted]
		return ix_list_sorted
