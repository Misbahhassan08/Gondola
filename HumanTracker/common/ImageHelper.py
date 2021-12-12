
import cv2

class ImageHelper:
    @staticmethod
    def resize(image, width = None, height = None, inter = cv2.INTER_AREA):
        # initialize the dimensions of the image to be resized and
        # grab the image size
        dim = None
        (h, w) = image.shape[:2]

        # if both the width and height are None, then return the
        # original image
        if width is None and height is None:
            return image

        # check to see if the width is None
        if width is None:
            # calculate the ratio of the height and construct the
            # dimensions
            r = height / float(h)
            dim = (int(w * r), height)

        # otherwise, the height is None
        else:
            # calculate the ratio of the width and construct the
            # dimensions
            r = width / float(w)
            dim = (width, int(h * r))

        # resize the image
        resized = cv2.resize(image, dim, interpolation = inter)

        # return the resized image
        return resized

    @staticmethod
    def get_bbox(image, bBox):
        image_height, image_width, _ = image.shape
        start_x = int(bBox.xmin * image_width)
        start_y = int(bBox.ymin * image_height)
        end_x = start_x + int(bBox.width * image_width)
        end_y = start_y + int(bBox.height * image_height)
        return (start_x, start_y), (end_x, end_y), end_x - start_x, end_y- start_y