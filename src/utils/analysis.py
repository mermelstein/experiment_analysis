import os
import jinja2

def create_research(experiment_df):
	# assumes the template is in the same directory as this script
	templateLoader = jinja2.FileSystemLoader(searchpath="./")
	templateEnv = jinja2.Environment(loader=templateLoader)
	# load template by filename
	TEMPLATE_FILE = "templates/index_template.html"
	template = templateEnv.get_template(TEMPLATE_FILE)
	outputText = template.render(
		experiment_list=experiment_df.to_dict("records")  # needs to be an iterable list
	)

	# save the index.html file
	index = open(os.path.join(os.getcwd(), "website/index.html"), "w")
	index.write(outputText)
	index.close()