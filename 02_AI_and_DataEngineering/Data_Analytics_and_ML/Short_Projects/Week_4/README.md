# Wine Quality Prediction - Regression

## Overview
Predicted wine quality using physicochemical features from the UCI Red Wine dataset. Compared multiple regression models and selected the best-performing approach.

## Workflow
- Split data into training (80%) and test (20%) sets.
- Scaled features using `StandardScaler`.
- Trained Linear Regression, Decision Tree, and Random Forest models.
- Evaluated using 5-Fold Cross-Validation (RMSE).
- Tuned models with GridSearchCV and RandomizedSearchCV.

## Final Results
**Best Model:** Random Forest Regressor  
- Test RMSE: **0.5554**  
- 95% Confidence Interval: **[0.5010, 0.6049]**

## Conclusion
Random Forest achieved the lowest prediction error, with an average deviation of ~0.56 quality points. The model generalizes well and provides stable performance.
