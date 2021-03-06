import numpy as np
from scorer import Scorer

class LinearRegression(object):
    """
    Fits a dataset (X, y) using a linear model 
    
    Options
    ----------
    alpha : float, default: 0.01
        The learning rate for gradient descent.
        
    Returns
    -------
    X_norm : array_like
        The normalized dataset of shape (m x n).
    """
    
    def __init__(self, alpha_=0.01):
        self.alpha_ = alpha_
    
    def cost(self):
        """
        Compute cost and gradient for regularized linear regression 
        with multiple variables. Computes the cost of using theta as
        the parameter for linear regression to fit the data points in X and y. 
            
        Parameters
        ----------
        X : array_like
            The dataset. Matrix with shape (m x n + 1) where m is the 
            total number of examples, and n is the number of features 
            before adding the bias term.

        y : array_like
            The functions values at each datapoint. A vector of
            shape (m, ).

        w : array_like
            The parameters for linear regression. A vector of shape (n+1,).

        lambda_ : float, optional
            The regularization parameter.

        Returns
        -------
        C : float
            The value of the cost function.

        grad : array_like
            The value of the cost function gradient w.r.t theta. 
            A vector of shape (n+1, ).
                Returns

        Instructions
        ------------
        Compute the cost and gradient of regularized linear regression for
        a particular choice of theta.
        You should set J to the cost and grad to the gradient.
        """
        # Initialize some useful values
        m = self.y.size # number of training examples
        C = 0 # cost for each iteration

        y_hat = np.dot(self.X, self.w.T)
        C = (1/(2*m)) * np.sum((y_hat - self.y)**2) + (self.lambda_/(2*m))*np.sum(self.w[1:]**2)

        return C
    
    def gradient_descent(self):
        """
        Performs gradient descent to learn the weights w.
        Update weights by taking num_iters gradient steps with learning rate alpha.
    
        Returns
        -------
        cpi : list
            A python list for the values of the cost function after each iteration.
        """
        
        # Initialize some useful values
        m = self.y.size # number of training examples
        self.w = np.zeros(self.X.shape[1])
        cpi = dict()

        for i in range(self.num_iters):
            y_hat = np.dot(self.X, self.w.T)           
            
            w_ = self.w
            w_[0] = 0   # because we don't add anything for j = 0
            grad = (1/m) * np.dot(self.X.T, (y_hat - self.y))
            grad = grad + (self.lambda_/m)*w_
            self.w = self.w - self.alpha_*grad
            
            # save the cost C in dictionary for every 10th iteration
            if not np.remainder(i, 10):
                cpi[i] = self.cost()
        return cpi
    
    def normal_eqn(self):
        """
        Computes the closed-form solution to linear regression using the normal equations.

        Parameters
        ----------
        X : array_like
            The dataset of shape (m x n+1).

        y : array_like
            The value at each data point. A vector of shape (m, ).

        Returns
        -------
        w : array_like
            Estimated linear regression weights. A vector of shape (n+1, ).
        """
        self.w = np.zeros(self.X.shape[1])
        self.w = ((np.linalg.pinv(np.dot(self.X.T, self.X)))@self.X.T)@self.y
        
        return
    
    def fit(self, X, y, num_iters=100, lambda_=0.0, **kwargs):
        """ Fits a dataset (X, y) using a linear model 
    
        Parameters
        ----------
        X : array_like
            The dataset of shape (m x n).

        y : array_like
            A vector of shape (m, ) for the values at a given data point.
        
         Options
        ----------        
        lambda_ : float, optional
            The regularization parameter.
            
        num_iters : float, default: 100
            Number of iterations for gradient descent to converge

        Returns
        -------
        w : array_like
            The array of weights of shape (m x n).
        cpi: array_like
            Cost per iteration. The cost calculated over each iteration of gradient descent.

        """
        
        m = y.size # number of examples
        
        if X.ndim == 1: 
            #promote array to 2 dimension if array is a vector
            X = X[:, None]
            self.X = np.concatenate([np.ones((m, 1)), X], axis=1)
        else:
            self.X = np.concatenate([np.ones((m, 1)), X], axis=1)
        self.y = y
        self.num_iters = num_iters
        self.lambda_ = lambda_
        self.w = np.zeros(self.X.shape[1])
        
        if m < 10: 
            #use normal equation method
            self.normal_eqn()
            cpi = None
        else:
            #use gradient descent for m >100
            cpi = self.gradient_descent()    
        
        return {'w': self.w, 'cpi': cpi}
    
    def predict(self, X, y, score="rmse"):
        """ Find approximate values of arget variable using a learned model weights 
    
        Parameters
        ----------
        X : array_like
            The dataset of shape (m x n).

        y : array_like
            A vector of shape (m, ) for the values at a given data point.
        
         Options
        ----------        
        score : float
            The metrics for evaluating performance of model.
            
            - rmse : root mean squared error
            - mse : mean squared error

        Returns
        -------
        A dictionary of y_hat and score
        
        y_hat : array_like
            The array of predicted target for each example, shape (m x n).
        score: 
            - rmse or mse
        """
        m = X.shape[0]

        if X.ndim == 1: 
            #promote array to 2 dimension if array is a vector
            X = X[:, None]
            X = np.concatenate([np.ones((m, 1)), X], axis=1)
        else:
            X = np.concatenate([np.ones((m, 1)), X], axis=1)

        y_hat = np.dot(X, self.w.T)

        return y_hat
    
    def score(self, y, y_hat, score="rmse"):
        """ 
        Calculates score metrics for the learning algorithm.
        Parameters
        ----------
        X : array_like
            The dataset of shape (m x n).

        y : array_like
            A vector of shape (m, ) for the values at a given data point.

        Options
        ----------        
        type : string
            The type of metric to be used in evaluation.
            - rmse : root mean squared error
            - mse : mean squared error

        Returns
        -------
        score_metric: float
        """
        scorer = Scorer()
        if score == "rmse":   
            score_metric = scorer.rmse_(y, y_hat)
        elif score == "mse":
            score_metric = scorer.mse_(y, y_hat)

        return score_metric