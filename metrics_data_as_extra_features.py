# -*- coding: utf-8 -*-
"""metrics data as extra features.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ipPRxKxY8Ta_dPQVxJIrw1ExczsBA_C7
"""

!pip install --upgrade pip
!pip install --upgrade git+https://github.com/google/lightweight_mmm.git

import pandas as pd
from lightweight_mmm import preprocessing, lightweight_mmm, plot, optimize_media
import jax.numpy as jnp
from sklearn.metrics import mean_absolute_percentage_error
import jax.numpy as jnp
import numpyro
from lightweight_mmm import lightweight_mmm
from lightweight_mmm import optimize_media
from lightweight_mmm import plot
from lightweight_mmm import preprocessing
from lightweight_mmm import utils

ins_data = pd.read_csv("/content/instagram_processed_data.csv", usecols=["Impressions", "Reach", "Engaged Users", "Fan Growth", "Views", "Cost", "Consideration", "Awareness", "Engagement"])

yt_data = pd.read_csv("/content/youtube_processed_data.csv", usecols=["Impressions", "Reach", "Engaged Users", "Fan Growth", "Views", "Cost", "Consideration", "Awareness", "Engagement"])

fb_data = pd.read_csv("/content/facebook_processed_data.csv", usecols=["Lifetime Post Total Impressions", "Reach", "Engaged Users", "Fan Growth", "Views", "Cost", "Consideration", "Awareness", "Engagement"])

ins_data = ins_data[:398]

yt_data = yt_data[:398]



simulated_sales_data = utils.simulate_dummy_data(
    data_size=398,
    n_media_channels=3,
 n_extra_features=6)

sales_data = simulated_sales_data[2]

sales_data.shape

### Awareness as media data ###
# ins_media_data = ins_data[["Awareness"]]

# fb_media_data = fb_data[["Awareness"]]

# yt_media_data = yt_data[["Awareness"]]

# ins_cost_data = ins_data[["Cost"]]

# fb_cost_data = fb_data[["Cost"]]

# yt_cost_data = yt_data[["Cost"]]

# ins_extra_features_data = ins_data[["Engagement", "Consideration"]]

# fb_extra_features_data = fb_data[["Engagement", "Consideration"]]

# yt_extra_features_data = yt_data[["Engagement", "Consideration"]]

# ### Engagement as media data
# ins_media_data = ins_data[["Engagement"]]

# fb_media_data = fb_data[["Engagement"]]

# yt_media_data = yt_data[["Engagement"]]

# ins_cost_data = ins_data[["Cost"]]

# fb_cost_data = fb_data[["Cost"]]

# yt_cost_data = yt_data[["Cost"]]

# ins_extra_features_data = ins_data[["Awareness", "Consideration"]]

# fb_extra_features_data = fb_data[["Awareness", "Consideration"]]

# yt_extra_features_data = yt_data[["Awareness", "Consideration"]]


### Consideration as media data
ins_media_data = ins_data[["Consideration"]]

fb_media_data = fb_data[["Consideration"]]

yt_media_data = yt_data[["Consideration"]]

ins_cost_data = ins_data[["Cost"]]

fb_cost_data = fb_data[["Cost"]]

yt_cost_data = yt_data[["Cost"]]

ins_extra_features_data = ins_data[["Awareness", "Engagement"]]

fb_extra_features_data = fb_data[["Awareness", "Engagement"]]

yt_extra_features_data = yt_data[["Awareness", "Engagement"]]

len(ins_media_data)

# Reset index if the dataframes do not align properly
ins_media_data.reset_index(drop=True, inplace=True)
fb_media_data.reset_index(drop=True, inplace=True)
yt_media_data.reset_index(drop=True, inplace=True)

# Concatenate and rename columns
across_platform_media_data_df = pd.concat([fb_media_data, ins_media_data, yt_media_data], axis=1)
across_platform_media_data_df.columns = ['fb_media_data', 'ins_media_data', 'yt_media_data']

across_platform_media_data = across_platform_media_data_df.to_numpy()

across_platform_media_data

import numpy as np

# Calculate the mean of each column in media_data_train_scaled
column_means = np.mean(across_platform_media_data, axis=0)

# Replace negative values in each column with the corresponding mean
for i in range(across_platform_media_data.shape[1]):
    negative_indices = np.where(across_platform_media_data[:, i] <= 0)[0]
    across_platform_media_data[negative_indices, i] = column_means[i]

# Find the indices of negative values in media_data_train_scaled
negative_indices = np.where(across_platform_media_data <= 0)[0]

