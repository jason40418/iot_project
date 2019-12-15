import os
import time

class uploadfile():
    def __init__(self, name, type=None, size=None, not_allowed_msg=''):
        # 增加隨機碼避免瀏覽器快取造成圖片無法正確存取
        self.random = time.time()
        self.name = name
        self.type = type
        self.size = size
        self.not_allowed_msg = not_allowed_msg
        self.url = "/member/avatar/image/dataset/%s" % name
        self.thumbnail_url = "/member/avatar/image/thumbnail/%s?randon=%s" % (name, self.random)
        self.delete_url = "/member/avatar/delete/%s?randon=%s" % (name, self.random)
        self.delete_type = "DELETE"


    def is_image(self):
        fileName, fileExtension = os.path.splitext(self.name.lower())

        if fileExtension in ['.jpg', '.png', '.jpeg', '.bmp']:
            return True

        return False

    def get_file(self):
        if self.type != None:
            # POST an image
            if self.type.startswith('image') and self.not_allowed_msg == '':
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        "url": self.url,
                        "thumbnailUrl": self.thumbnail_url,
                        "deleteUrl": self.delete_url,
                        "deleteType": self.delete_type,}

            # POST an normal file
            elif self.not_allowed_msg == '':
                return {"name": self.name,
                        "type": self.type,
                        "size": self.size,
                        "url": self.url,
                        "deleteUrl": self.delete_url,
                        "deleteType": self.delete_type,}

            # File type is not allowed
            else:
                return {"error": self.not_allowed_msg,
                        "name": self.name,
                        "type": self.type,
                        "size": self.size,}

        # GET image from disk
        elif self.is_image():
            return {"name": self.name,
                    "size": self.size,
                    "url": self.url,
                    "thumbnailUrl": self.thumbnail_url,
                    "deleteUrl": self.delete_url,
                    "deleteType": self.delete_type,}

        # GET normal file from disk
        else:
            return {"name": self.name,
                    "size": self.size,
                    "url": self.url,
                    "deleteUrl": self.delete_url,
                    "deleteType": self.delete_type,}
