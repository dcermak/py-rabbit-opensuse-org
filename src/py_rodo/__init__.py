"""py_rodo: Process RabbitMQ messages from rabbit.opensuse.org

Users must call set_backend() before importing payload types:

    import py_rodo.config
    py_rodo.config.set_backend('pydantic')  # or 'dataclassy'

    import py_rodo
    payload = py_rodo.PackageBuildSuccessPayload(...)
"""

from . import config


# Lazy imports to avoid circular imports and allow backend configuration
def __getattr__(name):
    """Lazy load payload types and other exports."""
    if name == "QueueProcessor":
        from .callback import QueueProcessor

        return QueueProcessor

    payload_names = {
        "ActionPayload",
        "ContainerPublishedPayload",
        "PackageBranchPayload",
        "PackageBuildFailurePayload",
        "PackageBuildSuccessPayload",
        "PackageBuildUnchangedPayload",
        "PackageCommentPayload",
        "PackageCommitPayload",
        "PackageCreatePayload",
        "PackageDeletePayload",
        "PackageServiceFailPayload",
        "PackageServiceSuccessPayload",
        "PackageUndeletePayload",
        "PackageUpdatePayload",
        "PackageUploadPayload",
        "PackageVersionChangePayload",
        "ProjectCommentPayload",
        "ProjectCreatePayload",
        "ProjectDeletePayload",
        "ProjectUndeletePayload",
        "ProjectUpdatePayload",
        "ProjectUpdateProjectConfPayload",
        "PublishedStatusReportPayload",
        "RelationshipCreatePayload",
        "RepoBuildFinishedPayload",
        "RepoBuildStartedPayload",
        "RepoPacktrackPayload",
        "RepoPublishPayload",
        "RepoPublishStatePayload",
        "RepoStatusReportPayload",
        "RequestChangedPayload",
        "RequestCommentPayload",
        "RequestCreatePayload",
        "RequestDeletePayload",
        "RequestReviewChangedPayload",
        "RequestReviewWantedPayload",
        "RequestReviewsDonePayload",
        "RequestStateChangedPayload",
        "RequestStatus",
        "RequestStatusReportPayload",
        "RoutingKey",
    }

    if name in payload_names:
        from . import types

        return getattr(types, name)

    raise AttributeError(f"module {__name__} has no attribute {name}")


__all__ = [
    "config",
    "QueueProcessor",
    "ActionPayload",
    "ContainerPublishedPayload",
    "PackageBranchPayload",
    "PackageBuildFailurePayload",
    "PackageBuildSuccessPayload",
    "PackageBuildUnchangedPayload",
    "PackageCommentPayload",
    "PackageCommitPayload",
    "PackageCreatePayload",
    "PackageDeletePayload",
    "PackageServiceFailPayload",
    "PackageServiceSuccessPayload",
    "PackageUndeletePayload",
    "PackageUpdatePayload",
    "PackageUploadPayload",
    "PackageVersionChangePayload",
    "ProjectCommentPayload",
    "ProjectCreatePayload",
    "ProjectDeletePayload",
    "ProjectUndeletePayload",
    "ProjectUpdatePayload",
    "ProjectUpdateProjectConfPayload",
    "PublishedStatusReportPayload",
    "RelationshipCreatePayload",
    "RepoBuildFinishedPayload",
    "RepoBuildStartedPayload",
    "RepoPacktrackPayload",
    "RepoPublishPayload",
    "RepoPublishStatePayload",
    "RepoStatusReportPayload",
    "RequestChangedPayload",
    "RequestCommentPayload",
    "RequestCreatePayload",
    "RequestDeletePayload",
    "RequestReviewChangedPayload",
    "RequestReviewWantedPayload",
    "RequestReviewsDonePayload",
    "RequestStateChangedPayload",
    "RequestStatus",
    "RequestStatusReportPayload",
    "RoutingKey",
]
