from django.core.exceptions import ValidationError

def validate_image_size(image):
    max = 200 * 1000 # 200kb
    if image.size > max:
        raise ValidationError(
            f"A imagem não pode ter mais de {max / 1000} KB."
        )