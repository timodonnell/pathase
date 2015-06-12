#!/bin/bash

# Adapted from https://github.com/w3ctag/promises-guide/blob/master/deploy-gh-pages.sh

cd docs/_build

touch .nojekyll

git init
git config user.name "Travis-CI"
git config user.email "travis@w3ctag.org"
git add .
git commit -m "Deploy to GitHub Pages"
git push --force --quiet "https://${GH_TOKEN}@${GH_REF}" master:gh-pages > /dev/null 2>&1
