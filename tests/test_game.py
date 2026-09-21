import json

from app.game import evaluate_guess


def test_evaluate_guess_handles_all_statuses():
    assert evaluate_guess("trawa", "certa") == ["present", "present", "absent", "absent", "correct"]


def test_evaluate_guess_handles_duplicate_letters():
    assert evaluate_guess("aaaaa", "aabcd") == ["correct", "correct", "absent", "absent", "absent"]
