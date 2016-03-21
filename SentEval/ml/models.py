from sklearn import svm
from sklearn.cross_validation import train_test_split
from sklearn.externals import joblib
import pandas, sys
import pickle

dset = sys.argv[1]
initial_matrix = pandas.read_csv(dset, sep="\t")

food_answers = initial_matrix.aspect1
interior_answers = initial_matrix.aspect2
service_answers = initial_matrix.aspect3

print(food_answers.shape)

data = initial_matrix.drop(['id', 'aspect1', 'aspect2', 'aspect3'], 1)

def test_machine(questions, answers):
	'''
	functions for testing and optimizing
	'''
	train_questions, test_questions, train_answers, test_answers = train_test_split(questions, answers, test_size = 0.3, random_state=42)
	model = svm.SVC()
	fit_this = model.fit(train_questions, train_answers)
	predictions = fit_this.predict(test_questions)
	return f1_score(predictions, test_answers, average = "weighted")

def dump_machine(questions, answers):
	'''
	the main function
	'''
	model = svm.SVC()
	fit_this = pickle.dumps(model.fit(questions, answers))
	return fit_this

food_machine = joblib.dump(dump_machine(data, food_answers), 'food.pkl')
interior_machine = joblib.dump(dump_machine(data, interior_answers), 'interior.pkl')
service_machine = joblib.dump(dump_machine(data, service_answers), 'service.pkl')

