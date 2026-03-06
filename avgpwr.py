# File : avgpwr.py

def plot(file_name, frequency, frequency_units):
	"""
	plot() takes in the file name (with .npz at the end), loads it, averages the power and plots it. 
	data_index = the specific block of data 
	frequency = the injected frequency signal / target frequency
	frequency_units = the units of the injected / captured frequency
	"""
	importdata = np.load(f"{file_name}")
	indexdata = importdata["arr_1"]
	print(importdata["arr_0"])
	data = indexdata[3]

	# Convert I/Q to complex data
	complexdata = data[:,0] + 1j * data[:,1]

	# FFT Parameters
	sampling_rate = 2.9e6
	N = len(complexdata)

	# Hann window + FFT
	window = np.hanning(N)
	fft_data = np.fft.fftshift(np.fft.fft(complexdata * window))

	# Power Spectrum
	power = np.abs(fft_data)**2
	power_db = 10 * np.log10(power)

	# Frequency axis (baseband)
	f = np.fft.fftshift(np.fft.fftfreq(N, d=1/sampling_rate))

	# Plotting
	plt.figure(figsize=(10, 4))
	plt.axvline(10, linestyle=":", color="black", linewidth=2) # expected signal location
	plt.plot(f / 1e3, power_db)
	plt.xlim(-200, 200)
	# plt.xlim()
	plt.xlabel("Frequency Offset (kHz)")
	plt.ylabel("Power (dB)")
	plt.title(f"Baseband Power Spectrum at {frequency} {frequency_units}(I/Q Data, Hann Window)")
	plt.grid(True)
	finalplot = plt.show()
	return finalplot
