# 处理labelme多边形矩阵的标注  json转化txt,提取点
import json
import os


name2id = {'Runway': 1, 'taxiway': 2}    #  修改你的类别并且赋与index


def decode_json(json_floder_path, txt_outer_path, json_name):
    txt_name = txt_outer_path + json_name[:-5] + '.txt'
    with open(txt_name, 'a') as f:
        json_path = os.path.join(json_floder_path, json_name)
        data = json.load(open(json_path, 'r', encoding='gb2312', errors='ignore'))
        img_w = data['imageWidth']
        img_h = data['imageHeight']
        isshape_type = data['shapes'][0]['shape_type']
        print(isshape_type)
        dw = 1. / (img_w)
        dh = 1. / (img_h)
        for i in data['shapes']:
            label_name = i['label']
            if (i['shape_type'] == 'polygon'):
                point = []
                for lk in range(len(i['points'])):
                    x = float(i['points'][lk][0])
                    y = float(i['points'][lk][1])
                    point_x = x * dw
                    point_y = y * dh
                    point.append(point_x)
                    point.append(point_y)
                f.write(str(name2id[label_name]) + " " + " ".join([str(a) for a in point]) + '\n')
        f.close()


if __name__ == "__main__":
    json_floder_path = r'D:/Aapythonproject\ultralytics-main\datarunway\json'  # 存放json的文件夹的绝对路径
    txt_outer_path = r'D:/Aapythonproject\ultralytics-main\datarunway\Annoatations/'  # 存放txt的文件夹绝对路径
    json_names = os.listdir(json_floder_path)
    flagcount = 0
    for json_name in json_names:
        decode_json(json_floder_path, txt_outer_path, json_name)
        flagcount += 1

    print('-----------转化完毕------------')