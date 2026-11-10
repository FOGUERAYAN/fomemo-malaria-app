import pytest
from PIL import Image

pytest.importorskip("numpy")
from utils.inference import is_uncertain, preprocess, validate_image


def test_preprocess_shape_and_range():
    arr = preprocess(Image.new("RGB", (200, 180), (255, 0, 0)), (64, 48, 3))
    assert arr.shape == (1, 64, 48, 3)
    assert arr.max() <= 1.0 and arr.min() >= 0.0


def test_preprocess_converts_grayscale_to_rgb():
    assert preprocess(Image.new("L", (50, 50)), (32, 32, 3)).shape == (1, 32, 32, 3)


def test_validation():
    assert validate_image(Image.new("RGB", (100, 100))) == []
    assert validate_image(Image.new("RGB", (10, 10)))
    assert validate_image(Image.new("RGB", (400, 100)))


def test_uncertain():
    assert is_uncertain(0.5) and not is_uncertain(0.95) and not is_uncertain(0.02)
