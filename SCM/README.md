Causal inference to investigate french electricity market
==============================


Main notebooks are 01-get_data_nuc.ipynb for data acquisition, 
04-evaluate_scm.ipynb for creation, fit and evaluation of structured causal model via DoWhy 
and 05-visualize_evaluation.ipynb for the visualization of the results from notebook 04. 
Notebooks 02 and 03 are more for visualization misc and exploration of the data. Notebook 06 and 07 explore the indirect causal impact of river flow and price difference between France and other countries.

Project Organization
------------

    |-- README.md                   <- The top-level README for developers using this project.
    |-- data
    |   |
    |   |-- raw                     <- The original, immutable data dump.
    |   |-- processed               <- final data
    |       |
    |       |-- combined_data       <- final Data set used for all analysis 
    |
    |-- models                      <- Structural causal models. results from evaluate_scm notebook.
    |   |
    |   |-- model18                 <- results for the scm with price_da as target
    |   |-- model22                 <- results for the scm with net_export as target
    |   
    |-- notebooks                   <- Jupyter notebooks. Number for ordering. 
    |   |
    |   |-- scripts                 <- functions that the notebooks use. utils.py and countries.py are used by almost every 
    |                                   notebook.
    |
    |-- reports  
    |   |
    |   |-- figures                 <- Generated graphics and figures to be used in reporting. 
    |   |                               visualization of the causal model is in the folder "model_evaluation"  
    |
    |-- conda_env.yml           <- The environment file for reproducing the analysis environment, e.g.
    │                                   generated with `pip freeze > requirements.txt` 
    |-- sources.ods                 <- Table of all data sources  

Installation
------------

An environment can be created via conda_env.yml. We used miniforge.
The ENTSO-E transparency platform provides data needed for the analysis.
To get access to the ENTSO-E transperancy platform a .env.txt (saved at ../.env.txt) needs to be added containing an API-key.
To register for ENTSO-E and get an API-key go to ([ENTSO-E transparency platform](https://www.entsoe.eu/data/transparency-platform/)).

First the folder structure needs to be constructed by running the second cell after imports "create necessary folders".
of notebook 01-get_data_nuc.ipynb.

Secondly some data needs to be downloaded manually.


- Installed nuclear capacity France
    - download from  [ENTSO-E transparency platform](https://transparency.entsoe.eu/generation/r2/installedGenerationCapacityAggregation/show?name=&defaultValue=false&viewType=TABLE&areaType=BZN&atch=false&dateTime.dateTime=01.01.2015+00:00|UTC|YEAR&dateTime.endDateTime=01.01.2025+00:00|UTC|YEAR&area.values=CTY|10YFR-RTE------C!BZN|10YFR-RTE------C&productionType.values=B01&productionType.values=B25&productionType.values=B02&productionType.values=B03&productionType.values=B04&productionType.values=B05&productionType.values=B06&productionType.values=B07&productionType.values=B08&productionType.values=B09&productionType.values=B10&productionType.values=B11&productionType.values=B12&productionType.values=B13&productionType.values=B14&productionType.values=B20&productionType.values=B15&productionType.values=B16&productionType.values=B17&productionType.values=B18&productionType.values=B19#)
    - save as .csv file under path *../data/raw/na/installed_capacity_production_type_FR_2018-2023.csv* (paths["na_installed_cap"] in 01-get_data_nuc.ipynb).
- Carbon price France
    - download both ETS and carbon tax of France from [worldbank.org](https://carbonpricingdashboard.worldbank.org/compliance/price)
    - save as .csv file under path *../data/raw/price/carbonprice.csv* (paths["carbon_price_raw"] in 01-get_data_nuc.ipynb)
- Gas price
    - please contact authors for data access
    - save as .xlsx file under path *../data/raw/price/Price+History_20241019_2220.xlsx* (paths["gas_price_raw"] in 01-get_data_nuc.ipynb)
- Public holidays of France
    - download from [data.gouv.fr](https://www.data.gouv.fr/en/datasets/jours-feries-en-france/) (Toutes zones)
    - save as .csv file under path *../data/raw/france_holiday.csv* (paths["FR_holiday_raw"] in 01-get_data_nuc.ipynb)
- Production of electricity and derived heat by type of fuel in GWh
    - download from [nrg_bal_peh](https://ec.europa.eu/eurostat/databrowser/explore/all/envir?lang=en&subtheme=nrg.nrg_quant.nrg_quanta&display=list&sort=category)
    - save as .tsv file under path *../data/raw/nrg_bal_peh_el_prod_by_fuel.tsv*
    
After that the rest of 01-get_data_nuc.ipynb can be executed. Execution times may vary with internet connection.
For reference in our case a complete runthrough takes 3-4h (with nuclear availability taking the longest: 2h).

After that all necessary data is provided.

The notebook 04-evaluate_scm.ipynb can be used for creation, fit and evaluation of structured causal model via DoWhy. 
Here the option with_falsification = TRUE, allows for a more precise falsification of the model, while the standard evaluation 
is faster but less precise. Due to random permutations the exact number of LMC violations can vary in falsification, but this should not impact  that the original graph shows fewer LMC violations than the permuted graphs. In general running notebook 04_evaluate_scm.ipynb requires significant RAM and time.
After running notebook 04-evaluate_scm.ipynb, 05-visualize_evaluation.ipynb can be used for the visualization of the results from notebook 04.

Authors & Acknowledgements
-------------------
- Anton Tausendfreund - software developement
- Sarah Schreyer - software developement

#### Special Thanks
- to [James Brennan](https://james-brennan.github.io/posts/fast_gridding_geopandas/) for his code of fast gridding options. 

- to the DoWhy library 
    - Amit Sharma, Emre Kiciman. DoWhy: An End-to-End Library for Causal Inference. 2020. https://arxiv.org/abs/2011.04216

    - Patrick Blöbaum, Peter Götz, Kailash Budhathoki, Atalanti A. Mastakouri, Dominik Janzing. DoWhy-GCM: An extension of DoWhy for causal inference in graphical causal models. 2024. MLOSS 25(147):1−7. https://jmlr.org/papers/v25/22-1258.html

