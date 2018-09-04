import loadData as loader
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing
import matplotlib.pyplot as plt


x_train, y_train, x_test, y_test = loader.load_data("../res/readout7.xls")

Y_index = []
x_train = preprocessing.scale(x_train)
x_test = preprocessing.scale(x_test)
d = {}
ha = []

# for Y in range(3, 20):
#     model = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(Y,), random_state=1, max_iter=100000,
#                           momentum=0.9,
#                           activation='logistic', learning_rate_init=0.001, tol=1e-5)
#
#     model.fit(x_train, y_train)
#     preDiff = model.score(x_test, y_test)
#     loss = model.loss_
#     h = {
#         'loss':loss,
#         'pre':preDiff,
#         'y':Y
#     }
#     ha.append(h)
#     d[Y] = model.loss_
# minY = 3
# maxPre = 0
# print(ha)
# for i in ha:
#     if i['loss']>0.1:
#         continue
#     if maxPre<i['pre']:
#         maxPre = i['pre']
#         minY = i['y']
# # for key in d:
# #     if minloss > d[key]:
# #         minY = key
# #
# print(minY)
model = MLPClassifier(solver='adam', alpha=1e-5, hidden_layer_sizes=(17,), random_state=1, max_iter=100000,
                      momentum=0.9,
                      verbose=10,
                      activation='relu', learning_rate_init=0.001, tol=1e-5)

# y_train = preprocessing.scale(y_train)
# y_test = preprocessing.scale(y_test)
model.fit(x_train, y_train)
print(model)
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