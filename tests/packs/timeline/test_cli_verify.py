"""The verify lane's CLI adapters: --labels (check, verify, visualize). --timings belongs to the fast lane (see report)."""
from __future__ import annotations

import argparse

from astrid.packs.timeline import cli_verify


def test_the_labels_flag_parses_for_check_and_verify():
    parser = argparse.ArgumentParser()
    cli_verify.add_labels_flag(parser)
    assert parser.parse_args([]).labels is False
    assert parser.parse_args(["--labels"]).labels is True
    assert "address" in parser.format_help()


def test_the_visualize_labels_shorthand_adds_the_labels_layer_once():
    parser = argparse.ArgumentParser()
    cli_verify.add_visualize_labels_flag(parser)
    assert parser.parse_args(["--labels"]).labels is True
    assert cli_verify.with_labels_layer(["sync"], True) == ["sync", "labels"]
    assert cli_verify.with_labels_layer(["labels", "sync"], True) == ["labels", "sync"]
    assert cli_verify.with_labels_layer(None, True) == ["labels"]
    assert cli_verify.with_labels_layer(["sync"], False) == ["sync"]
    assert cli_verify.with_labels_layer(None, False) is None
