# run release tasks
[group('release')]
release: release-test-wheel release-test-source release-package

# smoke test wheel
[group('release')]
release-test-wheel: package-build
    uv run --isolated --no-project --with dist/*.whl tests/smoke_test.py

# smoke test source distribution
[group('release')]
release-test-source: package-build
    uv run --isolated --no-project --with dist/*.tar.gz tests/smoke_test.py

# publish python package
[group('release')]
release-package: package-build release-test-wheel release-test-source
	uv publish
