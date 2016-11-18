import tensorflow as tf

def lrelu(x,leak=.2):
    return tf.maximum(x,leak*x)

def resize_image_with_crop_or_pad(image, target_height, target_width):
    image_shape = tf.shape(image)
    original_height = image_shape[0]
    original_width = image_shape[1]

    zero = tf.constant(0)
    half = tf.constant(2)

    offset_crop_width = tf.cond(
        tf.less(
            target_width,
            original_width),
        lambda: tf.floordiv(tf.sub(original_width, target_width), half),
        lambda: zero)

    offset_pad_width = tf.cond(
        tf.greater(
            target_width,
            original_width),
        lambda: tf.floordiv(tf.sub(target_width, original_width), half),
        lambda: zero)

    offset_crop_height = tf.cond(
        tf.less(
            target_height,
            original_height),
        lambda: tf.floordiv(tf.sub(original_height, target_height), half),
        lambda: zero)

    offset_pad_height = tf.cond(
        tf.greater(
            target_height,
            original_height),
        lambda: tf.floordiv(tf.sub(target_height, original_height), half),
        lambda: zero)

    cropped = crop_to_bounding_box(
        image, offset_crop_height, offset_crop_width,
        tf.minimum(target_height, original_height),
        tf.minimum(target_width, original_width))

    resized = pad_to_bounding_box(cropped, offset_pad_height, offset_pad_width,
                                  target_height, target_width)

    return resized


def crop_to_bounding_box(image, offset_height, offset_width, target_height,
                         target_width):
    cropped = tf.slice(
        image,
        tf.pack([offset_height, offset_width, 0]),
        tf.pack([target_height, target_width, -1]))

    return cropped


def pad_to_bounding_box(image, offset_height, offset_width, target_height,
                        target_width):
    image_shape = tf.shape(image)
    original_height = image_shape[0]
    original_width = image_shape[1]

    after_padding_width = tf.sub(
        tf.sub(target_width, offset_width),  original_width)
    after_padding_height = tf.sub(
        tf.sub(target_height, offset_height), original_height)

    paddings = tf.reshape(
        tf.pack(
            [offset_height, after_padding_height,
             offset_width, after_padding_width,
             0, 0]), [3, 2])

    padded = tf.pad(image, paddings)

    return padded
