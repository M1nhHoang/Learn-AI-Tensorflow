import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
import ClawDataGcafe

def load_saveModel():
	src = r'.\Save_Model'
	Model_list = os.listdir(src)
	
	return Model_list

def predict(x, model):
	x = tf.expand_dims(x, 0)
	pred = model.predict(x)

	return round(float(pred[0][0]), 2)

def check_existModel(Stock_Symbol):
	if f'PredictStock_{Stock_Symbol}.h5' in load_saveModel():
		return True
	else:
		return False

def KiemTraNamNhuan(year):
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    return False

def DemSoNgayTrongThang(month, year):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif KiemTraNamNhuan(year) == True:
            return 29
    return 28

def predict_stock(Stock_Symbol):
	global means_price
	global std_price

	#get data
	data = ClawDataGcafe.get_data(Stock_Symbol)

	# datafarame
	Stock_df = pd.DataFrame(data, columns =['Date', 'Price', 'Volume'])

	# split data
	Price = Stock_df['Price'].to_numpy()
	Date = Stock_df['Date'].to_numpy()

	X_price = []
	X_Date = []
	step = 5
	for i in range(0, len(Price)-step, step):
	    X_price.append(Price[i:i+step-1])
	    X_Date.append(Date[i:i+step-1])

	X_price, X_Date = np.array(X_price), np.array(X_Date)

	# create df for price
	mean_price_df = pd.DataFrame(X_price, columns =['price_1', 'price_2', 'price_3', 'price_4'])
	
	# Calculate the mean of each column
	means_price = [mean_price_df[col].mean() for col in mean_price_df]

	# Calculate the Std. Deviation of each column
	std_price = [mean_price_df[col].std() for col in mean_price_df]

	#load model
	model = load_model(fr'.\Save_model\PredictStock_{Stock_Symbol}.h5')

	# today
	today = X_Date[0][0]

	# price today
	price = list(X_price[0])

	# predict
	print('\n')
	end_day = int(input('Nhập Số Ngày Bạn Muốn Dự Đoán: '))
	day, month, year = today.split('/')
	day, month, year = int(day), int(month),int(year)

	newPrice_list = []
	newDate_list = []

	while end_day != 0:
		# predict
		price_pred = predict(price, model)

	    # tinh ngay`
		dayInMonth = DemSoNgayTrongThang(month, year)
		day += 1
		if day > dayInMonth:
		    day = 1
		    month += 1

		if month > 12:
		    month = 1
		    year += 1
		newDate_list.append(str(day)+'/'+str(month)+'/'+str(year))

		# tinh tien`
		price = price[1:]
		price.append(price_pred)
		newPrice_list.append(price_pred)

		# print
		print(f'\nGiá Của {Stock_Symbol} vào ngày {day}/{month}/{year} được dự đoán là: {price_pred}\n')

		end_day -= 1

	# save txt
	with open(f'Giá_Dự_Đoán_Của_{Stock_Symbol}_Ngày_{newDate_list[0]}.txt','w',encoding = 'utf-8') as f: f.write(f'Giá Dự Đoán: {newPrice_list[0]}')

	# show trading view
	plt.plot(newDate_list, newPrice_list)
	plt.ylabel('VND x 1.000')
	plt.xlabel('Day/Month/Year')
	plt.title(f'Giá Dự Đoán Của {Stock_Symbol}. [{today} Đến {day}/{month}/{year}]')
	plt.show()

# Create TensorFlow preprocessing function for stats stream
def stat_scaler_price(tensor):
    return (tensor - means_price) / std_price

