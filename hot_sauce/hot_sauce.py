import numpy as np
import pandas as pd

from hot_sauce.utils import (
    remove_nones,
    enum_to_data_frame,
    sample_gamma
)

from hot_sauce.config import (
    Peppers,
    PEPPER_FACTORS,
    PEPPER_PROBABILITIES,
    GREEN_PEPPERS,
    GREEN_PEPPER_COLOR_MODE,
    GREEN_PEPPER_COLOR_SHAPE,
    RED_PEPPERS,
    RED_PEPPER_COLOR_MODE,
    RED_PEPPER_COLOR_SHAPE,
    AGE_X_SCALE,
    AGE_Y_SCALE
)


class HotSauceData:

    def sample(self, n):
        peppers = sample_peppers(n)
        peppers_df = enum_to_data_frame(Peppers, peppers)
        peppers_factor = compute_peppers_factor(peppers)
        color = compute_color(peppers)
        ages = sample_ages(n)
        age_factor = compute_age_factor(ages)
        hotness = pd.Series(peppers_factor + age_factor, name='HOTNESS')
        return pd.concat([peppers_df, color, ages, hotness], axis=1)


def sample_peppers(n):
    peppers = []
    for _ in range(n):
        row = [
            np.random.choice(
                [pepper, None], 
                p=PEPPER_PROBABILITIES[pepper])
            for pepper in Peppers]
        row = remove_nones(row)
        if row == []:
            row = [np.random.choice(Peppers)]
        peppers.append(row)
    return peppers

def compute_peppers_factor(peppers_df):
    return pd.Series([0.5]*len(peppers_df))

def compute_color(peppers):
    colors = []
    for row in peppers:
        green_color = sum(
            sample_gamma(
                1, 
                mode=GREEN_PEPPER_COLOR_MODE,
                shape=GREEN_PEPPER_COLOR_SHAPE)
            for p in row
            if p in GREEN_PEPPERS)
        red_color = sum(
            sample_gamma(
                1, 
                mode=RED_PEPPER_COLOR_MODE,
                shape=RED_PEPPER_COLOR_SHAPE)
            for p in row
            if p in RED_PEPPERS)
        color = (green_color + red_color) / len(row)
        colors.append(color)
    return pd.Series(np.concatenate(colors), name='COLOR')

def sample_ages(n):
    return pd.Series([5]*n, name='AGE')

def compute_age_factor(ages):
    return pd.Series([1]*len(ages))


#    commute_time_raw = (
#        RAW_DISTANCE_SLOPE * raw_distance
#            - RAW_DISTANCE_NONLINEARITY_Y_SCALE * (
#                2 / (1 + np.exp(RAW_DISTANCE_NONLINEARITY_X_SCALE * raw_distance)
#                         ** RAW_DISTANCE_NONLINEARITY_POWER))
#            + TIME_OF_DAY_FACTOR_SCALING * time_of_day_factor
#            + geometry_factor
#            + commute_type_factor)
