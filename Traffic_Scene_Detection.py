import cv2
import time
import xlsxwriter
import tensorflow as tf
from utils import Frame
from yolov3_tf2.models import YoloV3
from yolov3_tf2.dataset import transform_images
from absl import logging

class VideoProcessing():
	def __init__(self):
		self.flags = {}
		self.flags['classes'] = './yolov3_tf2/yolo_v3_model/data/coco.names'
		self.flags['weights'] = './yolov3_tf2/yolo_v3_model/checkpoints/yolov3.tf'
		self.flags['tiny'] = False
		self.flags['size'] = 416
		self.flags['video'] = 'Image&Video/LargeIntersection.mp4'
		self.flags['output'] = 'Image&Video/0826.avi'
		self.flags['output_format'] = 'XVID'
		self.flags['num_classes'] = 80

		# 功能选项
		self.Traffic_Light_Recognition = True
		self.Estimate_Speed = True
		self.License_Plate_Recognition = False


		# 将识别结果保存在Excel中
		self.workbook = xlsxwriter.Workbook('Recognize_Result.xlsx')  # 建立文件
		self.worksheet = self.workbook.add_worksheet()  # 建立sheet


	def Create_Excel(self):
		self.worksheet.write('A1', '帧数')  # 向A1写入-
		self.worksheet.write('C1', '实时路人数目')
		self.worksheet.write('E1', '实时汽车数目')
		self.worksheet.write('G1', '实时摩托车数目')
		self.worksheet.write('I1', '路段车流量统计')

		if self.License_Plate_Recognition:
			self.worksheet.write('M1', '车牌检测结果')

	def Run(self):
		physical_devices = tf.config.experimental.list_physical_devices('GPU')
		if len(physical_devices) > 0:
			tf.config.experimental.set_memory_growth(physical_devices[0], True)

		yolo = YoloV3(classes=self.flags['num_classes'])

		yolo.load_weights(self.flags['weights'])
		logging.info('weights loaded')

		class_names = [c.strip() for c in open(self.flags['classes']).readlines()]
		logging.info('classes loaded')


		try:
			vid = cv2.VideoCapture(int(self.flags['video']))
		except:
			vid = cv2.VideoCapture(self.flags['video'])

		out = None

		frame = 0
		num_frame = 0
		traffic_sta = 0
		writer = None
		self.Create_Excel()
		begin_time = time.time()
		while True:
			_, img = vid.read()

			if img is None:
				break

			# 预处理
			(h, w) = img.shape[:2]
			width = 1400
			r = width / float(w)
			dim = (width, int(h * r))
			img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

			img_in = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			img_in = tf.expand_dims(img_in, 0)
			img_in = transform_images(img_in, self.flags['size'])

			# 判断结果是否需要保存
			if self.flags["output"] is not None and writer is None:
				fourcc = cv2.VideoWriter_fourcc(*"MJPG")
				writer = cv2.VideoWriter(self.flags["output"], fourcc, 30,
				                         (img.shape[1], img.shape[0]), True)

			# 使用YOLOv3进行目标检测
			boxes, scores, classes, nums = yolo.predict(img_in)

			# 创建Frame对象 便于处理当前帧
			if num_frame%10 == 0:
				frame = Frame(img, (boxes, scores, classes, nums), class_names, num_frame,
				              [], [], [], traffic_sta, [], 30, self.License_Plate_Recognition, self.Traffic_Light_Recognition,
				              self.Estimate_Speed)
			else:
				trackers, labels, confidence, license_plate = frame.Get_Track_Obj()
				frame = Frame(img, (boxes, scores, classes, nums), class_names, num_frame,
				              trackers, labels, confidence, traffic_sta, license_plate, 30, self.License_Plate_Recognition,
				              self.Traffic_Light_Recognition, self.Estimate_Speed)


			traffic_sta = frame.Get_Traffic_Sta() # 获取车流量统计值
			img = frame.Draw_Outputs() # 标注识别框和标签
			count_obj = frame.Count_Obj() # 统计当前帧画面中的检测目标个数
			img = frame.Draw_Obj(img, count_obj) # 标注当前帧检测结果
			frame.Write_Excel(self.worksheet, count_obj) # 将标注结果写入Excel文件


			num_frame += 1
			if writer is not None: # 也可以保存结果
				writer.write(img)
			cv2.imshow('output', img) # 显示当前帧处理结果
			if cv2.waitKey(1) == ord('q'): # 按q键退出
				break

		end_time = time.time()
		run_time = end_time - begin_time
		print("处理时间：{}".format(run_time))

		self.workbook.close()
		if writer is not None:
			writer.release()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	Video = VideoProcessing()
	Video.Run()
