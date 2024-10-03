---
slug: docusaurus-setup
title: Using Docusaurus
authors: [amaloney]
tags: [docusaurus]
---

How to create a project page using GitHub Pages and Docusaurus.

{/* truncate */}

I have used Docusaurus in the past to create documentation pages for tools. One of the
nicest features of Docusaurus is that you can create MDX (markdown with React) files
with content. My previous use case with Docusaurus was generating tutorial pages
rendered from Jupyter notebooks. You can see examples of the tutorials on [Bean
Machine](https://beanmachine.org/docs/overview/tutorials/Coin_flipping/CoinFlipping/).
Bean Machine is no longer being actively developed, and has been archived, but one of
the things I built was a converter from a Jupyter notebook to an MDX file. The MDX file
could then be consumed by Docusaurus and served statically in a GitHub pages site. I
made custom React components for Bokeh and Plotly figures, so they retained their
interactivity, see the [Zero inflated count data](
https://beanmachine.org/docs/overview/tutorials/Zero_inflated_count_data/ZeroInflatedCountData/)
tutorial for an example. The workflow `Jupyter -> MDX -> statically served` with the
capability to include React components is why I decided to use Docusaurus for my
personal project page.

I'll first describe how to create a Docusaurus project page before going into the
details of converting Jupyter notebooks to MDX files. I'm going to use
[mamba](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html) to
create a virtual environment, even though it may seem absurd to do this right now. The
goal is to create Jupyter notebooks using Python, so using `mamba` as a virtual
environment manager is not ridiculous.

```yaml
# environment.yaml
name: github-page-dev
channels:
  - conda-forge
dependencies:
  - python <3.12
  # Package managers
  - nodejs
  - pip
```

Above is a minimum example for creating a virtual environment. To create the
environment, save it to a directory, create the environment, and activate it.

```bash
mkdir github-page-dev
cd github-page-dev
# Assuming the file is in the directory.
mamba env create --file environment.yaml && mamba activate github-page-dev
```

Next, install the latest Docusaurus. `nodejs` was installed into the virtual
environment, so we can run the scaffold for the website using the [Docusaurus
documentation](https://docusaurus.io/docs/installation#scaffold-project-website)

```bash
npx create-docusaurus@latest website classic --typescript
```

The above command will create the scaffold in the current directory, and will configure
it to use TypeScript. I removed everything out of the `website` directory and placed it
in the top level directory. I did this because I am only going to use this repo for
discussing my various projects. You can read more about using Docusaurus as part of a
mono-repo setup with a tool you create with its documentation.

My repo looked like the following after getting this set up.

```
project-page
├── blog
├── docs
├── node_modules
├── src
│   ├── components
│   ├── css
│   └── pages
├── static
├── .gitignore
├── .prettierrc
├── LICENSE
├── README.md
├── babel.config.js
├── docusaurus.config.js
├── environment.yaml
├── package-lock.json
├── package.json
├── sidebar.ts
└── tsconfig.json
```

One needs to update the `docusaurus.config.js` file by updating it with your personal
info. For instance, changing the `projectName`, `url`, `organizationName` _etc_ is
necessary to personalize the website. I did not do very much initially as I was more
interested in deploying the website before changing a lot of stuff.

Follow along with [GitHub](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)
about how to create a page (and a repo if you need to). I created a workflow for
deploying the website so that any push to main triggers a Docusaurus build. Note that I
also used `npm` and not `yarn`, which the Docusaurus documentation uses. Nonetheless,
save the below file to `.github/workflows` in your repo.

```yaml
# deploy.yml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main

jobs:
  build:
    name: Build Docusaurus
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: actions/setup-node@v4
        with:
          node-version: 18
          cache: npm

      - name: Install dependencies
        run: npm ci
      - name: Build website
        run: npm run build

      - name: Upload Build Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: build

  deploy:
    name: Deploy to GitHub Pages
    needs: build

    # Grant GITHUB_TOKEN the permissions required to make a Pages deployment
    permissions:
      pages: write # to deploy to Pages
      id-token: write # to verify the deployment originates from an appropriate source

    # Deploy to the github-pages environment
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    runs-on: ubuntu-latest
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

Push everything to your GitHub repo, and you should be able to see your new page.
