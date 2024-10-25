"""This module contains type definitions of the bodies of the messages sent out
by the open build service and the mapping of these types to the respective
routing keys.

"""

import enum
from abc import ABCMeta
from typing import Dict
from typing import Type

from dataclassy import dataclass


@enum.unique
class RequestStatus(enum.Enum):
    """Possible states of a Review of a request"""

    #:: The request has been reviewed
    REVIEW = "review"
    #:  New request without any reviews
    NEW = "new"
    #: The request has been accepted
    ACCEPTED = "accepted"
    #: The request has been declined by the reviewer
    DECLINED = "declined"
    #: The request has been revoked by the submitter
    REVOKED = "revoked"
    #: The request has been superseded by a new one
    SUPERSEDED = "superseded"
    #: The request has been deleted
    DELETED = "deleted"


@enum.unique
class RoutingKey(enum.Enum):
    PACKAGE_BUILD_SUCCESS = "package.build_success"
    PACKAGE_BUILD_FAILURE = "package.build_fail"
    PACKAGE_BUILD_UNCHANGED = "package.build_unchanged"
    PACKAGE_CREATE = "package.create"
    PACKAGE_UPDATE = "package.update"
    PACKAGE_DELETE = "package.delete"
    PACKAGE_UNDELETE = "package.undelete"
    PACKAGE_BRANCH = "package.branch"
    PACKAGE_COMMIT = "package.commit"
    PACKAGE_UPLOAD = "package.upload"
    PACKAGE_SERVICE_SUCEESS = "package.service_success"
    PACKAGE_SERVICE_FAIL = "package.service_fail"
    PACKAGE_VERSION_CHANGE = "package.version_change"
    PACKAGE_COMMENT = "package.comment"
    PROJECT_CREATE = "project.create"
    PROJECT_UPDATE_PROJECT_CONF = "project.update_project_conf"
    PROJECT_UPDATE = "project.update"
    PROJECT_DELETE = "project.delete"
    PROJECT_UNDELETE = "project.undelete"
    PROJECT_COMMENT = "project.comment"
    REPO_PACKTRACK = "repo.packtrack"
    REPO_PUBLISH_STATE = "repo.publish_state"
    REPO_PUBLISHED = "repo.published"
    REPO_BUILD_STARTED = "repo.build_started"
    REPO_BUILD_FINISHED = "repo.build_finished"
    REPO_STATUS_REPORT = "repo.status_report"
    REQUEST_CREATE = "request.create"
    REQUEST_CHANGE = "request.change"
    REQUEST_DELETE = "request.delete"
    REQUEST_STATE_CHANGE = "request.state_change"
    REQUEST_REVIEW_WANTED = "request.review_wanted"
    REQUEST_REVIEW_CHANGED = "request.review_changed"
    REQUEST_REVIEWS_DONE = "request.reviews_done"
    REQUEST_COMMENT = "request.comment"
    REQUEST_STATUS_REPORT = "request.status_report"
    PUBLISHED_STATUS_REPORT = "published.status_report"
    CONTAINER_PUBLISHED = "container.published"
    RELATIONSHIP_CREATE = "relationship.create"
    RELATIONSHIP_DELETE = "relationship.delete"


@dataclass(frozen=True, kw_only=True, slots=True)
class ObsMessageBusPayloadBase(metaclass=ABCMeta):
    """Base class for all rabbitmq message payloads from OBS."""

    pass


class PackageBuildSuccessPayload(ObsMessageBusPayloadBase):
    """Payload of the ``.package.build_success`` message."""

    project: str
    package: str
    repository: str
    arch: str
    release: str | None = None
    readytime: str
    srcmd5: str
    rev: str | None = None
    reason: str
    bcnt: str | None = None
    verifymd5: str | None = None
    starttime: str
    endtime: str
    workerid: str
    versrel: str | None = None
    buildtype: str
    previouslyfailed: int | None = None


class PackageBuildFailurePayload(PackageBuildSuccessPayload):
    """Payload of the ``.package.build_failed`` message."""

    successive_failcount: int


class PackageBuildUnchangedPayload(PackageBuildSuccessPayload):
    """Payload of the ``.package.build_unchanged`` message."""

    pass


class PackageCreatePayload(ObsMessageBusPayloadBase):
    """Payload of the ``.package.create`` message."""

    project: str
    package: str
    sender: str | None = None


class PackageUpdatePayload(PackageCreatePayload):
    """Payload of the ``.package.update`` message."""


class PackageDeletePayload(PackageCreatePayload):
    """Payload of the ``.package.delete`` message."""

    requestid: int | None = None
    comment: str | None = None


class PackageUndeletePayload(PackageDeletePayload):
    """Payload of the ``.package.undelete`` message."""


