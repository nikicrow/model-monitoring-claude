# model-monitoring-claude

My prompt

As a senior python developer, create a python app that will serve as a model monitoring dashboard for a production propensity model.

For context, the model scores on a monthly basis for around 2.5 million customers on around the 3-5th day of the month. 

The dashboard will be for non technical stakeholders so try and use language that is easy to understand and be verbose in trying to explain each chart. Remember to have clear chart titles, x and y axis titles.

All charts should be created using plotly so it is interactive and charts are downloadable.

Have the following on this dashboard:
1. A section titled 'Model scoring pipelne stability'. In this section will be several charts and score cards. Add a text section to explain what this section is about.
 a. Scorecard with the date of the last model run which should be 4th April 2025
 b. Scorecard with the number of customers scored which should be around 2.58 million customers. Also include an MoM change arrow with a percentage difference e.g. +3%
 c. Scorecard with the percentage of customers that were scored as high probability to convert e.g. 25% with a MoM percentage difference to last month
 d. Scorecard with the percentage of customers that were scored as medium probability to convert e.g. 35% with a MoM percentage difference to last month
 e. Scorecard with the percentage of customers that were scored as low probability to convert e.g. 50% with a MoM percentage difference to last month
 f. A bar chart with total number of customers scored over the last 6 months.
 g. A stacked bar chart with the number of high medium and low customers over the last 6 months. 
 h. A bar chart showing the number of customers in high, medium and low for each decile. The low customers should be deciles 1-4 and some of 5, medium should be some of 5 and 6-7 and some of 8. The rest should be high.
2. A section titled 'Actual conversion rates for past model scores'. Charts in this section should only have data from up to the previous model month which is 3rd Feb 2025. Add a text section to explain what this section is about.
 a. Scorecards with the percentage of conversions from last month in high, medium and low model score buckets, make these numbers roughly 7%, 4% and 1.5% respectively. Also add MoM difference in percentage difference.
 b. A line chart showing the conversion rates over high, medium and low buckets over the past 6 months. Use similar numbers to 2a for the past months (but not the exact same).
 c. A bar chart with the number of conversions by decile for last month with a line chart that shows the percentage of conversions by propensity decile. Make sure the top decile has aroun 10% conversions and the bottom decile has less than 1% conversions.
 d. A stacked bar chart with the number of conversation by decile for the past 5 months up to last month. Always show the 10th decile with the most conversions and the 1st decile with the least.
 e. Actual conversions vs month for the past 5 months.
3. A section titled 'Model accuracy - data science metrics'. Charts in this section are just for this months predictions. Add a text section to explain what this section is about.
 a. ROC with AUROC printed. this should be roughly 0.70
 b. PRC with AUPRC printed. This is an imbalanced model so keep that in mind.
 c. Cumulative recall vs decile. This is a chart with the x axis as decile and the y axis as cumulative recall at decile. THe top decile should have cumulative recall at about 30% and this will increase to 100% by the last decile.
 d. Cumulative precision vs decile. This is a chart with the x axis as decile and the y axis as the cumulative precision as decile. For the top bucket it should be around 10% and by the last bucket it should be around 1%.
4. A section titled 'Feature importance and feature drift'. Charts in this section are just for this months predictions. Add a text section to explain what this section is about.
 a. Add a gain feature importance chart. Make up the top features but base them around unicorn features e.g. magic level, horn toughness, average poop weight, number of legs e.t.c.
 b. Add a feature drift table for each feature using character stability index. Order by the feature importance.

Create the above dashboard so that i can easily export an html file. Create mock data that satisfies all of the above.

Make the code clear and well laid out so that it is easily extendable and scalable.