import imagedisplay
from skimage import data


def main():

    image = data.camera()
    imagedisplay.ImageDisplay(image)

if __name__ == "__main__":
    main()
