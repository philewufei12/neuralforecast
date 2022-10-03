# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/losses.ipynb.

# %% auto 0
__all__ = ['MAE', 'MSE', 'RMSE', 'MAPE', 'SMAPE', 'MASE', 'QuantileLoss', 'MQLoss', 'wMQLoss']

# %% ../nbs/losses.ipynb 4
import torch

# %% ../nbs/losses.ipynb 5
def _divide_no_nan(a, b):
    """
    Auxiliary funtion to handle divide by 0
    """
    div = a / b
    div[div != div] = 0.0
    div[div == float('inf')] = 0.0
    return div

# %% ../nbs/losses.ipynb 8
class MAE:
    
    def __init__(self):
        """Mean Absolute Error

        Calculates Mean Absolute Error between
        y and y_hat. MAE measures the relative prediction
        accuracy of a forecasting method by calculating the
        deviation of the prediction and the true
        value at a given time and averages these devations
        over the length of the series.
        
        $$ \mathrm{MAE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = 
            \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} 
            |y_{\\tau} - \hat{y}_{\\tau}| $$
        """
        pass

    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>
        
        **Returns:**<br>
        `mae`: tensor (single value).
        """
        if mask is None:
            mask = torch.ones_like(y)

        mae = torch.abs(y - y_hat) * mask
        mae = torch.mean(mae)
        return mae

# %% ../nbs/losses.ipynb 12
class MSE:
    
    def __init__(self):
        """  Mean Squared Error

        Calculates Mean Squared Error between
        y and y_hat. MSE measures the relative prediction
        accuracy of a forecasting method by calculating the 
        squared deviation of the prediction and the true
        value at a given time, and averages these devations
        over the length of the series.
        
        $$ \mathrm{MSE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = 
            \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} (y_{\\tau} - \hat{y}_{\\tau})^{2} $$
        """
        pass
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mse`: tensor (single value).
        """
        if mask is None:
            mask = torch.ones_like(y_hat)

        mse = (y - y_hat)**2
        mse = mask * mse
        mse = torch.mean(mse)
        return mse

# %% ../nbs/losses.ipynb 16
class RMSE:
    
    def __init__(self):
        """ Root Mean Squared Error

        Calculates Root Mean Squared Error between
        y and y_hat. RMSE measures the relative prediction
        accuracy of a forecasting method by calculating the squared deviation
        of the prediction and the observed value at a given time and
        averages these devations over the length of the series.
        Finally the RMSE will be in the same scale
        as the original time series so its comparison with other
        series is possible only if they share a common scale. 
        RMSE has a direct connection to the L2 norm.
        
        $$ \mathrm{RMSE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = 
            \\sqrt{\\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} (y_{\\tau} - \hat{y}_{\\tau})^{2}} $$
        """
        pass
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `rmse`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        mse = (y - y_hat)**2
        mse = mask * mse
        mse = torch.mean(mse)
        mse = torch.sqrt(mse)
        return mse

