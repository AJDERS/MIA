import os
import imageio
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import image as mpimg

class Loader():

    def __init__(self, path):
        current_path = os.getcwd()
        self.ab_path = os.path.join(current_path, path)

    def load_im(self):
        # Check if a folder.
        if self.check_if_folder():
            print('Assuming data is DICOM.')
            vol = imageio.volread(self.ab_path,'DICOM')
            return (vol, 'DICOM')

        self.file_extension = self.check_format()
        if self.file_extension in ['.gz', '.nii']:
            print('Assuming data is Nifty.')
            vol = nib.load('./sub3.nii.gz') 
            return (vol, 'NIFTY')
        else:
            print('Assuming data is single image.')
            vol = mpimg.imread(self.ab_path)
            return (vol, 'Image {}'.format(self.file_extension))

    def plot(self):
        (vol, type_) = self.load_im()
        self.data = vol
        if 'Image' in type_:
            print('Path {} \n'.format(self.ab_path))
            print('File extension {}'.format(self.file_extension))
            plt.imshow(vol, cmap='inferno')
        else:
            _, axes = plt.subplots(nrows=3, ncols=4)
            if 'DICOM' in type_:
                print('Available metadata:', vol.meta.keys())
                print('Shape of image array:', vol.shape)
            if 'NIFTY' in type_:
                print('Available metadata:', vol.header.keys())
                print('Shape of image array:', vol.shape)
                vol = vol.get_fdata()
            print('Every 60th frame from each dimension.')
            for i in range(3):
              for j in range(4):
                # Loop through subplots and draw image
                if i == 0:
                  axes[i, j].imshow(vol[j*60, :, :],cmap='gray')
                  axes[i, j].axis('off')
                elif i == 1:
                  axes[i, j].imshow(vol[:, j*60, :],cmap='gray')
                  axes[i, j].axis('off')
                else:
                  axes[i, j].imshow(vol[:, :, j*60],cmap='gray')
                  axes[i, j].axis('off')

            # Render the figure
            plt.show()

    def check_if_folder(self):
        try:
            os.listdir(self.ab_path)
            return True
        except NotADirectoryError:
            return False

    def check_format(self):
        _, file_extension = os.path.splitext(self.ab_path)
        return file_extension


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Load and plot')
    parser.add_argument('--path', metavar='path', required=True,
                        help='the path to the image data')
    args = parser.parse_args()
    l = Loader(path=args.path)
    l.plot()    