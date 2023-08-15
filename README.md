[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/trustyai-explainability/trustyai-explainability-python-examples/main?labpath=examples)
# trustyai-examples

Examples for the [Python bindings](https://github.com/trustyai-explainability/trustyai-explainability-python) to [TrustyAI](https://github.com/trustyai-explainability/trustyai-explainability)'s explainability library.

## Binder

You can run the example Jupyter notebooks using `mybinder.org` by following [this link](https://mybinder.org/v2/gh/trustyai-explainability/trustyai-explainability-python-examples/main?labpath=examples).

## Jupyter notebooks

Several example Jupyter notebooks are available.

### Explainers

- [Counterfactual explanations](examples/Counterfactuals.ipynb)
- [LIME explanations](examples/Lime.ipynb)
- [SHAP explanations](examples/SHAP.ipynb)
- [PDP explanations](examples/PDP.ipynb) 
- Time-series explainers
  - [TSLime](examples/TSLime.ipynb)[^1]
  - [TSSaliency](examples/TSSaliency.ipynb)[^1]
  - [Time-series Individual Conditional Expectation (TSICE)](examples/TSICE.ipynb)[^1]
  - Full examples
    - [Energy load forecasting](examples/EnergyLoadForecasting.ipynb)[^1]
    - [Engine fault detection](examples/EngineFaultDetection.ipynb)[^1]

### Fairness metrics

- [Group fairness metrics](examples/GroupFairnessMetrics.ipynb)



[^1]: These explainers require the extra dependencies, installed with `pip install trustyai[extras]`.