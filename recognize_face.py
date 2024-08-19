from seetaface.api import *


def recognize_face(image_1, image_2):
    init_mask = FACE_DETECT | FACERECOGNITION | LANDMARKER5
    seetaFace = SeetaFace(init_mask)
    feature1 = seetaFace.ExtractCroppedFace(image_1)
    feature2 = seetaFace.ExtractCroppedFace(image_2)

    similar = seetaFace.CalculateSimilarity(feature1, feature2)
    return similar


if __name__ == '__main__':
    image1 = cv2.imread("asserts/crop1.jpg")

    image2 = cv2.imread("asserts/crop2.jpg")

    print(recognize_face(image1, image2))
