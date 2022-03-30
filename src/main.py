import yaml
import json
import subprocess
import os
import pandas as pd
from utils.simplehttp import launch_local_server
from utils.analysis import create_research
from utils.db_connection import get_data

def main():
	with open("experiments.yaml", 'r') as file:
		try:
			experiments_yaml = yaml.safe_load(file)
		except yaml.YAMLError as e:
			print(e)

	# for each experiment, run the analysis and create the html output
	# write variables to json file and load in notebook
	for i in experiments_yaml:
		experiment_dict = {"name": i,
											 "title": experiments_yaml[i]['title'],
											 "start_date": experiments_yaml[i]['start_date'].strftime("%Y-%m-%d"),
											 "end_date": experiments_yaml[i]['end_date'].strftime("%Y-%m-%d"),
											 "control_variant_name": experiments_yaml[i]['control_variant_name'],
											 "author": experiments_yaml[i]['author']}

		# write to json so it can be picked up by the notebook
		with open("website/experiment.json", "w") as outfile:
			json.dump(experiment_dict, outfile)

		# create temp Jupyter notebook with experiment metadata
		with open("templates/analysis_output.ipynb") as f:
			data = json.load(f)
		try:
			# replace metadata in notebook with YAML values
			m = data["cells"][0]["source"]
			m = [s.replace("title: title_holder\n", str("title: " + experiment_dict['title'] + "\n")) for s in m]
			m = [s.replace("author: author_mcauthorson\n", str("author: " + experiment_dict['author'] + "\n")) for s in m]
			m = [s.replace("date: experiment_date\n", str("date: " + experiment_dict['start_date'] + "\n")) for s in m]
			data["cells"][0]["source"] = m

		except Exception as e:
			print(e)

		temp_notebook_name = str("website/" + i + ".ipynb")

		with open(temp_notebook_name, "w") as outfile:
			json.dump(data, outfile)

		# PRODUCTION ONLY
		# get experiment data
		# # data needs to be in a dataframe format where one column has the variant names, and one is a binomial outcome variable
		# query = str("""
		# select
		#     bucket, --expected column name for the variants is "bucket"
		#     user_id,
		#     conversion as """ + outcome_col + """
		# from experiments table
		# where experiment_name = '""" + experiment['name'] + """'
		# """)
		# df = get_data(query)
		# df.to_csv('website/experiment_data.csv', index=False)

		# run notebook
		subprocess.run(
			[f"quarto render {temp_notebook_name} --to html --execute"],
			shell=True,
			check=True,
			stdout=subprocess.PIPE,
		)

		# delete temp Jupyter notebook
		os.remove(temp_notebook_name)

		# PRODUCTION ONLY
		# os.remove('website/experiment_data.csv')

	# gather all the metadata for the experiments and their html file locations and insert into the front page
	experiment_df = pd.DataFrame(
		columns=[
			"name",
			"title",
			"date",
			"author",
			"link",
		]
	)

	# get most metadata from the YAML file, then add in the html file location
	for i in experiments_yaml:
		experiment_df = experiment_df.append(
			{
				"name": i,
				"title": experiments_yaml[i]['title'],
				"date": experiments_yaml[i]['start_date'].strftime("%Y-%m-%d"),
				"author": experiments_yaml[i]['author'],
				"link": str(i + ".html"),
			},
			ignore_index=True,
		)

	# write the front page
	create_research(experiment_df)

	# remove the experiments.json
	os.remove("website/experiment.json")

	# use this for testing, but deploying as a static website hosted on S3 is more stable
	# launch the local server
	launch_local_server()

if __name__ == "__main__":
	main()