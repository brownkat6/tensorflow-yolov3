#! /usr/bin/env python
# coding=utf-8
#================================================================
#   Copyright (C) 2019 * Ltd. All rights reserved.
#
#   Editor      : VIM
#   File name   : freeze_graph.py
#   Author      : YunYang1994
#   Created date: 2019-03-20 15:57:33
#   Description :
#
#================================================================


import tensorflow as tf
from core.yolov3 import YOLOV3
import os

ROOT_DIR = "/content/tensorflow-yolov3"

ckpt_model_name = "yolov3_ball_goal.pb"#"/yolov3_45_epochs.pb"#"/yolov3_coco.pb"

latest_checkpoint_path = "/content/gdrive/My Drive/Robotics/yolov3/checkpoint/yolov3_test_loss=nan.ckpt-30"#yolov3_test_loss=8.7657.ckpt-45"

#pb_file = ROOT_DIR + ckpt_model_name
pb_file = "/content/gdrive/My Drive/Robotics/yolov3/checkpoint/" + ckpt_model_name
ckpt_file = latest_checkpoint_path
#ckpt_file = ROOT_DIR + "/checkpoint/yolov3_coco_demo.ckpt"
output_node_names = ["input/input_data", "pred_sbbox/concat_2", "pred_mbbox/concat_2", "pred_lbbox/concat_2"]

with tf.name_scope('input'):
    input_data = tf.placeholder(dtype=tf.float32, name='input_data')

model = YOLOV3(input_data, trainable=False)
print(model.conv_sbbox, model.conv_mbbox, model.conv_lbbox)

sess  = tf.Session(config=tf.ConfigProto(allow_soft_placement=True))
saver = tf.train.Saver()
print(str(len(list(os.listdir("/content/gdrive/My Drive/Robotics/yolov3/checkpoint/")))) + " files  in checkpoint directory")
saver.restore(sess, ckpt_file)

converted_graph_def = tf.graph_util.convert_variables_to_constants(sess,
                            input_graph_def  = sess.graph.as_graph_def(),
                            output_node_names = output_node_names)

with tf.gfile.GFile(pb_file, "wb") as f:
    f.write(converted_graph_def.SerializeToString())




