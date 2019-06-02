
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors
from sklearn.metrics import classification_report, mean_squared_error 

class Classifier():
	
	def __init__(self, X_test, y_test, X_train, y_train, X_train_ix, X_test_ix, num_neighbors=2):


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

		self.classifier.fit(self.X_train, self.y_train.values.ravel())  
		
		
		
	def classify(self, X_train, y_train, X_train_ix, X_test_ix):
		
		self.scaler.fit(X_train)
		self.X_train=self.scaler.transform(X_train)
		self.y_train=y_train
		self.X_train_ix=X_train_ix
		self.X_test_ix=X_test_ix
	 	
		self.classifier.fit(self.X_train, self.y_train.values.ravel()) 

		y_pred = self.classifier.predict(self.X_test)

		#print(classification_report(self.y_test, y_pred))
		print('MSE ',mean_squared_error(self.y_test, y_pred, multioutput='raw_values'))

		'''
		plt.title('training set')
		plt.plot(X_test[y_pred==0,'lat'], X_test[y_pred==0,'lon'], '.', label='class 1')
		plt.plot(X_test[y_pred==1,'lat'], X_test[y_pred==1,'lon'], '.', label='class 2')
		plt.legend()
		plt.show()'''
	def choose_new_objective(self, train_set, objectives_to_sample_ix):
		
	
		proba=self.classifier.predict_proba(self.X_test)
		prob_list=[]
		for row_number, ix in enumerate(self.X_test_ix):
			prob_list.append( (ix, abs(proba[row_number,0]-0.5) ) )
		
		return sorted(prob_list, key = lambda x: x[1])