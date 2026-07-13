#app\services\image_processing\exceptions.py
class ImageProcessingError(Exception):
    """
    Error base del módulo de procesamiento de imágenes.
    """

    pass


class ImageProcessingConfigurationError(ImageProcessingError):
    """
    Error en la configuración del procesamiento.
    """

    pass


class ImageProcessingExecutionError(ImageProcessingError):
    """
    Error durante la ejecución de una operación.
    """

    pass