# xây dựng mô hình
def create_model(optimizer):
    model = tf.keras.models.Sequential()
    
    model.add(tf.keras.Input(shape=(4,)))
    model.add(tf.keras.layers.Lambda(stat_scaler_price))
    model.add(tf.keras.layers.Dense(64, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(128, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(256, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(512, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(1, activation = 'linear'))
    
    model.compile(optimizer=optimizer,
                  loss='mse')

    return model

def train_newModel(Stock_Symbol):
	global means_price
	global std_price

	#get data
	data = ClawDataGcafe.get_data(Stock_Symbol)

	# datafarame
	Stock_df = pd.DataFrame(data, columns =['Date', 'Price', 'Volume'])
	Stock_df = Stock_df[::-1].reset_index()
	Stock_df = Stock_df.drop(['index'], axis=1)

	# split data
	Price = Stock_df['Price'].to_numpy()
	Date = Stock_df['Date'].to_numpy()

	X_price = []
	X_Date  = []
	Y       = []
	step = 5
	for i in range(0, len(Price)-step, step):
	    X_price.append(Price[i:i+step-1])
	    X_Date.append(Date[i:i+step-1])
	    Y.append(Price[i+step-1:i+step])

	X_price, X_Date, Y = np.array(X_price), np.array(X_Date), np.array(Y)

	# create df for price
	mean_price_df = pd.DataFrame(X_price, columns =['price_1', 'price_2', 'price_3', 'price_4'])
	
	# Calculate the mean of each column
	means_price = [mean_price_df[col].mean() for col in mean_price_df]

	# Calculate the Std. Deviation of each column
	std_price = [mean_price_df[col].std() for col in mean_price_df]

	#split data
	split = int(len(X_price)*95/100)
	x_train_price, x_test_price = X_price[:split], X_price[split:]

	y_train, y_test = Y[:split], Y[split:]

	# train model
	print('\nBắt đầu Train model...\n')
	pred_rate = 0
	lr = 0.002
	rag = 0.2
	while pred_rate <= 45:
		# build model
		# định nghĩa thuật toán tối ưu
		optimizer = tf.keras.optimizers.SGD(learning_rate=lr)
		model = create_model(optimizer)

		# Thiết lập hàm call back Early Stopping
		callback = tf.keras.callbacks.EarlyStopping(monitor='val_loss', min_delta=0.1, mode="auto", patience=150, restore_best_weights=True)
		history = model.fit(x_train_price, y_train, epochs = 5000, batch_size = 100, validation_split=0.25, shuffle=True, callbacks = callback)

		# check
		if str(history.history['loss'][len(history.history['loss'])-1]) == 'nan':
			lr /= 10
			rag *= 10

		# test
		test_predictions =  model.predict(x_test_price)
		rate = 0
		for i in range(len(test_predictions)):
		    check = round(float(test_predictions[i][0]), 2) - float(y_test[i][0])
		    if -1*rag < check < rag:
		        rate += 1

		pred_rate = rate/len(test_predictions)*100
		print(f'Xác suất dự đoán đúng = {round(pred_rate, 2)}% Trong Khoản {rag}')

	# today
	today = X_Date[0][0]

	# price today
	price = list(X_price[0])

	# predict
	print('\n')
	end_day = int(input('Nhập Số Ngày Bạn Muốn Dự Đoán: '))
	day, month, year = today.split('/')
	day, month, year = int(day), int(month),int(year)

	newPrice_list = []
	newDate_list = []

	while end_day != 0:
		# predict
		price_pred = predict(price, model)

	    # tinh ngay`
		dayInMonth = DemSoNgayTrongThang(month, year)
		day += 1
		if day > dayInMonth:
		    day = 1
		    month += 1

		if month > 12:
		    month = 1
		    year += 1
		newDate_list.append(str(day)+'/'+str(month)+'/'+str(year))

		# tinh tien`
		price = price[1:]
		price.append(price_pred)
		newPrice_list.append(price_pred)

		# print
		print(f'\nGiá Của {Stock_Symbol} vào ngày {day}/{month}/{year} được dự đoán là: {price_pred}\n')

		end_day -= 1

	# save txt
	with open(f'Giá_Dự_Đoán_Của_{Stock_Symbol}_Ngày_{newDate_list[0]}.txt','w',encoding = 'utf-8') as f: f.write(f'Giá Dự Đoán: {newPrice_list[0]}')

	# show trading view
	plt.plot(newDate_list, newPrice_list)
	plt.ylabel('VND x 1.000')
	plt.xlabel('Day/Month/Year')
	plt.title(f'Giá Dự Đoán Của {Stock_Symbol}. [{today} Đến {day}/{month}/{year}]')
	plt.show()

	# save model
	model.save(fr'.\Save_model\PredictStock_{Stock_Symbol}.h5')

Stock_Symbol = input('\nNhập Mã Chứng Khoán Bạn Muốn Dự Đoán: ').upper()
if check_existModel(Stock_Symbol) == True:
	print('\nĐã Tìm Thấy 1 Model!\n')
	confrim_predict = input('Dự đoán mã này? [Y/N]').upper()
	if confrim_predict == 'Y':
		predict_stock(Stock_Symbol)
	else:
		reFit = input('Bạn muốn train lại mã này không? [Y/N]').upper()
		if reFit == 'Y':
			train_newModel(Stock_Symbol)
		else:
			exit()
else:
	print('\nBạn chưa từng train mã này!\n')
	train = input('Bạn muốn train mã này không? [Y/N]').upper()
	if train == 'Y':
			train_newModel(Stock_Symbol)
	else:
		exit()
