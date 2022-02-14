from cProfile import label
import re
import sys
import cv2
import time
import threading
import signal
import platform
import os



from matplotlib import image
import numpy as np
from tflite_support import metadata

import json
import settings
# pylint: disable=g-import-not-at-top
#try:
  # Import TFLite interpreter from tflite_runtime package if it's available.
from tflite_runtime.interpreter import Interpreter
from tflite_runtime.interpreter import load_delegate
#except ImportError:
# If not, fallback to use the TFLite interpreter from the full TF package.
#  import tensorflow as tf
#  Interpreter = tf.lite.Interpreter
#  load_delegate = tf.lite.experimental.load_delegate

done = False

class Detector():
    def __init__(self) -> None:
        
        #threading.Thread.__init__(self)
        self.imcnt,self.fps = 0.0,0.0
        self.start = time.time()
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS, 60)
        self.cap.set(cv2.CAP_PROP_CONTRAST, 50)
        self.model_path = 'example_files/efficientdet_lite0.tflite'
        self.tnum = 3
        self.core = Core(self.tnum)
        #super().__init__(group=None,target=self.run(),name=None, daemon=True)
    def cap_read(self):
        if self.cap.isOpened():
            success,img = self.cap.read()
            if not success:
                sys.exit("ERROR: cap error.")
            self.imcnt += 1
            img = cv2.flip(img,-1)
            self.core.detect(img)
            print(self.fps,settings.detections)
            if self.imcnt % 10 == 0:
                self.fps = 10/(self.start-time.time())
                self.start = time.time()
            return img
    def cap_destroy(self):
        self.cap.release()
        cv2.destroyAllWindows()
    def routine(self):
        while self.cap.isOpened() and done == False:
            self.cap_read()
        self.cap_destroy()

class Core():
    def __init__(self,tnum):
        self.mpath = 'example_files/efficientdet_lite0.tflite'
        d = metadata.MetadataDisplayer.with_model_file(self.mpath)
        model = json.loads(d.get_metadata_json())
        pu = model['subgraph_metadata'][0]['input_tensor_metadata'][0]['process_units']
        mean = 127.5
        std = 127.5
        for o in pu:
            if o['options_type'] == 'NormalizeOptions':
                mean = o['options']['mean'][0]
                std = o['options']['std'][0]
        self.mean = mean
        self.std = std
        self.score_threshold = .8
        file_name = d.get_packed_associated_file_list()[0]
        label_map = d.get_associated_file_buffer(file_name).decode()
        self.lablist = list(filter(len,label_map.splitlines()))
        interpreter = Interpreter(model_path=self.mpath, num_threads=tnum)
        interpreter.allocate_tensors()
        input_detail = interpreter.get_input_details()[0]
        sorted_ids = sorted([output['index'] for output in interpreter.get_output_details()])
        self.out_ids = {'location':sorted_ids[0], 'category':sorted_ids[1],'score':sorted_ids[2],'number of detections':sorted_ids[3]}
        self.in_size = input_detail['shape'][2], input_detail['shape'][1]
        self.quant_in = input_detail['dtype'] == np.uint8
        self.interpreter = interpreter
    def detect(self,img:np.ndarray):
        height,width, _ = img.shape
        in_tens = self.preprocess(img)
        self.set_in_tens(in_tens)
        self.interpreter.invoke()
        boxes = self.get_output_tensor('location')
        classes = self.get_output_tensor('category')
        scores = self.get_output_tensor('score')
        count = int(self.get_output_tensor('number of detections'))
        return self.postprocess(boxes,classes,scores,count,width,height)

    def preprocess(self,img:np.ndarray):
        in_tens = cv2.resize(img,self.in_size)
        if not self.quant_in:
            in_tens = (np.float32(in_tens)-self.mean) / self.std
        in_tens = np.expand_dims(in_tens,axis=0)
        return in_tens
    def set_in_tens(self, image):
        ten_idx = self.interpreter.get_input_details()[0]['index']
        in_tens = self.interpreter.tensor(tensor_index=ten_idx)()[0]
        in_tens[:,:] = image
    def get_output_tensor(self,name):
        out_idx = self.out_ids[name]
        tensor = np.squeeze(self.interpreter.get_tensor(out_idx))
        return tensor
    def postprocess(self,boxes,classes,scores,count,width,height):
        results = []

        for i in range(count):
            if scores[i] >= self.score_threshold:
                y1,x1,y2,x2 = boxes[i]
                category = self.lablist[int(classes[i])]
                if category in settings.CATEGORY_LIST:
                    results.append([[category],scores[i],{'x1':x1,'y1':y1,'x2':x2,'y2':y2}])
                
        results = sorted(results, key=lambda d:d[1],reverse=True)
        
        result_count = min(len(results), 3)
        settings.detections = results[:result_count]

#t1 = Detector()


def signal_handler(sig,frame):
    #pass
    #print('joining...')
    #done = True
    #t1.join()
    os._exit()
def test1():
    t1 = Detector()
    #print(t1.is_alive())
    #print(t1)
    t1.routine()
    pass


if __name__ == '__main__':
    #signal.signal(signal.SIGINT, signal_handler)
    test1()
    pass