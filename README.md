# Bayes Experiment Analysis

> Dani Mermelstein

This is a Dockerized/containerized skeleton service for applying Bayesian statistics to A/B tests and outputting standardized reports. It leverages and productionizes the [BayesABTest](https://github.com/bakermoran/BayesABTest) package and [Quarto](https://quarto.org/) publishing system. The service will result in a website with a front page listing all tests conducted and various HTML outputs for each experiment.

### **Example of the front page:**

![service front page](https://github.com/clone-this-repo/experiment_analysis/blob/main/src/templates/images/index_screenshot.png)

### **Example of an experiment result page:**

![example experiment page](https://github.com/clone-this-repo/experiment_analysis/blob/main/src/templates/images/experiment_screenshot.png)

### **Usage:**

It all starts with the [experiments.yaml](https://github.com/clone-this-repo/experiment_analysis/blob/main/src/experiments.yaml) file. This is where metadata is listed for each experiment. This metadata could be expanded to include a summary, logic on whether the experiment has finished running, or anything else that you might want to insert in the final writeup. This service is a skeleton, so really up to you.

Quarto is used to generate all HTML files related to experiments, which might get a little heavy depending on how many experiments you run. A more lightweight version could use a similar method to the generation of [index.html](https://github.com/clone-this-repo/experiment_analysis/blob/main/src/website/templates/index_template.html) where you have a template file to which you insert charts and variable values. Quarto renders every experiment through the analysis_output Jupyter notebook (although this could be switched to a markdown file with embedded code).

The service could generate reporting on a schedule (eg daily) or when new experiments are concluded (ie with some trigger).

The default included analysis is for split tests that are judged on conversion rates and requires a binary outcome (ie conversion happened yes/no). BayesABTest additionally allows for analysis of continuous or discrete variables (eg minutes spend on calls, deposit amounts, account balance) which would only require some minor tweaking. It would also be possible to implement different SQL queries for data gathering, depending on the KPI being measured, or different traditional statistical tests as needed.   

### **Suggested hosting method:**

The most stable end state for hosting the output would probably be a static website on S3. That's because this is not an app, and while it is possible to connect to a database (*ahem* strongly suggested) the output is static HTML files. A static website would also result in improved uptime, less downtime, and not having to figure out what's wrong with the server. That said, the service does default to hosting on a local server which is useful for local testing but can be easily removed. 

Hopefully this provides the heavy lifting for you to analyze experiments at scale. Happy testing!