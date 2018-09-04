from sklearn.neural_network import MLPClassifier
import saveModel as sm
import GrainDataLoad as loader
import matplotlib.pyplot as plt
import time

x_train, y_train, x_test, y_test = loader.load_data('./readout2.xls')

# model = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(13,), random_state=1, max_iter=100000,
#                       momentum=0.9,
#                       verbose=10, activation='relu',learning_rate_init=0.001)
# model.fit(x_train, y_train)
#

# print(model.score(x_test, y_test))



    errors.append(model.loss_)Y_index = []
errors = []

for Y in range(3, 20):
    model = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(Y,), random_state=1, max_iter=100000,
                          momentum=0.9,
                          activation='relu', learning_rate_init=0.001)

    model.fit(x_train, y_train)
    Y_index.append(Y)
line = plt.plot(Y_index, errors)
plt.title('test layer size for error')
plt.xlabel('hidden_layers_sizes')
plt.ylabel('error')
plt.yscale('symlog', linthreshy=0.5)
plt.setp(line, 'color', 'r', 'linewidth', 2.0)
plt.show()

model = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1, max_iter=100000,
                      momentum=0.9,
                      verbose=10,
                      activation='relu', learning_rate_init=0.001, tol=1e-5)

model.fit(x_train, y_train)
print( model.n_layers_)
print( model.loss_)
print( model.out_activation_)
start = time.clock()
print(model.score(x_test, y_test))
print(x_test)
print(model.predict(x_test))
end = time.clock()
print('Running time: %s Seconds' % (end - start))
sm.save_model(model)
