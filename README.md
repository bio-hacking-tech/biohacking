# Digital biohacking approach on dietary interventions

## Description
This repository contains the implementation of the digital biohacking algorithm used to create personalized diets aimed at promoting sustainable weight loss and reducing environmental impact. The algorithm was developed and evaluated in a pilot study involving four participants, monitoring their weight, diet, and activities over a year.

## Features
- **Calorie Reduction:** Personalized dietary suggestions leading to an average daily reduction of 236.78 kcal (14.24%).
- **Environmental Impact Reduction:** An average reduction in carbon footprint of 15.12% (-736.48 gCO2eq) per participant.
- **Personalization:** Utilizes a Personalized Metabolic Avatar (PMA) to simulate weight changes and plan dietary interventions.
- **Diet-Adherence Correlation:** Linear regression analysis shows a significant correlation between adherence to the suggested diet and weight loss.

## Repository Structure
- `scripts/`: Contains Python scripts implementing the digital biohacking algorithm.

## Requirements
The computational requirements are minimal to allow deployment on virtual machines available on the web. The code was run in Google Colab with the default settings (free plan). The code requires the following libraries:
- TensorFlow 2.9.2 ([source](https://pypi.org/project/tensorflow/), accessed on 25 January 2024)
- pandas 1.3.5 ([source](https://pandas.pydata.org/), accessed on 25 January 2024)
- numpy 1.21.6 ([source](https://numpy.org/), accessed on 25 January 2024)
- matplotlib 3.2.2 ([source](https://matplotlib.org/), accessed on 25 January 2024)
- seaborn 0.11.2 ([source](https://seaborn.pydata.org/), accessed on 25 January 2024)
- statsmodels 0.12.2 ([source](https://www.statsmodels.org/stable/index.html), accessed on 25 January 2024)
- scipy 1.7.3 ([source](https://pypi.org/project/scipy/), accessed on 25 January 2024)
- scikit-learn 1.0.2 ([source](https://scikit-learn.org/stable/), accessed on 25 January 2024)
- scikit-posthocs 0.7.0 ([source](https://scikit-posthocs.readthedocs.io/en/latest/), accessed on 25 January 2024)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/biohacking.git
   cd digital-biohacking-diet

## License
This project is distributed under the MIT License. See the LICENSE file for more details.

## References
Reference article: "Abeltino, A.; Bianchetti, G.; Serantoni, C.; Ardito, C.F.; Malta, D.; De Spirito, M.; Maulucci, G. Personalized Metabolic Avatar: A Data Driven Model of Metabolism for Weight Variation Forecasting and Diet Plan Evaluation. Nutrients 2022, 14, 3520. https://doi.org/10.3390/nu14173520"

## Contact
For questions or more information, please contact Giuseppe Maulucci at giuseppe.maulucci@unicatt.it.
