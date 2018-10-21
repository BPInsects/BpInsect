# coding=utf-8
import GrainDataLoad as loader
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from modelManage import save_model,saveFile
import matplotlib.pyplot as plt


x_train, y_train, x_test, y_test,trainList = loader.load_data("../res/savedata2.xls")

Y_index = []
x_train = preprocessing.scale(x_train)
x_test = preprocessing.scale(x_test)
d = {}

for Y in range(3, 20):
    model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(Y,), random_state=1, max_iter=100000,
                          momentum=0.9,
                          activation='logistic', learning_rate_init=0.001, tol=1e-5,verbose=10)

    model.fit(x_train, y_train)

    print(model.loss_)

    # d[Y] = model.loss_
    d[Y] = model.score(x_test, y_test)
minY = 3
maxY = 3
# minloss = 1000
# for key in d:
#     if minloss > d[key]:
#         minY = key

maxscore = 0
for key in d:
    if maxscore < d[key]:
        maxY = key



model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(maxY,), random_state=1, max_iter=100000,
                      momentum=0.9,
                      verbose=10,
                      activation='logistic', learning_rate_init=0.001, tol=1e-5)

# y_train = preprocessing.scale(y_train)
# y_test = preprocessing.scale(y_test)
model.fit(x_train, y_train)
print( model.n_layers_)
print( model.loss_)
print( model.out_activation_)

print(model.score(x_test, y_test))
print(model.predict(x_test))
print(x_test)
print(y_test)
down = []
for i in range(y_train.__len__()):
    down.append(i)

fittingAccuracy = 1 - model.loss_
predictionAccuracy = d[maxY]


print(model.loss_)
save_model(model,'00100100101_小露尾甲_b_0.95_0.85_50')

# saveFile(trainList,'00100100101_米象_b_0.95_0.85_50')