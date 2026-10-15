"""Explicit provider envelopes survive executor/worker/client boundaries."""
import pytest

from astrid.core.execution.generic_host import RuntimeProtocolClient
from astrid.core.execution.provider_failure import ProviderFailure, provider_failure
from tests.core.execution.test_generic_host_actions_v3 import pack, invoke


@pytest.mark.parametrize("retryable", [True, False])
def test_python_executor_provider_rejection_survives_real_child(tmp_path, retryable):
    _, host, _, definition, admission = pack(tmp_path, code=f'''
from astrid.core.execution.provider_failure import ProviderFailure
def run(value):
    raise ProviderFailure('fake provider rejection', provider_id='fake', retryable={retryable}, retry_after_seconds=7)
''')
    with pytest.raises(ProviderFailure, match="fake provider rejection") as caught:
        invoke(tmp_path, host, definition, admission)
    error = caught.value.to_envelope()
    assert error["retryable"] is retryable
    assert error["retry_after_seconds"] == 7
    assert error["provider_id"] == "fake"


def test_failure_client_preserves_provider_fields_and_attempt_identity():
    class Generated:
        def health(self):
            return {"runtime_epoch": 7}

        def fail_attempt(self, attempt_id, **kwargs):
            self.called = (attempt_id, kwargs)
    client = object.__new__(RuntimeProtocolClient)
    client.generated = Generated()
    client._attempt_runtime_epochs = {"attempt": 7}
    error = ProviderFailure("429", provider_id="fake", retryable=True, retry_after_seconds=9).to_envelope()
    client.fail("task", "lease", error, attempt_id="attempt", fence=3)
    attempt, call = client.generated.called
    assert attempt == "attempt"
    assert call["error"] == error
    assert call["runtime_epoch"] == 7
    assert call["lease_id"] == "lease" and call["fence"] == 3
    assert call["idempotency_key"] == "fail-attempt-3"


@pytest.mark.parametrize("changes", [{"retryable": "true"}, {"retry_after_seconds": -1},
    {"retry_after_seconds": float("inf")}, {"provider_id": ""}, {"code": "timeout"}])
def test_malformed_or_ambiguous_errors_never_opt_into_retry(changes):
    error = ProviderFailure("429", provider_id="fake", retryable=True).to_envelope()
    assert provider_failure({**error, **changes}) is None
