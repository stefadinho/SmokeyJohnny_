Prod: [![Netlify Status](https://api.netlify.com/api/v1/badges/a1b263d1-d795-455a-954b-e43dc59b609c/deploy-status)](https://app.netlify.com/sites/stavenuiter/deploys)

# Smokey Johnny

Stavenuiter barbeque website.

## Development

Run:

```make
make install-hugo
make
```

## Preview Build

Push code to `develop` to trigger the following sequence of steps:
- A [Azure DevOps Build](https://dev.azure.com/menziess/blog/_build?definitionId=33) that builds, installs and runes the `vlees-converter` tool that creates the products from the ["Vlees assortiment - assortiment.csv"](assortiment/Vlees%20assortiment%20-%20assortiment.csv).

  It then builds the website and pushes it to [github.io](https://github.com/Menziess/barbeque).

- A [Netlify preview](https://app.netlify.com/sites/stavenuiter/deploys) is created.

## Production

Create a PR from `develop` into `master` to publish the build to production. Or publish a preview build directly from netlify.
