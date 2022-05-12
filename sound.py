from headers import *

###############################################################################
# class that generates a sound from a given power spectrum

class Sound(object):

   def __init__(self):
      pass


   def writeSound(self, fPowerSpectrum, duration=5., name="test"):
      """takes a 1d power spectrum as input
      generates and saves a wav sound with the given power spectrum
      See http://en.wikipedia.org/wiki/Bit_rate#Audio
      nuMin, nuMax: frequency range to hear, in Hz
      duration: seconds
      """
      #number of frames per second
      bitRate = 44100
      
      # number of useful / empty frames
      nFrame = int(bitRate * duration)
      
      frame = np.arange(nFrame)  # in Hz
      time = frame.astype(float) / bitRate  # in sec
      
      ##################################################################
      # generate random noise in Fourier space, with desired power spectrum
      
      # frequencies present in the signal
      # use only half the nb of frame, because only positive frequencies here,
      # since the time-signal is real
      Nu = np.arange(nFrame//2+1) / duration # frequencies in Hz
      
      # Generate Gaussian noise signal in Fourier space
      fRandomGauss = lambda var: np.random.normal(0., scale=np.sqrt(var)+1.e-10) * np.exp(1j*np.random.uniform(0., 2.*np.pi))
      fFourier = lambda nu: fRandomGauss(fPowerSpectrum(nu))
      fourier = np.array(list(map(fFourier, Nu)))
      # guarantee that the Fourier signal at nu=0 is hermitian, e.g. zero
      fourier[0] = 0.
      
#      var = np.array(list(map(fPowerSpectrum, Nu)))
#      plt.semilogx(Nu, np.real(fourier), 'r.', alpha=0.5)
#      plt.semilogx(Nu, np.imag(fourier), 'b.', alpha=0.5)
#      plt.semilogx(Nu, np.sqrt(var), 'k')
#      plt.semilogx(Nu, -np.sqrt(var), 'k')
#      plt.semilogx(Nu, 2.*np.sqrt(var), 'k')
#      plt.semilogx(Nu, -2.*np.sqrt(var), 'k')
#      plt.show()

      
      
      ##################################################################
      # get sound amplitude in real space
      
      amplitude = np.fft.irfft(fourier)
      
      ##################################################################
      # save to wav file
      
#      print np.min(amplitude), np.max(amplitude)

      # convert amplitude to [-1, 1]
      amplitude = 1.*(amplitude-np.min(amplitude)) / (np.max(amplitude)-np.min(amplitude)) - 1.*(amplitude-np.max(amplitude)) / (np.min(amplitude)-np.max(amplitude))
 
#      plt.plot(time, amplitude, 'b')
#      plt.show()

      # convert to int32, in [-2147483648, 2147483647]
      amplitude = - 0.5 + 2147483647.5 * amplitude
      amplitude = np.int32(amplitude)
      
      # create wav file
      wavfile.write("./output/sound/"+name+"_"+str(int(duration))+"sec.wav", bitRate, amplitude)
      return



