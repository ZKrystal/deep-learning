import os
import random
import shutil


#  将jpg图片转化为png
from PIL import Image


def transform(root_dir,img_file,out_file):
    input_folder = os.path.join(root_dir, img_file)
    output_folder = os.path.join(root_dir, out_file)
    # 循环遍历原始图片文件夹中的所有jpg图片
    num = 0
    for filename in os.listdir(input_folder):
        if filename.endswith('.bmp'):
            # 打开jpg图片文件
            img = Image.open(os.path.join(input_folder, filename))
            # 生成输出png图片的文件名
            output_filename = os.path.splitext(filename)[0] + '.jpg'

            # 保存png图片到输出图片文件夹
            # os.remove(os.path.join(input_folder, filename))
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            img.save(os.path.join(output_folder, output_filename))
            num = num + 1
            print("{}转化成功".format(os.path.splitext(filename)), num)

def dataset():
    img_path = os.path.join(root_dir, img_file)
    img_names = [n for n in os.listdir(img_path) if n.endswith('.jpg') or n.endswith('.png')]
    path_imgs = [os.path.join(img_path, name) for name in img_names]

    random.seed(2020393)
    random.shuffle(path_imgs)

    train_ratios = int(len(path_imgs) * train_ratio)
    val_ratios = int(len(path_imgs) * (train_ratio + val_ratio))

    train_dataset = path_imgs[:train_ratios]
    val_dataset = path_imgs[train_ratios:val_ratios]
    test_dateset = path_imgs[val_ratios:]

    label_train = label(train_dataset, img_path)
    label_val = label(val_dataset, img_path)
    label_test = label(test_dateset, img_path)

    save_img(train_dataset, save_dirs, "train")
    save_img(val_dataset, save_dirs, "val")
    save_img(test_dateset, save_dirs, "test")

    save_label(label_train, save_dirs, "train")
    save_label(label_val, save_dirs, "val")
    save_label(label_test, save_dirs, "test")


def label(dataset, img_path):
    label_data_list = []
    for data in dataset:
        if data[-4:] == '.png':
            tran = data[len(img_path) + 1:].replace('.png', '.txt', 1)
        else:
            tran = data[len(img_path) + 1:].replace('.jpg', '.txt', 1)
        label_path = os.path.join(root_dir, label_file, tran)
        if os.path.exists(label_path):
           label_data_list.append(label_path)
        else:
            continue
    return label_data_list


def save_img(imgs, save_dirs, datasetname):
    data_dir = os.path.join(save_dirs, 'images', datasetname)
    if not os.path.isdir(data_dir): os.makedirs(data_dir)
    for index, path_img in enumerate(imgs):
        print("{}/{}".format(index, data_dir))
        shutil.copy(path_img, data_dir)


def save_label(imgs, save_dirs, datasetname):

    data_dir = os.path.join(save_dirs, 'labels', datasetname)
    if not os.path.isdir(data_dir): os.makedirs(data_dir)
    for index, path_img in enumerate(imgs):
        print("{}/{}".format(index, data_dir))
        shutil.copy(path_img, data_dir)


if __name__ == '__main__':
    train_ratio = 0.8
    val_ratio = 0.1
    root_dir = r'../../data'
    # img_file = 'JPEGImagess'   # 标签所在目录
    img_file = 'imagess'  # 图片所在目录名
    label_file = 'Annotations'  # 标签所在目录名
    save_dirs = r'../../data/datasets'  # 保存路径
    out_file = 'imagess'
    # 图片转化
    # transform(root_dir,img_file,out_file)
    # 图片划分
    dataset()