class PackageBranchPayload(ObsMessageBusPayloadBase):
    """Payload of the ``.package.branch`` message."""

    project: str | None = None
    package: str
    sender: str | None = None
    targetproject: str | None = None
    targetpackage: str | None = None
    user: str


class PackageCommitPayload(PackageDeletePayload):
    """Payload of the ``.package.commit`` message."""

    user: str
    files: str | None = None
    rev: str


class PackageUploadPayload(PackageDeletePayload):
    """Payload of the ``.package.upload`` message."""

    filename: str
    target: str | None = None
    user: str
    meta: int | None = None


class PackageServiceSuccessPayload(PackageDeletePayload):
    """Payload of the ``.package.service_success`` message."""

    rev: str
    user: str
    requestid: int | None = None


class PackageServiceFailPayload(PackageServiceSuccessPayload):
    """Payload of the ``.package.service_fail`` message."""

    error: str


class PackageVersionChangePayload(PackageServiceSuccessPayload):
    """Payload of the ``.package.version_change`` message."""

    newversion: str
    oldversion: str
    files: str


class PackageCommentPayload(PackageCreatePayload):
    """Payload of the ``.package.comment`` message."""

    id: int
    commenters: str
    commenter: str
    comment_body: str
    comment_title: str | None = None
    when: str | None = None


class ProjectCreatePayload(ObsMessageBusPayloadBase):
    """Payload of the ``.project.create`` message."""

    project: str
    sender: str


class ProjectUpdateProjectConfPayload(ProjectCreatePayload):
    """Payload of the ``.project.update_project_conf`` message."""

    files: str | None = None
    comment: str | None = None


class ProjectUpdatePayload(ProjectCreatePayload):
    """Payload of the ``.project.update`` message."""


class ProjectUndeletePayload(ProjectCreatePayload):
    """Payload of the ``.project.undelete`` message."""

    comment: str


class ProjectDeletePayload(ProjectUndeletePayload):
    """Payload of the ``.project.delete`` message."""

    requestid: int | None = None


class ProjectCommentPayload(ObsMessageBusPayloadBase):
    """Payload of the ``.project.comment`` message."""

    id: int
    project: str
    commenters: list[str]
    commenter: str
    comment_body: str
    comment_title: str | None = None
    when: str


class RepoPublishPayload(ObsMessageBusPayloadBase):
    """Payload of the ``.repo.publish`` message, it is emitted when a repository
    is published.

    """

    project: str
    repo: str
    buildid: str | None = None


class RepoPacktrackPayload(RepoPublishPayload):
    """Payload of the ``.repo.packtrack`` message, it is emitted when a binary
    is published into a repository.

    """

    payload: str


class RepoPublishStatePayload(RepoPublishPayload):
    """Payload of the ``.repo.publish_state`` message, it is emitted when the
    publish state of a repository changes.

    """

    state: str


class RepoBuildStartedPayload(RepoPublishPayload):
    """Payload of the ``.repo.build_started`` message, it is emitted when a
    repository started building.

    """

    arch: str


class RepoBuildFinishedPayload(RepoBuildStartedPayload):
    """Payload of the ``.repo.build_finished`` message, it is emitted when a
    repository finished building.

    """


class RepoStatusReportPayload(RepoBuildStartedPayload):
    """Payload of the ``.repo.status_report`` message, it is emitted when a
    status report was created for a finished repository

    """

    who: str
    short_description: str | None = None
    name: str
    state: str
    url: str


@dataclass(frozen=True, kw_only=True, slots=True)
class ActionPayload:
    action_id: int
    type: str
    sourceproject: str | None
    sourcepackage: str | None
    sourcerevision: str | None
    targetproject: str
    targetpackage: str | None
    makeoriginolder: bool | None
    sourceupdate: str | None


class RequestChangedPayload(ObsMessageBusPayloadBase):
    id: int
    author: str
    comment: str | None = None
    description: str | None = None
    namespace: str
    number: int
    actions: list[ActionPayload]
    state: RequestStatus
    when: str
    who: str


class RequestCreatePayload(RequestChangedPayload):
    diff: str | None = None


class RequestDeletePayload(RequestChangedPayload):
    pass


class RequestStateChangedPayload(RequestChangedPayload):
    id: int
    oldstate: str
    duration: int | None = None


class RequestReviewChangedPayload(ObsMessageBusPayloadBase):
    id: int
    number: int
    author: str
    comment: str | None = None
    description: str | None = None
    actions: list[ActionPayload]
    state: str
    when: str
    who: str
    namespace: str
    reviewers: str | None = None
    by_user: str | None = None
    by_group: str | None = None
    by_project: str | None = None
    by_package: str | None = None


class RequestReviewWantedPayload(RequestChangedPayload):
    reviewers: str | None
    by_user: str | None = None
    by_group: str | None = None
    by_project: str | None = None
    by_package: str | None = None


