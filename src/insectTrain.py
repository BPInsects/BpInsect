import GrainDataLoad as loader
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
from saveModel import save_model
import matplotlib.pyplot as plt


x_train, y_train, x_test, y_test = loader.load_data("../res/savedata2.xls")

Y_index = []
x_train = preprocessing.scale(x_train)
x_test = preprocessing.scale(x_test)
d = {}

for Y in range(3, 20):
    model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(Y,), random_state=1, max_iter=100000,
                          momentum=0.9,
                          activation='logistic', learning_rate_init=0.001, tol=1e-5)

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


print(maxY)
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
print(y_test)
down = []
for i in range(y_train.__len__()):
    down.append(i)


# plt.plot(down,y_train,label='line one')
# plt.plot(down,model.predict(x_train),label='line two')
#
# plt.show()
print(model.loss_)
save_model(model,'nslk_xcbg.model')