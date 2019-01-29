import numpy
from scipy.signal import bilinear


def A_weighting(fs):

    # Definition of analog A-weighting filter according to IEC/CD 1672.
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    A1000 = 1.9997

    NUMs = [(2*numpy.pi * f4)**2 * (10**(A1000/20)), 0, 0, 0, 0]

    DENs = numpy.polymul([1, 4*numpy.pi * f4, (2*numpy.pi * f4)**2],
                   [1, 4*numpy.pi * f1, (2*numpy.pi * f1)**2])

    DENs = numpy.polymul(numpy.polymul(DENs, [1, 2*numpy.pi * f3]),
                                 [1, 2*numpy.pi * f2])

    return bilinear(NUMs, DENs, fs)



def rms_flat(a):
    return numpy.sqrt(numpy.mean(numpy.absolute(a)**2))