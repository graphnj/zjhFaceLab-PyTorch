from PIL import Image,ImageDraw
from mtcnn.detector import detect_faces
from mtcnn.align_trans import get_reference_facial_points, warp_and_crop_face
import numpy as np
import os
from tqdm import tqdm
import argparse
import torch

class MtcnnDetector(object):
    def __init__(self,model_folder, ctx=torch.device("cuda:0" if torch.cuda.is_available() else "cpu")):
        scale = crop_size / 112.
        reference = get_reference_facial_points(default_square = True) * scale
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "face alignment")
    parser.add_argument("-source_root", "--source_root", help = "specify your source dir", default = "../data/test", type = str)
    parser.add_argument("-dest_root", "--dest_root", help = "specify your destination dir", default = "../data/test_Aligned", type = str)
    parser.add_argument("-crop_size", "--crop_size", help = "specify size of aligned faces, align and crop with padding", default = 112, type = int)
    args = parser.parse_args()

    source_root = args.source_root # specify your source dir
    dest_root = args.dest_root # specify your destination dir
    crop_size = args.crop_size # specify size of aligned faces, align and crop with padding

    source_root = '../../data/'
    dest_root   = '../../data/'
    scale = crop_size / 112.
    reference = get_reference_facial_points(default_square = True) * scale

    cwd = os.getcwd() # delete '.DS_Store' existed in the source_root
    os.chdir(source_root)
    os.system("find . -name '*.DS_Store' -type f -delete")
    os.chdir(cwd)

    if not os.path.isdir(dest_root):
        os.mkdir(dest_root)

    for subfolder in tqdm(os.listdir(source_root)):
        if not os.path.isdir(os.path.join(dest_root, subfolder)):
            os.mkdir(os.path.join(dest_root, subfolder))
        for image_name in os.listdir(os.path.join(source_root, subfolder)):
            print("Processing\t{}".format(os.path.join(source_root, subfolder, image_name)))
            img = Image.open(os.path.join(source_root, subfolder, image_name))
            try: # Handle exception
                _, landmarks = detect_faces(img)
            except Exception as e:
                print("{} is discarded due to exception!".format(os.path.join(source_root, subfolder, image_name)))
                continue
            if len(landmarks) == 0: # If the landmarks cannot be detected, the img will be discarded
                print("{} is discarded due to non-detected landmarks!".format(os.path.join(source_root, subfolder, image_name)))
                continue

            saveAllExistFace=True
            facecnt=1
            if saveAllExistFace:
                facecnt=len(landmarks)
            draw=ImageDraw.Draw(img)
            for i in range(facecnt):
                facial5points = [[landmarks[i][j], landmarks[i][j + 5]] for j in range(5)]

                facial5points_tuple=[(landmarks[i][j],landmarks[i][j+5]) for j in range(5)]
                draw.polygon(facial5points_tuple,fill= (255, 0, 0))

                warped_face = warp_and_crop_face(np.array(img), facial5points, reference, crop_size=(crop_size, crop_size))
                img_warped = Image.fromarray(warped_face)
                dstimage_name = '.'.join(image_name.split('.')[:-1]) + '_aligned_%d.jpg'%i
                img_warped.save(os.path.join(dest_root, subfolder, dstimage_name))
            img.save(os.path.join(dest_root, subfolder,'.'.join(image_name.split('.')[:-1]) + '_0facial5points.jpg'))