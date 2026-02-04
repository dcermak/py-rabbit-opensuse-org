"""Test that pydantic backend is correctly selected and used."""

from pydantic import BaseModel


def test_pydantic_backend_is_used():
    """Verify that payload classes use the pydantic backend."""
    from py_rodo import PackageBuildSuccessPayload

    payload = PackageBuildSuccessPayload(
        project="test-project",
        package="test-package",
        repository="test-repo",
        arch="x86_64",
        readytime="2021-01-01T00:00:00",
        srcmd5="abc123",
        reason="test",
        starttime="2021-01-01T00:00:00",
        endtime="2021-01-01T00:01:00",
        workerid="test-worker",
        buildtype="test",
    )

    assert isinstance(payload, BaseModel), "Payload should be a pydantic BaseModel"
    assert "pydantic" in payload.__class__.__bases__[0].__module__, (
        "Base class should be from py_rodo.backends.pydantic"
    )
