<a href="https://datahub.io/core/browser-stats"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25)" alt="badge" /></a>

Web browser usage statistics over time. 

## Data

Primary data source is [W3Schools browser statistics](http://www.w3schools.com/browsers/browsers_stats.asp). The data provided comes from the log files of W3Schools' servers.

`data.csv` contains usage statistics for both current browsers as well as several now-defunct browsers.

`data-extant.csv` only includes data for current browsers.

## Preparation

This package includes `scripts/process.py` to scrape the data. Currently it is required to manually change the index to match which calendar year's table data to act on.

## License

Non-commerical use of this data appears to be covered under W3Schools' Fair Use in their [Terms of Use](http://www.w3schools.com/about/about_copyright.asp), but please review these terms or contact W3Schools yourself to clarify terms for your specific usage.
