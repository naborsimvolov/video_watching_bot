from win32api import GetSystemMetrics
import cv2 as cv

class Vision:

    objects = ['Pictures/hideout.png', 'Pictures/refresh2.png']
    errors = ['Pictures/error75scale.png', 'Pictures/error80scale.png', 'Pictures/error90scale.png', 
    'Pictures/error_sweden.png']

    objects_offset = [(4,6), (0, 0), (5, 6,2)]
    method = cv.TM_CCOEFF_NORMED
    window = None
    object = None
    obj_error2 = None
    obj_error3 = None
    obj_error4 = None
    x_pr = int(round(GetSystemMetrics(0) / 100, 0))
    y_pr = int(round(GetSystemMetrics(1) / 100, 0))
    offset_x = 0
    offset_y = 0

    def __init__(self, window, object, method=cv.TM_CCOEFF_NORMED):
        self.window = window
        self.method = method
        #convert given object name to the picture
        if object == 'hideout':
            self.object = self.objects[0]
            self.offset_x  = self.objects_offset[0][0] * self.x_pr
            self.offset_y = self.objects_offset[0][1] * self.y_pr

        elif object == 'page_refresh':
            self.object = self.objects[1]
            self.offset_x  = self.objects_offset[2][0] * self.x_pr
            self.offset_y = self.objects_offset[2][1] * self.y_pr

        elif object == 'error':
            self.object = self.errors[0]
            self.obj_error2 = self.errors[1]
            self.obj_error3 = self.errors[2]
            self.obj_error4 = self.errors[3]

            self.offset_x = 0
            self.offset_y = 0

            self.obj_error2 = cv.imread(str(self.obj_error2), cv.IMREAD_UNCHANGED)
            self.obj_error3 = cv.imread(str(self.obj_error3), cv.IMREAD_UNCHANGED)
            self.obj_error4 = cv.imread(str(self.obj_error4), cv.IMREAD_UNCHANGED)

            self.obj_error2 = self.obj_error2[...,:3]
            self.obj_error3 = self.obj_error3[...,:3]
            self.obj_error4 = self.obj_error4[...,:3]

        else:
            print('no correct object given')

        #read picture we want to detect     and     drop alfa channel to avoid error in function matchTemplate
        self.object = cv.imread(str(self.object), cv.IMREAD_UNCHANGED)
        self.object = self.object[...,:3]

    def get_error_state(self):
        result0 = cv.matchTemplate(self.window, self.object, self.method)
        max_val0 = cv.minMaxLoc(result0)[1]
        result1 = cv.matchTemplate(self.window, self.obj_error2, self.method)
        max_val1 = cv.minMaxLoc(result1)[1]
        result2 = cv.matchTemplate(self.window, self.obj_error3, self.method)
        max_val2 = cv.minMaxLoc(result2)[1]
        result3 = cv.matchTemplate(self.window, self.obj_error4, self.method)
        max_val3 = cv.minMaxLoc(result3)[1]

        if max_val0 >= 0.9:
            return 'true'
        elif max_val1 >= 0.9:
            return 'true'
        elif max_val2 >= 0.9:
            return 'true'
        elif max_val3 >= 0.9:
            return 'true'
        else:
            return 'false'
        

    def get_object_pos(self):
        #find object ob the picture
        result = cv.matchTemplate(self.window, self.object, self.method)
        #find best match location
        max_loc = cv.minMaxLoc(result)[3]
        center_x = max_loc[0] + self.offset_x
        center_y = max_loc[1] + self.offset_y

        return center_x, center_y
