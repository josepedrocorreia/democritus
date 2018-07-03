from builtins import range

import matplotlib.cm as cm
import numpy as np

from democritus import utils


class ElementSet(object):
    def __init__(self, elements):
        self.elements = elements

    def size(self):
        return len(self.elements)

    def index(self, element):
        return self.elements.index(element)


class ElementSetWithPriors(ElementSet):
    def __init__(self, elements, priors):
        ElementSet.__init__(self, elements)
        self.priors = utils.make_stochastic(np.array(priors))
        if len(self.elements) != len(self.priors):
            raise ValueError('Number of elements and priors should be the same. '
                             'Supplied %s elements and %s priors.' % (len(self.elements), len(self.priors)))

    def get_prior(self, x):
        x_index = self.index(x)
        return self.priors[x_index]


class MetricSpace(ElementSet):
    def __init__(self, elements, metric):
        ElementSet.__init__(self, elements)
        self.distances = np.array(metric)
        if self.distances.shape[0] != len(self.elements) or self.distances.shape[1] != len(self.elements):
            raise ValueError('Incorrect dimensions of metric. '
                             'Metric should be square matrix of order %s.' % len(self.elements))

    def distance(self, x, y):
        x_index = self.index(x)
        y_index = self.index(y)
        return self.distances[x_index, y_index]


class StateSet(ElementSetWithPriors):
    def plot(self, axis):
        axis.plot(self.elements, self.priors, marker='.')
        axis.set_ylim(bottom=0)


class StateMetricSpace(StateSet, MetricSpace):
    def __init__(self, elements, priors, metric):
        StateSet.__init__(self, elements, priors)
        MetricSpace.__init__(self, elements, metric)


class WCSMunsellPalette(StateMetricSpace):
    wcs_values = list('ABCDEFGHIJ')
    wcs_hue_key = 'wcs.hue'
    wcs_value_key = 'wcs.value'

    def plot(self, axis):
        probabilities = np.full((10, 41), np.nan)
        for chip_index in range(len(self.elements)):
            chip = self.elements[chip_index]
            wcs_value_index = WCSMunsellPalette.wcs_values.index(chip[WCSMunsellPalette.wcs_value_key])
            wcs_hue_index = chip[WCSMunsellPalette.wcs_hue_key]
            probabilities[wcs_value_index, wcs_hue_index] = self.priors[chip_index]
        axis.imshow(probabilities, origin='upper', interpolation='none')
        axis.axis('off')


class MessageSet(ElementSet):
    pass


class ActionSet(ElementSet):
    pass


class BivariateFunction(object):
    def __init__(self, values):
        self.values = np.array(values)
        if len(self.values.shape) != 2:
            raise ValueError('Values for bivariate function should be two-dimensional.')

    def __getitem__(self, index):
        return self.values[index]

    def __setitem__(self, index, value):
        self.values[index] = value

    def __len__(self):
        return len(self.values)

    def make_row_stochastic(self):
        self.values = utils.make_row_stochastic(self.values)

    def plot(self, axis):
        axis.imshow(self.values, origin='upper', interpolation='none')


class BehavioralStrategy(BivariateFunction):
    def __init__(self, choice_points, choices, probabilities):
        BivariateFunction.__init__(self, probabilities)
        self.probabilities = self.values
        self.make_row_stochastic()
        self.choice_points = choice_points
        self.choices = choices
        if self.values.shape[0] != self.choice_points.size() or self.values.shape[1] != self.choices.size():
            raise ValueError('Incorrect dimensions for probabilities, should accord with choice points and choices. '
                             'There are %s choice points, %s choices, '
                             'but probabilities have dimensions %s.' %
                             (self.choice_points.size(), self.choices.size(), self.values.shape))


class SenderStrategy(BehavioralStrategy):
    def __init__(self, states, messages, probabilities):
        BehavioralStrategy.__init__(self, states, messages, probabilities)
        self.states = self.choice_points
        self.messages = self.choices

    def plot(self, axis):
        for m in range(self.messages.size()):
            axis.plot(self.states.elements, self.values[:, m],
                      label='$' + str(self.messages.elements[m]) + '$',
                      marker='.')
        axis.set_ylim(-0.1, 1.1)
        axis.legend(loc='lower left')


class WCSMunsellSenderStrategy(SenderStrategy):
    def plot(self, axis):
        color_map = cm.get_cmap('Set1')
        probabilities = np.array([[color_map.colors[0] + (0,)] * 41] * 10)
        for chip_index in range(len(self.states.elements)):
            chip = self.states.elements[chip_index]
            wcs_value_index = WCSMunsellPalette.wcs_values.index(chip[WCSMunsellPalette.wcs_value_key])
            wcs_hue_index = chip[WCSMunsellPalette.wcs_hue_key]
            message_index = np.argmax(self.values[chip_index])
            probability = self.values[chip_index, message_index]
            color = color_map.colors[message_index] + (probability,)
            probabilities[wcs_value_index, wcs_hue_index] = color
        axis.imshow(probabilities, origin='upper', interpolation='none')
        # axis.axis('off')


class ReceiverStrategy(BehavioralStrategy):
    def __init__(self, messages, actions, probabilities):
        BehavioralStrategy.__init__(self, messages, actions, probabilities)
        self.messages = self.choice_points
        self.actions = self.choices

    def plot(self, axis):
        for m in range(self.messages.size()):
            axis.plot(self.actions.elements, self.values[m, :],
                      label='$' + str(self.messages.elements[m]) + '$',
                      marker='.')
        axis.set_ylim(ymin=0)
        axis.legend(loc='lower left')


class WCSMunsellReceiverStrategy(ReceiverStrategy):
    def plot(self, axis):
        color_map = cm.get_cmap('Set1')
        probabilities = np.array([[color_map.colors[0] + (0,)] * 41] * 10)
        for chip_index in range(len(self.actions.elements)):
            chip = self.actions.elements[chip_index]
            wcs_value_index = WCSMunsellPalette.wcs_values.index(chip[WCSMunsellPalette.wcs_value_key])
            wcs_hue_index = chip[WCSMunsellPalette.wcs_hue_key]
            message_index = np.argmax(self.values[:, chip_index])
            probability = self.values[message_index, chip_index]
            color = color_map.colors[message_index] + (probability,)
            probabilities[wcs_value_index, wcs_hue_index] = color
        axis.imshow(probabilities, origin='upper', interpolation='none')
        # axis.axis('off')