# %% ../nbs/losses.ipynb 21
class MAPE:
    
    def __init__(self):
        """ Mean Absolute Percentage Error

        Calculates Mean Absolute Percentage Error  between
        y and y_hat. MAPE measures the relative prediction
        accuracy of a forecasting method by calculating the percentual deviation
        of the prediction and the observed value at a given time and
        averages these devations over the length of the series.
        The closer to zero an observed value is, the higher penalty MAPE loss
        assigns to the corresponding error.
        
        $$ \mathrm{MAPE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = 
            \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1}
            \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{|y_{\\tau}|} $$
        """
        pass
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mape`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        mask = _divide_no_nan(mask, torch.abs(y))
        mape = torch.abs(y - y_hat) * mask
        mape = torch.mean(mape)
        return mape

# %% ../nbs/losses.ipynb 26
class SMAPE:
    def __init__(self):
        """ Symmetric Mean Absolute Percentage Error
        
        Calculates Symmetric Mean Absolute Percentage Error between
        y and y_hat. SMAPE measures the relative prediction
        accuracy of a forecasting method by calculating the relative deviation
        of the prediction and the observed value scaled by the sum of the
        absolute values for the prediction and observed value at a
        given time, then averages these devations over the length
        of the series. This allows the SMAPE to have bounds between
        0% and 200% which is desireble compared to normal MAPE that
        may be undetermined when the target is zero.
        
        $$ \mathrm{sMAPE}_{2}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}) = 
        \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} 
        \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{|y_{\\tau}|+|\hat{y}_{\\tau}|} $$
        """
        pass
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `smape`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        delta_y = torch.abs((y - y_hat))
        scale = torch.abs(y) + torch.abs(y_hat)
        smape = _divide_no_nan(delta_y, scale)
        smape = smape * mask
        smape = 2 * torch.mean(smape)
        return smape

# %% ../nbs/losses.ipynb 31
class MASE:
    
    def __init__(self, seasonality: int):
        """ Mean Absolute Scaled Error 
        Calculates the Mean Absolute Scaled Error between
        y and y_hat. MASE measures the relative prediction
        accuracy of a forecasting method by comparinng the mean absolute errors
        of the prediction and the observed value against the mean
        absolute errors of the seasonal naive model.
        The MASE partially composed the Overall Weighted Average (OWA), 
        used in the M4 Competition.
        
        $$ \mathrm{MASE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}_{\\tau}, \\mathbf{\hat{y}}^{season}_{\\tau}) = 
            \\frac{1}{H} \sum^{t+H}_{\\tau=t+1} \\frac{|y_{\\tau}-\hat{y}_{\\tau}|}{\mathrm{MAE}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{season}_{\\tau})} $$

        **Parameters:**<br>
        `seasonality`: int. Main frequency of the time series; Hourly 24,  Daily 7, Weekly 52, Monthly 12, Quarterly 4, Yearly 1.
        """
        self.seasonality = seasonality
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor,  y_insample: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor (batch_size, output_size), Actual values.<br>
        `y_hat`: tensor (batch_size, output_size)), Predicted values.<br>
        `y_insample`: tensor (batch_size, input_size), Actual insample Seasonal Naive predictions.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mase`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        delta_y = torch.abs(y - y_hat)
        scale = torch.mean(torch.abs(y_insample[:, self.seasonality:] - \
                                     y_insample[:, :-self.seasonality]), axis=1)
        mase = _divide_no_nan(delta_y, scale[:, None])
        mase = mase * mask
        mase = torch.mean(mase)
        return mase

# %% ../nbs/losses.ipynb 37
class QuantileLoss:
    
    def __init__(self, q):
        """ Quantile Loss
    
        Computes the quantile loss between y and y_hat. 
        QL measures the deviation of a quantile forecast.
        By weighting the absolute deviation in a non symmetric way, the
        loss pays more attention to under or over estimation.
        A common value for q is 0.5 for the deviation from the median (Pinball loss).

        $$ \mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q)}_{\\tau}) = 
            \\frac{1}{H} \\sum^{t+H}_{\\tau=t+1} 
            \Big( (1-q)\,( \hat{y}^{(q)}_{\\tau} - y_{\\tau} )_{+} 
            + q\,( y_{\\tau} - \hat{y}^{(q)}_{\\tau} )_{+} \Big) $$

        **Parameters:**<br>
        `q`: float, between 0 and 1. The slope of the quantile loss, in the context of quantile regression, the q determines the conditional quantile level.<br>
        """
        self.q = q
    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `quantile_loss`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        delta_y = y - y_hat
        loss = torch.max(torch.mul(self.q, delta_y), torch.mul((self.q - 1), delta_y))
        loss = loss * mask
        quantile_loss = torch.mean(loss)
        return quantile_loss

