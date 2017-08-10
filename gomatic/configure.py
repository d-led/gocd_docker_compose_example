#!/usr/bin/env python

# pip install gomatic (~>0.5.0)

# when GoCD server is up, run python configure.py

from gomatic import *
import re
import os

host = 'http://localhost:8153'

if 'DOCKER_HOST' in os.environ:
    host = os.environ['DOCKER_HOST']

url = re.search(r'//(.*)\:', host).group(1)+':8153'

print(url)

configurator = GoCdConfigurator(HostRestClient(url))

configurator.agent_auto_register_key = '123456789abcdef'

# reverse-engineered complex_pipelines.xml via gomatic

########################
pipeline = configurator\
	.ensure_pipeline_group("defaultGroup")\
	.ensure_replacement_of_pipeline("something_complex")\
	.set_git_url("https://github.com/d-led/gocd_docker_compose_example.git")
stage = pipeline.ensure_stage("build")
job = stage.ensure_job("build").ensure_artifacts({BuildArtifact("df.txt")})
job.add_task(ExecTask(['ls']))
job.add_task(ExecTask(['/bin/bash', '-c', 'df -h > df.txt']))
stage = pipeline.ensure_stage("unit")
job = stage.ensure_job("unit_test_1").ensure_resource("java")
job.add_task(ExecTask(['sleep', '3']))
job = stage.ensure_job("unit_test_2").ensure_resource("python")
job.add_task(ExecTask(['sleep', '1']))
stage = pipeline.ensure_stage("package")
job = stage.ensure_job("package").ensure_artifacts({BuildArtifact("sleep.txt")})
job.add_task(ExecTask(['/bin/bash', '-c', 'sleep 3 > sleep.txt']))

########################
pipeline = configurator\
	.ensure_pipeline_group("defaultGroup")\
	.ensure_replacement_of_pipeline("acceptance")\
	.ensure_material(PipelineMaterial("something_complex", "package"))
stage = pipeline.ensure_stage("defaultStage")
job = stage.ensure_job("defaultJob")
job.add_task(ExecTask(['sleep', '7']))

########################
pipeline = configurator\
	.ensure_pipeline_group("defaultGroup")\
	.ensure_replacement_of_pipeline("security")\
	.ensure_material(PipelineMaterial("something_complex", "package"))
stage = pipeline.ensure_stage("defaultStage")
job = stage.ensure_job("defaultJob")
job.add_task(ExecTask(['sleep', '10']))

########################
pipeline = configurator\
	.ensure_pipeline_group("defaultGroup")\
	.ensure_replacement_of_pipeline("docs")\
	.ensure_material(PipelineMaterial("something_complex", "build"))
stage = pipeline.ensure_stage("defaultStage")
job = stage.ensure_job("defaultJob")
job.add_task(ExecTask(['sleep', '15']))

########################
pipeline = configurator\
	.ensure_pipeline_group("defaultGroup")\
	.ensure_replacement_of_pipeline("deploy")\
	.ensure_material(PipelineMaterial("security", "defaultStage"))\
	.ensure_material(PipelineMaterial("acceptance", "defaultStage"))
stage = pipeline.ensure_stage("defaultStage")
job = stage.ensure_job("defaultJob")
job.add_task(FetchArtifactTask("something_complex/acceptance", "build", "build", FetchArtifactFile("df.txt")))
job.add_task(FetchArtifactTask("something_complex/acceptance", "package", "package", FetchArtifactFile("sleep.txt")))
job.add_task(ExecTask(['ls']))
job.add_task(ExecTask(['cat', 'sleep.txt']))


configurator.save_updated_config()
