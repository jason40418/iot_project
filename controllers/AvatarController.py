import os, PIL, simplejson, traceback
from PIL import Image
from flask import Blueprint, jsonify, request, render_template, redirect, url_for, send_from_directory
from werkzeug import secure_filename
from model.upload.upload_file import uploadfile
from model.util import General
from __main__ import app

# 定義
avatar_blueprint = Blueprint('avatar', __name__)

# 專案路徑
ROOT_DIR = app.root_path

# 上傳資料夾
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'model/face/dataset')
THUMBNAIL_FOLDER = os.path.join(ROOT_DIR, 'model/face', 'thumbnail')

# TODO: 後端判斷檔案大小是否過大
# 內容限制長度
MAX_CONTENT_LENGTH = 50 * 1024 * 1024

# 允許上傳格式型態（限定圖片檔案）
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
IGNORED_FILES = set(['.gitignore'])

# 檢查是否為允許的檔案格式
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 產生新的檔案名稱
def gen_file_name(filename, user_account):
    """
    If file was exist already, rename it and return a new name
    """

    i = 1
    while os.path.exists(os.path.join(UPLOAD_FOLDER, user_account, filename)):
        name, extension = os.path.splitext(filename)
        filename = '%s_%s%s' % (name, str(i), extension)
        i += 1

    return filename

# 建立影像縮圖
def create_thumbnail(image, user_account):
    try:
        base_width = 80
        img = Image.open(os.path.join(UPLOAD_FOLDER, user_account, image))
        w_percent = (base_width / float(img.size[0]))
        h_size = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((base_width, h_size), PIL.Image.ANTIALIAS)
        img.save(os.path.join(THUMBNAIL_FOLDER, user_account, image))

        return True

    except:
        print(traceback.format_exc())
        return False

@avatar_blueprint.route('/', methods=['GET', 'POST'])
@General.token_require_page("/member/login", 'page')
def index(payload):
   return render_template('app/member/upload.html')

@avatar_blueprint.route("/upload", methods=['GET', 'POST', 'HEAD'])
@General.token_require_page("/member/login")
def upload(payload):
    user_account = payload['account']
    if request.method == 'POST':
        files = request.files['files[]']

        if files:
            filename = secure_filename(files.filename)
            filename = gen_file_name(filename, user_account)
            mime_type = files.content_type

            print(filename, mime_type)
            print(allowed_file(files.filename))

            if not allowed_file(files.filename):
                result = uploadfile(name=filename, type=mime_type, size=0, not_allowed_msg="File type not allowed")

            else:
                # save file to disk
                uploaded_file_path = os.path.join(UPLOAD_FOLDER, user_account, filename)
                files.save(uploaded_file_path)

                # create thumbnail after saving
                if mime_type.startswith('image'):
                    create_thumbnail(filename, user_account)

                # get file size after saving
                size = os.path.getsize(uploaded_file_path)

                # return json for js call back
                result = uploadfile(name=filename, type=mime_type, size=size)

            return simplejson.dumps({"files": [result.get_file()]})

    if request.method == 'GET':
        # 取回該使用者的照片
        folder = os.path.join(UPLOAD_FOLDER, user_account)
        thumbnail_folder = os.path.join(THUMBNAIL_FOLDER, user_account)

        # 檢查該使用者之資料夾是否存在
        for path in [folder, thumbnail_folder]:
            if not os.path.isdir(path):
                try:
                    os.mkdir(path)
                except OSError:
                    print ("Creation of the directory %s failed" % path)
                else:
                    print ("Successfully created the directory %s " % path)

        files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f)) and f not in IGNORED_FILES ]

        file_display = []

        for f in files:
            size = os.path.getsize(os.path.join(folder, f))
            file_saved = uploadfile(name=f, size=size)
            file_display.append(file_saved.get_file())

        return simplejson.dumps({"files": file_display})

    if request.method == 'HEAD':
        return jsonify({
            'Request': 'HEAD'
        }), 200

    return redirect(url_for('/'))

# 刪除檔案
@avatar_blueprint.route("/delete/<string:filename>", methods=['DELETE'])
@General.token_require_page("/member/login")
def delete(payload, filename):
    user = payload['account']
    file_path = os.path.join(UPLOAD_FOLDER, user, filename)
    file_thumb_path = os.path.join(THUMBNAIL_FOLDER, user, filename)

    if os.path.exists(file_path):
        try:
            os.remove(file_path)

            if os.path.exists(file_thumb_path):
                os.remove(file_thumb_path)

            return simplejson.dumps({filename: 'True'})
        except:
            return simplejson.dumps({filename: 'False'})

# 處理靜態（static）文件路徑
@avatar_blueprint.route('/image/<path:path>', methods=['GET'])
@General.token_require_page("/member/login")
def face_static_file(payload, path):
    user = payload['account']
    # 去除掉避免cache的變數，取得完整靜態路徑
    path = path.split('?')[0]
    # 依照路徑（/）切割
    path_split = path.rsplit('/', 1)
    folder = path_split[0]
    file_name = path_split[1]

    static_path = os.path.join(ROOT_DIR, 'model/face', folder, user, file_name)
    folder, file_name = General.get_folder_and_file_name(static_path)
    ext = file_name.split('.')[-1]
    return send_from_directory(folder, file_name, mimetype=General.MIME_TYPE[ext.lower()], cache_timeout =-1)
