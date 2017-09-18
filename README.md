# Advisor

## Introduction

Advisor is the hyper parameters tuning system for black box optimization.

It is the open-source implementation of [Google Vizier](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/46180.pdf) with the features.


* Get suggestions from API, WEB or CLI
* Support abstractions of Study and Trial
* Included search and early stop algorithms
* Recommend parameters with trained model
* Same programming interfaces as Google Vizier

## Algorithms

* [x] Random Search Algorithm
* [ ] 2x Random Search Algorithm
* [x] Grid Search Algorithm
* [ ] Gaussian Process Bandit
* [ ] Batched Gaussian Process Bandits
* [ ] SMAC Algorithm
* [ ] CMA-ES Algorithm
* [x] No Early Stop Algorithm
* [x] Early Stop First Trial Algorithm
* [x] Early Stop Descending Algorithm
* [ ] Performance Curve Stop Algorithm
* [ ] Median Stop Algorithm

## Usage

Install the dependencies.

```shell
pip install -r requirements.txt
```

Run the advisor server.

```shell
./manage.py runserver 0.0.0.0:8000
```

Open `http://127.0.0.1:8000` in the browser.

## Screenshot

List all the studies and create/delete the studies easily.

![study_list.png](./images/study_list.png)

List the detail of study and all the related trials.

![study_detail.png](./images/study_detail.png)

List all the trials and create/delete the trials easily.

![trial_list.png](./images/trial_list.png)

List the detail of trial and all the related metrics.

![trial_detail.png](./images/trial_detail.png)

