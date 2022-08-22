# swipe-type

A novel swipe based biometric pipeline

## About

This project implements a swipe based biometric pipeline using the [How We Swipe Dataset](https://osf.io/sj67f/)

## How to build and run

See the [Swipe-Type build instructions](https://github.com/AlvinKuruvilla/swipe-type/blob/master/docs/BuildInstructions.md). Swipe-Type can run on Linux and macOS

## Configuration

Config is stored in the `config.json` file and has two configuration components:

1. TIME_DELTA_THRESHOLD: The threshold to use to distinguish individual swipes
2. SWIPE_LENGTH_THRESHOLD: The minimum length of a swipe to be considered "high quality" and added to the list of swipes for a particular word

There are APIs which allow these configuration values to be programmatically retrieved and dynamically reconfigured

## Citation

Parts of the source code for this project were taken from

```bib

@InProceedigs{swipe_dataset,
author = {Luis A. Leiva and Sunjun Kim Wenzhe Cui and Xiaojun Bi and Antti Oulasvirta},
title = {How We Swipe: A Large-scale Shape-writing Dataset and Empirical Findings},
booktitle = {Proc. MobileHCI},
year = {2021},
}
```
