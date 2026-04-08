# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 XCENA Inc.
# Unit tests verifying that core maru packages can be imported successfully.

import importlib


class TestSetup:
    # Test that core maru packages are importable.

    def test_import_maru_common(self):
        # maru_common package should be importable.
        mod = importlib.import_module("maru_common")
        assert mod is not None

    def test_import_maru_common_logging_setup(self):
        # maru_common.logging_setup module should be importable.
        mod = importlib.import_module("maru_common.logging_setup")
        assert hasattr(mod, "setup_package_logging")

    def test_import_maru_common_config(self):
        # maru_common.config module should be importable.
        mod = importlib.import_module("maru_common.config")
        assert mod is not None

    def test_import_maru_common_protocol(self):
        # maru_common.protocol module should be importable.
        mod = importlib.import_module("maru_common.protocol")
        assert mod is not None
