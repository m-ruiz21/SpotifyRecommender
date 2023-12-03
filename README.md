# Spotify Copilot : Customized Playlist Generator For Whatever Music You Want, Exactly When You Want It 

## Overview
**Spotify Copilot** is a project with the aim to take the first steps towards a conversational recommendation system (CRS) for music by allowing users to generate custom playlists given a playlist name. 

The project leverages the [Spotify Recommendations](https://developer.spotify.com/documentation/web-api/reference/get-recommendations) and its ability to fine tune recommendations given song latent factors that Spotify calls 'Song Features'. 

The objective of the project, therefore, is to translate human speech to these Song Features in order to generate highly customizable recommendations.
 
To achieve this, the Program leverages a BERT model fine-tuned for the regression task of predicting the Song Features. This model is then trained on a set of about 9-10 thousand playlists and their resulting latent factors. 

The trained model is then deployed to a flask API so the user can interact with it using the [front end interface](https://github.com/m-ruiz21/SpotifyRecommender-FrontEnd) built with Next.js, Tailwind, and Typescript.

For more specific implementation details and how to navigate the repository, you can reference the [wiki](https://github.com/m-ruiz21/SpotifyRecommender/wiki) (recommended), the [Design Doc](https://docs.google.com/document/d/1zC-kdPw4mLZAQSHgnoq8gnnF_FW-U8kmtuk2DkBA-6E/edit?usp=sharing), or the video presentation.

## Documenation
For specific implementation details and tips on navigating the repository, reference:
- The [wiki](https://github.com/m-ruiz21/SpotifyRecommender/wiki) (recommended)
- The [Design Doc](https://docs.google.com/document/d/1zC-kdPw4mLZAQSHgnoq8gnnF_FW-U8kmtuk2DkBA-6E/edit?usp=sharing)
- The Video Presentation

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
To get started, select a feature from the issues tab (you can also check out the Milestones page to select a task), create branch for the PR, accomplish task, and attach it to PR.  

>Note: you can approve your own PR, PR's are working simply as a feature to keep track of tasks being completed / so we don't run into each other too much.
