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

#executor helper
def report_failure(ch, method, properties, body):
    try:
        properties.headers = properties.headers or {"x-delivery-count":0}
        if(properties.headers.get("x-delivery-count")>=int(os.environ.get("MAX_RERUNS"))):
            database.update_dict(body["task_id"], {"status": "failed","rerun_count":int(properties.headers.get("x-delivery-count"))}) 
        else:   
            database.update_dict(body["task_id"], {"status": f"rerun {properties.headers.get('x-delivery-count')}","rerun_count":int(properties.headers.get("x-delivery-count"))}) 
    finally:
        ch.basic_nack(delivery_tag=method.delivery_tag)