MIME_TYPE = {
    'gif' : "image/gif",
    'jpg' : "image/jpeg",
    'jpeg' : "image/jpeg",
    'png' : "image/png",
    'webp' : "image/webp",
    'svg' : "image/svg+xml",
    'xml' : "image/svg+xml",
    'tiff' : "image/tiff"
}

def get_folder_and_file_name(path):
    path_spilt_list = path.split('/')
    folder = "/"
    file_name = ""

    for i in range(len(path_spilt_list)):
        if i == (len(path_spilt_list) - 1):
            file_name = path_spilt_list[i]
        else:
            folder = folder + path_spilt_list[i] + "/"

    return folder, file_name