# Count the number of negative values
num_negative_values = len(negative_indices)

# Get the actual negative values
negative_values = across_platform_media_data[negative_indices]

# Print the results
print(f"Number of negative values: {num_negative_values}")
print(f"Negative values: {negative_values}")
print(f"Indices of negative values: {negative_indices}")

# Reset index if the dataframes do not align properly
ins_cost_data = ins_cost_data.sum(axis=0)
fb_cost_data = fb_cost_data.sum(axis=0)
yt_cost_data = yt_cost_data.sum(axis=0)

import numpy as np
across_platform_cost_data = np.concatenate([fb_cost_data, ins_cost_data, yt_cost_data], axis=0)

across_platform_cost_data

# ### Awareness as media data
# # Reset index if the dataframes do not align properly
# ins_extra_features_data.reset_index(drop=True, inplace=True)
# fb_extra_features_data.reset_index(drop=True, inplace=True)
# yt_extra_features_data.reset_index(drop=True, inplace=True)

# # Concatenate and rename columns
# across_platform_extra_features_data_df = pd.concat([fb_extra_features_data, ins_extra_features_data, yt_extra_features_data], axis=1)
# across_platform_extra_features_data_df.columns = ['fb_engagement_data', 'fb_consideration_data','ins_engagement_data', 'ins_consideration_data','yt_engagement_data', 'yt_consideration_data']

# ### Engagement as media data
# # Reset index if the dataframes do not align properly
# ins_extra_features_data.reset_index(drop=True, inplace=True)
# fb_extra_features_data.reset_index(drop=True, inplace=True)
# yt_extra_features_data.reset_index(drop=True, inplace=True)

# # Concatenate and rename columns
# across_platform_extra_features_data_df = pd.concat([fb_extra_features_data, ins_extra_features_data, yt_extra_features_data], axis=1)
# across_platform_extra_features_data_df.columns = ['fb_awareness_data', 'fb_consideration_data','ins_awareness_data', 'ins_consideration_data','yt_awareness_data', 'yt_consideration_data']

### Consideration as media data
# Reset index if the dataframes do not align properly
ins_extra_features_data.reset_index(drop=True, inplace=True)
fb_extra_features_data.reset_index(drop=True, inplace=True)
yt_extra_features_data.reset_index(drop=True, inplace=True)

# Concatenate and rename columns
across_platform_extra_features_data_df = pd.concat([fb_extra_features_data, ins_extra_features_data, yt_extra_features_data], axis=1)
across_platform_extra_features_data_df.columns = ['fb_awareness_data', 'fb_engagement_data','ins_awareness_data', 'ins_engagement_data','yt_awareness_data', 'yt_engagement_data']

across_platform_extra_features_data = across_platform_extra_features_data_df.to_numpy()
across_platform_extra_features_data

import numpy as jnp
from sklearn.impute import SimpleImputer

# Create an imputer
imputer = SimpleImputer(missing_values=jnp.nan, strategy="mean")

# Impute missing values
sales_data = imputer.fit_transform(sales_data.reshape(-1, 1)).ravel()

# sales_data_reshaped = sales_data.reshape(-1, 1)

media_data_train = across_platform_media_data[:300]
media_data_test = across_platform_media_data[300:]
target_data_train = sales_data[:300]
target_data_test = sales_data[300:]
cost_data_train = across_platform_cost_data
extra_features_data_train = across_platform_extra_features_data[:300]
extra_features_data_test = across_platform_extra_features_data[300:]

cost_data_train

media_data_train.shape

target_data_train.shape

extra_features_data_train.shape

target_data_test

media_scaler = preprocessing.CustomScaler(divide_operation=jnp.mean)
target_scaler = preprocessing.CustomScaler(
    divide_operation=jnp.mean)
cost_scaler = preprocessing.CustomScaler(divide_operation=jnp.mean)
extra_features_scaler = preprocessing.CustomScaler(divide_operation=jnp.mean)

media_data_train_scaled = media_scaler.fit_transform(media_data_train)
target_train_scaled = target_scaler.fit_transform(target_data_train)
# target_train_scaled1 = target_scaler.fit_transform(target_data_train1)
costs_scaled = cost_scaler.fit_transform(cost_data_train)
extra_features_scaled = extra_features_scaler.fit_transform(extra_features_data_train)

media_data_test_scaled = media_scaler.transform(media_data_test)
extra_features_test_scaled = extra_features_scaler.fit_transform(extra_features_data_test)

target_data_test

