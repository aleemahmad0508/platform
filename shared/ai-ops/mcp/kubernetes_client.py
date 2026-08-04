from kubernetes import client, config
from kubernetes.config.config_exception import ConfigException

# Load Kubernetes configuration
try:
    # Running inside a Kubernetes cluster
    config.load_incluster_config()
    print("Using in-cluster Kubernetes configuration")
except ConfigException:
    # Running locally
    config.load_kube_config()
    print("Using local kubeconfig")

# Kubernetes Core API
v1 = client.CoreV1Api()


def get_pods(namespace: str = "default"):
    """
    Get all pods from the given namespace.
    """

    pods = v1.list_namespaced_pod(namespace=namespace)

    if not pods.items:
        return f"No pods found in namespace '{namespace}'."

    result = []

    for pod in pods.items:
        result.append(
            f"{pod.metadata.name} - {pod.status.phase}"
        )

    return "\n".join(result)


def describe_pod(
    pod_name,
    namespace="default",
):
    pod = v1.read_namespaced_pod(
        name=pod_name,
        namespace=namespace,
    )

    return f"""
Pod: {pod.metadata.name}
Status: {pod.status.phase}
Node: {pod.spec.node_name}
IP: {pod.status.pod_ip}
"""


def get_logs(
    pod_name,
    namespace="default",
    lines=100,
):
    return v1.read_namespaced_pod_log(
        name=pod_name,
        namespace=namespace,
        tail_lines=lines,
    )