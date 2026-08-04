from mcp_instance import mcp

print("loading tools.py")

import kubernetes_client
import argocd
import prometheus
import alertmanager


@mcp.tool()
def get_pods(namespace: str = "default"):
    return kubernetes_client.get_pods(namespace)


@mcp.tool()
def describe_pod(name):
    return kubernetes_client.describe_pod(name)


@mcp.tool()
def get_logs(name):
    return kubernetes_client.get_logs(name)


@mcp.tool()
def get_application_status(app):
    return argocd.get_application_status(app)


@mcp.tool()
def get_cpu_usage():
    return prometheus.get_cpu_usage()




@mcp.tool()
def get_alert_status():
    return alertmanager.get_alerts()


print("Finished registering tools")