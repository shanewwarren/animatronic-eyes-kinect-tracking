import cv

class Classifier:
    def __init__(self, filename, classifier_type, minimum_detection_scale,
                 scale_increase_rate = 1.4, minimum_neighbor_threshold=4,
                 flags=0):
        # store the parameters used for the haar detection
        self.classifier = cv.Load(filename)
        self.minimum_detection_scale = minimum_detection_scale 
        self.scale_increase_rate = scale_increase_rate 
        self.minimum_neighbor_threshold = minimum_neighbor_threshold
        self.classifier_type = classifier_type
        self.flags = flags


    def detect(self, image):
        storage = cv.CreateMemStorage(0)
        objects_detected = cv.HaarDetectObjects(image, self.classifier,
                                                storage, self.scale_increase_rate,
                                                self.minimum_neighbor_threshold,
                                                self.flags, self.minimum_detection_scale)
        detected = len(objects_detected)
        if detected == 0:
            return None 
    
        total_x = 0
        total_y = 0    
    
        for (x,y,w,h),n in objects_detected:
            total_x = total_x + x 
            total_y = total_y + y 

        average = [total_x/float(detected), total_y/float(detected)]
        return average[0] + 50, average[1] + 50 
       
