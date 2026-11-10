"""Prétraitement et validation des images (sans dépendance à TensorFlow, donc testable)."""
import numpy as np
from PIL import Image

MIN_SIDE = 32
MAX_ASPECT_RATIO = 1.5
UNCERTAIN_RANGE = (0.35, 0.65)


def validate_image(image: Image.Image) -> list:
    """Retourne la liste des problèmes bloquants (vide si l'image est exploitable)."""
    w, h = image.size
    errors = []
    if min(w, h) < MIN_SIDE:
        errors.append(f"Image trop petite ({w}×{h} px) : minimum {MIN_SIDE} px de côté.")
    elif max(w, h) / min(w, h) > MAX_ASPECT_RATIO:
        errors.append(
            "Format très allongé : le modèle attend l'image d'une seule cellule (cadrage proche du carré), "
            "pas un frottis entier."
        )
    return errors


def preprocess(image: Image.Image, input_shape) -> np.ndarray:
    """Redimensionne selon (hauteur, largeur, canaux) du modèle, normalise dans [0, 1], ajoute l'axe batch."""
    height, width = int(input_shape[0]), int(input_shape[1])
    arr = np.asarray(image.convert("RGB").resize((width, height)), dtype="float32") / 255.0
    return np.expand_dims(arr, axis=0)


def is_uncertain(probability: float) -> bool:
    low, high = UNCERTAIN_RANGE
    return low <= probability <= high
