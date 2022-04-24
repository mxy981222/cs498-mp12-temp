from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.CoreV1Api()
# api = client.ApiClient(client.Configuration())
v2 = client.BatchV1Api()
app = Flask(__name__)
# app.run(debug = True)

@app.route('/config', methods=['GET'])
def get_config():
    pods = []

    res = v1.list_pod_for_all_namespaces(watch=False)
    for p in res.items():
        pod = {"node":p.spec.node_name,"ip":p.status.pod_ip,"namespace":p.metadata.namespace,"name":p.metadata.name,"status":p.status.phase}
        pods.append(pod)
    output = {"pods": pods}
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here
    # req = request.get_json(force=True)
    # dataset = req['dataset']
    dataset = "mnist"

    env = [
        client.V1EnvVar(name = "DATASET", value = dataset),
        client.V1EnvVar(name = "TYPE", value = "ff")   
    ]

    # resources = client.V1ResourceRequirements(limits = {"cpu","0.9"},requests = {"cpu","0.9"})
    
    container = client.V1Container(
        name = "free-job",
        image = "mxy981222/mp12",
        env = env,
        # resources = resources
    )
    
    # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Job.md
    body = client.V1Job(
        api_version = "batch/v1",
        kind = "Job",
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ObjectMeta.md
        metadata = client.V1ObjectMeta(generate_name = "free-app-", namespace = "free-service"),
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1JobSpec.md
        spec = client.V1JobSpec(template = client.V1PodTemplateSpec(spec = client.V1PodSpec(containers = [container],
                                                                                            restart_policy = 'OnFailure')))
    )
    
    v2.create_namespaced_job("free-service", body)
    return "success"


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    # req = request.get_json(force=True)
    # dataset = req['dataset']
    dataset = "mnist"

    env = [
        client.V1EnvVar(name = "DATASET", value = dataset),
        client.V1EnvVar(name = "TYPE", value = "cnn")   
    ]
    
    resources = client.V1ResourceRequirements(limits = {"cpu","0.9"},requests = {"cpu","0.9"})
    
    container = client.V1Container(
        name = "free-job",
        image = "mxy981222/mp12",
        env = env,
        resources = resources
    )
    
    # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1Job.md
    body = client.V1Job(
        api_version = "batch/v1",
        kind = "Job",
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1ObjectMeta.md
        metadata = client.V1ObjectMeta(generate_name = "premium-app-", namespace = "default"),
        # https://github.com/kubernetes-client/python/blob/master/kubernetes/docs/V1JobSpec.md
        spec = client.V1JobSpec(template = client.V1PodTemplateSpec(spec = client.V1PodSpec(containers = [container],
                                                                                            restart_policy = 'OnFailure')))
    )
    
    v2.create_namespaced_job("default", body)

    return "success"

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)