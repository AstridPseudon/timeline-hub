"""Exact semantic compatibility metadata, never route or grant authority."""


def supported_versions(value):
    """A legacy scalar declares one version, never a minimum version."""
    values = value if isinstance(value, list) else [value]
    if not values or any(type(version) is not int or version < 1 for version in values):
        raise ValueError("operation versions must be a nonempty finite set of positive integers")
    return sorted(set(values))


def normalize_operation_versions(descriptor):
    if not isinstance(descriptor, dict) or any(not isinstance(key, str) or not key for key in descriptor):
        raise ValueError("operation_versions must map operation IDs to supported versions")
    return {key: supported_versions(descriptor[key]) for key in sorted(descriptor)}


def supports_operation(descriptor, operation, version):
    if type(version) is not int or version < 1:
        raise ValueError("required operation version must be a positive integer")
    return version in normalize_operation_versions(descriptor).get(operation, [])
