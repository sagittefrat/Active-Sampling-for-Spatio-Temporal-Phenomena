
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler  
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.metrics import classification_report, mean_squared_error 

class Classifier():
	
	def __init__(self, X_test, y_test):


		self.scaler = StandardScaler()  
			
		self.X_test = self.scaler.transform(X_test) 
		self.y_test=y_test
		
		
		
	def classify(self, X_train, y_train):
		self.scaler.fit(X_train)
		self.X_train=scaler.transform(X_train)
		self.y_train=y_train
	
		classifier = KNeighborsClassifier(n_neighbors=3)  
		classifier.fit(X_train, y_train.values.ravel())  

		y_pred = classifier.predict(X_test)

		print(classification_report(y_test, y_pred))
		print('MSE ',mean_squared_error(y_test, y_pred, multioutput='raw_values'))

		'''
		plt.title('training set')
		plt.plot(X_test[y_pred==0,'lat'], X_test[y_pred==0,'lon'], '.', label='class 1')
		plt.plot(X_test[y_pred==1,'lat'], X_test[y_pred==1,'lon'], '.', label='class 2')
		plt.legend()
		plt.show()'''
	def choose_new_objective(self, train_set, objectives_to_sample_ix):
		objectives_to_choose_from=train_set[train_set not in objectives_to_sample_ix.any()]
		for ix, objective in objectives_to_choose_from.iterrows():
			pass