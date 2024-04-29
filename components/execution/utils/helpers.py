import cv2
from numpy import ndarray
from io import BytesIO
def np_array_to_BytesIO_stream(np_array:ndarray,extension:str)->BytesIO:
    #converting image to stream. needed for s3 uploadObj
    success,encoded_image = cv2.imencode(f".{extension}", np_array)
    if not success:
        raise "Couldn't encode Image"
    image_stream = BytesIO()
    image_stream.write(encoded_image.tobytes())
    image_stream.seek(0)
    return image_stream