class RequestReviewsDonePayload(RequestReviewChangedPayload):
    author: str
    number: int
    actions: list[ActionPayload]
    state: str
    when: str
    who: str


class RequestCommentPayload(RequestChangedPayload):
    commenters: list[str]
    commenter: str
    comment_body: str
    comment_title: str | None = None
    # useless field, use number instead
    request_number: int | None = None
    diff_ref: str | None = None


class RequestStatusReportPayload(ObsMessageBusPayloadBase):
    number: int


class PublishedStatusReportPayload(ObsMessageBusPayloadBase):
    project: str
    repo: str
    buildid: str
    who: str
    name: str
    state: str
    url: str


class ContainerPublishedPayload(ObsMessageBusPayloadBase):
    project: str
    repo: str
    buildid: str
    container: str


class RelationshipCreatePayload(ObsMessageBusPayloadBase):
    who: str
    user: str | None = None
    project: str
    package: str | None = None
    group: str | None = None
    role: str
    notifiable_id: int


class RelationshipDeletePayload(RelationshipCreatePayload):
    pass


QUEUE_TO_PAYLOAD_TYPE: Dict[RoutingKey, Type[ObsMessageBusPayloadBase]] = {
    # package
    RoutingKey.PACKAGE_BUILD_SUCCESS: PackageBuildSuccessPayload,
    RoutingKey.PACKAGE_BUILD_FAILURE: PackageBuildFailurePayload,
    RoutingKey.PACKAGE_BUILD_UNCHANGED: PackageBuildUnchangedPayload,
    RoutingKey.PACKAGE_CREATE: PackageCreatePayload,
    RoutingKey.PACKAGE_UPDATE: PackageUpdatePayload,
    RoutingKey.PACKAGE_DELETE: PackageDeletePayload,
    RoutingKey.PACKAGE_UNDELETE: PackageUndeletePayload,
    RoutingKey.PACKAGE_BRANCH: PackageBranchPayload,
    RoutingKey.PACKAGE_COMMIT: PackageCommitPayload,
    RoutingKey.PACKAGE_UPLOAD: PackageUploadPayload,
    RoutingKey.PACKAGE_SERVICE_FAIL: PackageServiceFailPayload,
    RoutingKey.PACKAGE_SERVICE_SUCEESS: PackageServiceSuccessPayload,
    RoutingKey.PACKAGE_VERSION_CHANGE: PackageVersionChangePayload,
    RoutingKey.PACKAGE_COMMENT: PackageCommentPayload,
    # project
    RoutingKey.PROJECT_CREATE: ProjectCreatePayload,
    RoutingKey.PROJECT_UPDATE_PROJECT_CONF: ProjectUpdateProjectConfPayload,
    RoutingKey.PROJECT_UPDATE: ProjectUpdatePayload,
    RoutingKey.PROJECT_DELETE: ProjectDeletePayload,
    RoutingKey.PROJECT_UNDELETE: ProjectUndeletePayload,
    RoutingKey.PROJECT_COMMENT: ProjectCommentPayload,
    # repo
    RoutingKey.REPO_PACKTRACK: RepoPacktrackPayload,
    RoutingKey.REPO_PUBLISH_STATE: RepoPublishStatePayload,
    RoutingKey.REPO_PUBLISHED: RepoPublishPayload,
    RoutingKey.REPO_BUILD_STARTED: RepoBuildStartedPayload,
    RoutingKey.REPO_BUILD_FINISHED: RepoBuildFinishedPayload,
    RoutingKey.REPO_STATUS_REPORT: RepoStatusReportPayload,
    # request
    RoutingKey.REQUEST_CREATE: RequestCreatePayload,
    RoutingKey.REQUEST_CHANGE: RequestChangedPayload,
    RoutingKey.REQUEST_DELETE: RequestDeletePayload,
    RoutingKey.REQUEST_STATE_CHANGE: RequestStateChangedPayload,
    RoutingKey.REQUEST_REVIEW_WANTED: RequestReviewWantedPayload,
    RoutingKey.REQUEST_REVIEW_CHANGED: RequestReviewChangedPayload,
    RoutingKey.REQUEST_REVIEWS_DONE: RequestReviewsDonePayload,
    RoutingKey.REQUEST_COMMENT: RequestCommentPayload,
    RoutingKey.REQUEST_STATUS_REPORT: RequestStatusReportPayload,
    # published
    RoutingKey.PUBLISHED_STATUS_REPORT: PublishedStatusReportPayload,
    # container
    RoutingKey.CONTAINER_PUBLISHED: ContainerPublishedPayload,
    # relationship
    RoutingKey.RELATIONSHIP_CREATE: RelationshipCreatePayload,
    RoutingKey.RELATIONSHIP_DELETE: RelationshipDeletePayload,
}
