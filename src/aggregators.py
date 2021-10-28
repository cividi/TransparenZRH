from frictionless import Pipeline, system
from frictionless.plugins.s3 import S3Control
from datetime import datetime, date
from jinja2 import Environment, FileSystemLoader
import yaml
import requests

from custom_steps import transparenzrhPlugin

# Register custom plugin
system.register('transparenZRH', transparenzrhPlugin())

try:
    r = requests.head("https://data.stadt-zuerich.ch/dataset/ted_taz_verkehrszaehlungen_werte_fussgaenger_velo/download/2021_verkehrszaehlungen_werte_fussgaenger_velo.csv")
    source_time = datetime.strptime(r.headers['last-modified'],
        #Fri, 27 Mar 2015 08:05:42 GMT
        '%a, %d %b %Y %X %Z')

    r = requests.head("https://transparenzrh.eu-central-1.linodeobjects.com/bikepedestrian/FZS_MILI.csv")
    cached_time = datetime.strptime(r.headers['last-modified'],
        #Fri, 27 Mar 2015 08:05:42 GMT
        '%a, %d %b %Y %X %Z')
    # Load Sensors from GeoData portal via geo.pipeline.yaml if file has been updated today

    # if source_time >= cached_time:
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
                
                # NOTE: currently not possible with descriptive table-write, as options other than path are not expanded correctly
                pipeline.task.target.write(
                    # path= "tmp/tmp.csv"  # for local debugging
                    path=f"s3://transparenzrh/bikepedestrian/{sensor['sensor_ref']}.csv",
                    control=S3Control(acl="public-read")
                )

                if not pipeline.valid:
                    print(pipeline)
                else:
                    print("done")
        except Exception as e:
            print(f"An error occured during processing: {e}")
    # else:
    #     print("Source file not newer... Trying again soon.")
except Exception as e:
    print(e)