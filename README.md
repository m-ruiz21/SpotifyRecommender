# SpotifyRecommender

## Documenation
Documentation on the proxies and other aspects of the project can be found in the wiki page or in the [design document.](https://docs.google.com/document/d/1zC-kdPw4mLZAQSHgnoq8gnnF_FW-U8kmtuk2DkBA-6E/edit?usp=sharing)

## Getting started
To get started on the virtual enviornment as follows:
```bash
env/Scripts/activate
```
This script should activate the python virtual env which includes all of the required packages installed.
Afterwards you can run any sub-module / directory with:
```bash
py -m {directory}.{file name without .py}
```
So for example, to run data_fetcher/fetcher_driver.py:
```bash
py -m data_fetcher.fetcher_driver
```

Finally, when you install a package, make sure you install it in the virtual env and add the name of the package to requirements.txt so everybody stays up to date!

## Contributing
To get started, select a feature from the issues tab, create branch for the PR, accomplish task, and attach it to PR.
You can approve your own PR, PR's are working simply as a feature to keep track of tasks being completed.
