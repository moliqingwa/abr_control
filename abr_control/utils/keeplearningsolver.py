import numpy as np
import time

import nengo


class KeepLearningSolver(nengo.solvers.Lstsq):
    """ Loads in weights from a file if they exist,
    otherwise returns weights generated with the Lstq solver."""

    def __init__(self, filename, weights=False):
        super(KeepLearningSolver, self).__init__(weights=weights)
        self.filename = filename

    def __call__(self, A, Y, rng=None, E=None):
        import os
        if os.path.isfile('./%s' % self.filename):
            print('Loading weights from %s' % self.filename)
            tstart = time.time()
            weights = np.load(self.filename)['weights'][-1].T
            print('weights shape: ', weights.shape)
            info = {'rmses': None,
                    'time': time.time() - tstart}
            if (weights.shape[0] != A.shape[1] or
                    weights.shape[1] != Y.shape[1]):
                raise Exception('Stored weights are not ' +
                                'correct shape for connection.')
        else:
            print('No weights file found, ' +
                  'generating with Lstsq solver')
            weights, info = \
                super(KeepLearningSolver, self).__call__(A, Y)

        return weights, info

