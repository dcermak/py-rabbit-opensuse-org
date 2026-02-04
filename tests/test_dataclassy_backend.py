"""Test that dataclassy backend is correctly selected and used."""


def test_dataclassy_backend_is_used():
    """Verify that payload classes use the dataclassy backend."""
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

    assert "dataclassy" in payload.__class__.__bases__[0].__module__, (
        "Base class should be from py_rodo.backends.dataclassy"
    )
