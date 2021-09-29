from frictionless import Pipeline, system
from datetime import datetime, date
from jinja2 import Environment, FileSystemLoader
import yaml

from custom_steps import transparenzrhPlugin

# Register custom plugin
system.register('transparenZRH', transparenzrhPlugin())

# Load Sensors from GeoData portal via geo.pipeline.yaml
env = Environment(loader=FileSystemLoader('src/descriptors'))
template = env.get_template(f"geo.pipeline.yaml")
recipe = template.render(
    params={
        "thisyear": int(datetime.strftime(date.today(), "%Y"))
    }
)
target = Pipeline(yaml.full_load(recipe)).run()

# check if pipeline is valid
if not target.valid:
    print(target)
else:
    try:
        # convert resource from pipeline into python dictionary
        sensors = target.task.target.to_inline(dialect=dict(keyed=True))
        for sensor in sensors:
            print(f"processing {sensor}...")
            template = env.get_template(f"bikepedestrian.pipeline.yaml")
            recipe = template.render(params = sensor)
            recipe_parsed = yaml.full_load(recipe)
            pipeline = Pipeline(recipe_parsed).run()
            if not pipeline.valid:
                print(pipeline)
            else:
                print("done")
    except Exception as e:
        print(f"An error occured during processing: {e}")