# %% ../nbs/losses.ipynb 42
class MQLoss:
    
    def __init__(self, quantiles):
        """  Multi-Quantile loss
    
        Calculates the Multi-Quantile loss (MQL) between y and y_hat. 
        MQL calculates the average multi-quantile Loss for
        a given set of quantiles, based on the absolute 
        difference between predicted quantiles and observed values.
        
        $$ \mathrm{MQL}(\\mathbf{y}_{\\tau},
                        [\\mathbf{\hat{y}}^{(q_{1})}_{\\tau}, ... ,\hat{y}^{(q_{n})}_{\\tau}]) = 
        \\frac{1}{n} \\sum_{q_{i}} \mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q_{i})}_{\\tau}) $$
        
        The limit behavior of MQL allows to measure the accuracy 
        of a full predictive distribution $\mathbf{\hat{F}}_{\\tau}$ with 
        the continuous ranked probability score (CRPS). This can be achieved 
        through a numerical integration technique, that discretizes the quantiles 
        and treats the CRPS integral with a left Riemann approximation, averaging over 
        uniformly distanced quantiles.    
        
        $$ \mathrm{CRPS}(y_{\\tau}, \mathbf{\hat{F}}_{\\tau}) = 
            \int^{1}_{0} \mathrm{QL}(y_{\\tau}, \hat{y}^{(q)}_{\\tau}) dq $$

        **Parameters:**<br>
        `quantiles`: tensor(n_quantiles). Quantiles to estimate from the distribution of y. 
        """
        assert len(quantiles) > 1, f'your quantiles are of len: {len(quantiles)}'
        self.quantiles = quantiles

    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mqloss`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        n_q = len(self.quantiles)
        
        error  = y_hat - y.unsqueeze(-1)
        sq     = torch.maximum(-error, torch.zeros_like(error))
        s1_q   = torch.maximum(error, torch.zeros_like(error))
        mqloss = (self.quantiles * sq + (1 - self.quantiles) * s1_q)
            
        # Match y/weights dimensions and compute weighted average
        mask = mask / torch.sum(mask)
        mask = mask.unsqueeze(-1)
        mqloss = (1/n_q) * mqloss * mask
        return torch.sum(mqloss)

# %% ../nbs/losses.ipynb 47
class wMQLoss:
    
    def __init__(self, quantiles):
        """ Weighted Multi-Quantile loss
        
        Calculates the Weighted Multi-Quantile loss (WMQL) between y and y_hat. 
        WMQL calculates the weighted average multi-quantile Loss for
        a given set of quantiles, based on the absolute 
        difference between predicted quantiles and observed values.  
            
        $$ \mathrm{WMQL}(\\mathbf{y}_{\\tau},
                        [\\mathbf{\hat{y}}^{(q_{1})}_{\\tau}, ... ,\hat{y}^{(q_{n})}_{\\tau}]) = 
        \\frac{1}{n} \\sum_{q_{i}} 
            \\frac{\mathrm{QL}(\\mathbf{y}_{\\tau}, \\mathbf{\hat{y}}^{(q_{i})}_{\\tau})}
                {\\sum^{t+H}_{\\tau=t+1} |y_{\\tau}|} $$
        
        **Parameters:**<br>
        `quantiles`: tensor(n_quantiles). Quantiles to estimate from the distribution of y. 
        """
        assert len(quantiles) > 1, f'your quantiles are of len: {len(quantiles)}'
        self.quantiles = quantiles

    
    def __call__(self, y: torch.Tensor, y_hat: torch.Tensor, mask: torch.Tensor = None):
        """
        **Parameters:**<br>
        `y`: tensor, Actual values.<br>
        `y_hat`: tensor, Predicted values.<br>
        `mask`: tensor, Specifies date stamps per serie to consider in loss.<br>

        **Returns:**<br>
        `mqloss`: tensor (single value).
        """
        if mask is None: 
            mask = torch.ones_like(y_hat)

        error = y_hat - y.unsqueeze(-1)
        
        sq = torch.maximum(-error, torch.zeros_like(error))
        s1_q = torch.maximum(error, torch.zeros_like(error))
        loss = (self.quantiles * sq + (1 - self.quantiles) * s1_q)
        
        wmqloss = _divide_no_nan(torch.sum(loss * mask, axis=-2), 
                                 torch.sum(torch.abs(y.unsqueeze(-1)) * mask, axis=-2))
        return torch.mean(wmqloss)
