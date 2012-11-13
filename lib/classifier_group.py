from classifier import Classifier

class ClassifierGroup:
    
    def __init__(self, group_name):
        self.classifiers = []   
        self.group_name = group_name
        pass
    
    def add_classifier(self, classifier):
        self.classifiers.append(classifier)     

    # detect:  given an image iterates through each of the groups
    #          classifiers to identify objects.  
    #
    def detect(self, image):
        detected = [] # array of all the different objects detected
        for classifier in self.classifiers:
            detected_object_point = classifier.detect(image)
            if detected_object_point is not None:
                detected.append(detected_object_point)
        
        # did we detect anything     
        if len(detected) == 0:
            print self.group_name, " detected no objects."
            return None 
           
        #total_x = 0
        #total_y = 0
        #for point in detected:
        #    total_x = total_x + point[0]
        #    total_y = total_y + point[1]     

        #average_detected_object_point = [total_x/float(len(detected)),
        #                                 total_y/float(len(detected))]

        #print self.group_name, average_detected_object_point 
        print detected
        return detected[0][0], detected[0][1] 