import jax.numpy as jnp
import numpyro
import numpyro.distributions as dist

loc=extra_features_scaled
scale=jnp.std(extra_features_scaled)
#print("loc values:", loc)
# Ensure there are no NaNs or infinite values
assert jnp.all(jnp.isfinite(loc)), "loc contains non-finite values!"
assert jnp.all(jnp.isfinite(scale)), "scale contains non-finite values!"

# Creating a Normal distribution with valid parameters
try:
    normal_dist = dist.Normal(loc, scale)
    print("Normal distribution created successfully.")
except ValueError as e:
    print(f"Error creating Normal distribution: {e}")

mmm = lightweight_mmm.LightweightMMM(model_name="carryover")

# For replicability in terms of random number generation in sampling
# reuse the same seed for different trainings.
mmm.fit(
    media=media_data_train_scaled,
    media_prior=costs_scaled,
    target=target_train_scaled,
    extra_features=extra_features_scaled,
    number_warmup=1000,
    number_samples=1000,
    seed=1)

adstock_models = ["adstock", "hill_adstock", "carryover"]
degrees_season = [1,2,3]

#adstock_models = ["hill_adstock"]
#degrees_season = [1]


for model_name in adstock_models:
    for degrees in degrees_season:
        mmm = lightweight_mmm.LightweightMMM(model_name=model_name)
        mmm.fit(media=media_data_train_scaled,
                media_prior=costs_scaled,
                target=target_train_scaled,
                extra_features=extra_features_scaled,
                number_warmup=1000,
                number_samples=1000,
                number_chains=1,

                seed=1)

        prediction = mmm.predict(
        media=media_data_test_scaled,
        extra_features=extra_features_test_scaled,
        target_scaler=target_scaler,
        seed=1)
        p = prediction.mean(axis=0)

        # p = p.at[jnp.isnan(p)].set(jnp.nanmean(p))

        p = np.where(np.isinf(p), np.nan, p)

        # Calculate the mean value of the array, ignoring NaN values
        mean_value = np.nanmean(p)

        # Replace NaN values with the mean value
        p = np.where(np.isnan(p), mean_value, p)

        print(target_data_test)

        print(p)

        mape = mean_absolute_percentage_error(target_data_test, p)
        print(f"model_name={model_name} degrees={degrees} MAPE={mape} samples={p[:3]}")

target_data_test

plot.plot_media_baseline_contribution_area_plot(media_mix_model=mmm,
                                                target_scaler=target_scaler,
                                                fig_size=(30,10))

plot.plot_prior_and_posterior(media_mix_model=mmm)

plot.plot_response_curves(
    media_mix_model=mmm, target_scaler=target_scaler, seed=1)

prices = jnp.ones(mmm.n_media_channels)

n_time_periods = 10
budget = jnp.sum(jnp.dot(prices, across_platform_media_data.mean(axis=0)))* n_time_periods

# Run optimization with the parameters of choice.
solution, kpi_without_optim, previous_media_allocation = optimize_media.find_optimal_budgets(
    n_time_periods=n_time_periods,
    media_mix_model=mmm,
    extra_features=extra_features_scaler.transform(extra_features_data_test)[:n_time_periods],
    budget=budget,
    prices=prices,
    media_scaler=media_scaler,
    target_scaler=target_scaler,
    seed=1)

# Obtain the optimal weekly allocation.
optimal_buget_allocation = prices * solution.x
optimal_buget_allocation

# similar renormalization to get previous budget allocation
previous_budget_allocation = prices * previous_media_allocation
previous_budget_allocation

budget, optimal_buget_allocation.sum()

# Both numbers should be almost equal
budget, jnp.sum(solution.x * prices)

# Plot out pre post optimization budget allocation and predicted target variable comparison.
plot.plot_pre_post_budget_allocation_comparison(media_mix_model=mmm,
                                                kpi_with_optim=solution['fun'],
                                                kpi_without_optim=kpi_without_optim,
                                                optimal_buget_allocation=optimal_buget_allocation,
                                                previous_budget_allocation=previous_budget_allocation,
                                                figure_size=(10,10))

mmm.print_summary()

plot.plot_model_fit(mmm, target_scaler=target_scaler)

new_predictions = mmm.predict(media=media_scaler.transform(media_data_test),
                              extra_features=extra_features_scaler.transform(extra_features_data_test),
                              seed=1)

new_predictions

plot.plot_out_of_sample_model_fit(out_of_sample_predictions=new_predictions,
                                 out_of_sample_target=target_scaler.transform(target_data_test))