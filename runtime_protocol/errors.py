from enum import Enum


class AuthorizationGuard(Enum):
    """Internal source-site codes; never serialized into public error details."""

    UNKNOWN = ('unknown', 'unknown')
    CREDENTIAL_FORMAT_UNSUPPORTED = ('credential', 'format_unsupported')
    CREDENTIAL_BEARER_INVALID = ('credential', 'bearer_invalid')
    CREDENTIAL_BEARER_REQUIRED = ('credential', 'bearer_required')
    CREDENTIAL_EXPIRED = ('credential', 'expired')
    CREDENTIAL_SCOPE_REQUIRED = ('credential', 'scope_required')
    CREDENTIAL_BINDING_SCOPE_REQUIRED = ('credential', 'binding_scope_required')
    CREDENTIAL_DISABLED = ('credential', 'disabled')
    CREDENTIAL_BINDING_CHANGED = ('credential', 'binding_changed')
    CREDENTIAL_BINDING_UNAVAILABLE = ('credential', 'binding_unavailable')
    CREDENTIAL_METADATA_INVALID = ('credential', 'metadata_invalid')
    PUBLISHER_REQUIRED = ('publisher', 'required')
    PUBLISHER_ACTOR_MISMATCH = ('publisher', 'actor_mismatch')
    COMMIT_CAPTURE_MEDIA_REALM = ('commit_capture', 'media_realm')
    COMMIT_CAPTURE_NARRATION_REALM = ('commit_capture', 'narration_realm')
    COMMIT_CAPTURE_NARRATION_PROJECT = ('commit_capture', 'narration_project')
    COMMIT_CAPTURE_DUPLICATE_PROVENANCE = ('commit_capture', 'duplicate_provenance')
    COMMIT_CAPTURE_MEDIA_SELECTION = ('commit_capture', 'media_selection')
    COMMIT_CAPTURE_DRY_RUN_ACCEPT = ('commit_capture', 'dry_run_accept')
    COMMIT_CAPTURE_ACCEPTANCE_IDENTITY = ('commit_capture', 'acceptance_identity')
    COMMIT_CAPTURE_DRY_RUN_RESULT = ('commit_capture', 'dry_run_result')
    COMMIT_CAPTURE_REVISION_CLOSURE = ('commit_capture', 'revision_closure')
    COMMIT_CAPTURE_DUPLICATE_BOOTSTRAP = ('commit_capture', 'duplicate_bootstrap')
    COMMIT_CAPTURE_NARRATION_TAKE = ('commit_capture', 'narration_take')
    AUTHORING_INVOCATION_OWNER_UNAVAILABLE = ('authoring_invocation', 'owner_unavailable')
    AUTHORING_INVOCATION_VALIDATION_MISSING = ('authoring_invocation', 'validation_missing')
    AUTHORING_INVOCATION_EVALUATION_MISSING = ('authoring_invocation', 'evaluation_missing')
    AUTHORING_INVOCATION_SESSION_REQUIRED = ('authoring_invocation', 'session_required')
    AUTHORING_INVOCATION_WORKER_DENIED = ('authoring_invocation', 'worker_denied')
    AUTHORING_INVOCATION_PROJECT_REALM = ('authoring_invocation', 'project_realm')
    AUTHORING_INVOCATION_BINDING_CHANGED = ('authoring_invocation', 'binding_changed')
    AUTHORING_INVOCATION_CANDIDATE_PROOF = ('authoring_invocation', 'candidate_proof')
    AUTHORING_INVOCATION_ISSUER_UNAVAILABLE = ('authoring_invocation', 'issuer_unavailable')
    AUTHORING_INVOCATION_REVOKED = ('authoring_invocation', 'revoked')
    AUTHORING_INVOCATION_OWNER_CHANGED = ('authoring_invocation', 'owner_changed')
    AUTHORING_INVOCATION_DEPENDENCY_SCOPE = ('authoring_invocation', 'dependency_scope')
    AUTHORING_INVOCATION_HOST_CHANGED = ('authoring_invocation', 'host_changed')
    AUTHORING_INVOCATION_ASSET_SCOPE = ('authoring_invocation', 'asset_scope')
    TRANSCRIPT_CAPTURE_REQUEST_IDENTITY = ('transcript_capture', 'request_identity')
    TRANSCRIPT_CAPTURE_ISSUER_UNAVAILABLE = ('transcript_capture', 'issuer_unavailable')
    IDENTITY_RUNTIME_CLOSED = ('identity', 'runtime_closed')
    IDENTITY_BEARER_REQUIRED = ('identity', 'bearer_required')
    IDENTITY_COMMIT_SCOPE_REQUIRED = ('identity', 'commit_scope_required')
    COMMIT_AUTHORITY_PAIRED_SESSION_REQUIRED = ('commit_authority', 'paired_session_required')
    TRANSCRIPT_CAPTURE_SCOPE_REQUIRED = ('transcript_capture', 'scope_required')


class AuthoringInvocationRevocationReason(Enum):
    """Internal first-failing clause; never part of the public error envelope."""

    EVALUATION_CANCELLED = "evaluation_cancelled"
    CAPTURED_RELAY_ABSENT = "captured_relay_absent"
    CURRENT_RELAY_REPLACED = "current_relay_replaced"


class RuntimeErrorBase(Exception):
    code = "runtime_error"
    status = 400

    def __init__(self, message: str, *, details=None):
        super().__init__(message)
        self.message = message
        self.details = details

    def as_dict(self):
        result = {"code": self.code, "message": self.message}
        if self.details is not None:
            result["details"] = self.details
        return result


class AuthorizationError(RuntimeErrorBase):
    code = "unauthorized"
    status = 401

    def __init__(self, message: str, *, details=None, guard=AuthorizationGuard.UNKNOWN,
                 invocation_reason=None):
        super().__init__(message, details=details)
        self._authorization_guard = guard if type(guard) is AuthorizationGuard else AuthorizationGuard.UNKNOWN
        self._authoring_invocation_reason = (
            invocation_reason if type(invocation_reason) is AuthoringInvocationRevocationReason else None
        )


class ConflictError(RuntimeErrorBase):
    code = "conflict"
    status = 409


class NoCommittedRequestError(ConflictError):
    """Replay-only lookup found no matching committed mutation."""

    code = "no_committed_request"


class ValidationError(RuntimeErrorBase):
    code = "validation_error"
    status = 422


class ForbiddenError(RuntimeErrorBase):
    code = "forbidden"
    status = 403


class CapabilityUnavailableError(ConflictError):
    """Admission failed because the registered capability is not ready."""

    # Keep Astrid's frozen SDK taxonomy.  The capability-specific reason and
    # next action are carried in bounded details, not a new machine code.
    code = "unavailable"


class NotFoundError(RuntimeErrorBase):
    code = "not_found"
    status = 404


class RetiredRouteError(RuntimeErrorBase):
    """A public compatibility route removed by the canonical timeline cutover."""

    code = "retired_route"
    status = 410


class OwnerBusyError(ConflictError):
    code = "owner_busy"


class RealmAdmissionError(ConflictError):
    """An existing realm failed the bounded, read-only startup gate."""

    code = "realm_admission_failed"


class LeaseError(ConflictError):
    code = "lease_fenced"


class ProtocolError(RuntimeErrorBase):
    code = "protocol_error"
    status = 400


class InvalidRequestError(RuntimeErrorBase):
    """A syntactically valid request with an invalid JSON shape."""

    code = "invalid_request"
    status = 400
