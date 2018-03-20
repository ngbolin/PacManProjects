# perceptron_pacman.py
# --------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation for apprenticeship learning
import util
import operator
from perceptron import PerceptronClassifier
from pacman import GameState

PRINT = True


class PerceptronClassifierPacman(PerceptronClassifier):
    def __init__(self, legalLabels, maxIterations):
        PerceptronClassifier.__init__(self, legalLabels, maxIterations)
        self.weights = util.Counter()

    def classify(self, data ):
        """
        Data contains a list of (datum, legal moves)

        Datum is a Counter representing the features of each GameState.
        legalMoves is a list of legal moves for that GameState.
        """
        guesses = []
        for datum, legalMoves in data:
            vectors = util.Counter()
            for l in legalMoves:
                vectors[l] = self.weights * datum[l] #changed from datum to datum[l]
            guesses.append(vectors.argMax())
        return guesses


    def train( self, trainingData, trainingLabels, validationData, validationLabels ):
        self.features = trainingData[0][0]['Stop'].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.

        bestScore = float('-inf')
        bestWeights = {}

        for iteration in range(self.max_iterations):
            print "Starting iteration ", iteration, "..."
            for i in range(len(trainingData)):
                "*** YOUR CODE HERE ***"
                datum, legalMoves = trainingData[i]
                actualAction = trainingLabels[i]

                actionScore = util.Counter()
                for l in legalMoves:
                    for feature in self.features:
                        actionScore[l] += self.weights * datum[l]
                predictedAction = actionScore.sortedKeys()[0]

                if predictedAction == actualAction: continue
                else:
                    for feature in self.features:
                        self.weights -= datum[predictedAction]
                        self.weights += datum[actualAction]

            # Performance on validation dataset
            predictedValidationLabels = self.classify(validationData)
            accuracyScore = 0
            for j in range(len(validationData)):
                if predictedValidationLabels[j] == validationLabels[j]: accuracyScore += 1

            accuracyScore /= len(validationData)

            if accuracyScore > bestScore:
                bestScore = accuracyScore
                bestWeights = self.weights.copy()
            else:
                self.weights = bestWeights.copy()
                break