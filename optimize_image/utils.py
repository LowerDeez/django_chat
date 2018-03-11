import os
import imghdr
import logging
from subprocess import check_call
from uuid import uuid4
from PIL import Image
from django.conf import settings


class OptimizeImage(object):
    MAX_BIG_SIZE = (150, 150)
    MAX_SIZE = (50, 50)

    CONVERT_PATH = '/etc/alternatives/convert'

    CJPEG_PATH = '/opt/mozjpeg/bin/cjpeg'
    CJPEG_QUALITY = 80

    PNGQUANT_PATH = '/usr/bin/pngquant'
    PNGQUANT_QUALITY = 75 - 90

    def __init__(self, image_file, folder_name):
        self.image_file = image_file
        self.folder_name = folder_name
        self.image_size = self.MAX_SIZE
        self.image_big_size = self.MAX_BIG_SIZE

    def optimize_image(self):
        image_type = imghdr.what(self.image_file)
        original_name = str(self.image_file.name).split('/')[-1]
        uuid_folder = str(uuid4())
        new_folder = os.path.join(settings.MEDIA_ROOT + '/' + self.folder_name, uuid_folder)

        if not os.path.exists(new_folder):
            os.makedirs(new_folder)
        new_filename = os.path.join(new_folder, original_name)

        if image_type == 'jpeg':
            img = self.optimize_jpg(new_filename, self.image_size)
            img_big = self.optimize_jpg(new_filename, self.image_big_size)
        elif image_type == 'png':
            img = self.optimize_png(new_filename, self.image_size)
            img_big = self.optimize_png(new_filename, self.image_big_size)
        else:
            img = self.image_file
            img_big = self.image_file

        return {
            'image': img,
            'img_big': img_big,
            'name': self.folder_name + '/{}/{}'.format(uuid_folder, str(img.name.split('/')[-1])),
            'name_big': self.folder_name + '/{}/{}'.format(uuid_folder, str(img_big.name.split('/')[-1])),
            'url': 'media/{}/{}'.format(uuid_folder, str(img.name.split('/')[-1])),
            'url_big': 'media/{}/{}'.format(uuid_folder, str(img_big.name.split('/')[-1]))
        }

    def optimize_jpg(self, new_filename, image_size):
        img = Image.open(self.image_file)
        img.thumbnail(image_size, Image.ANTIALIAS)
        temp_filename = '{}{}'.format(new_filename, '.old.jpg')
        img.save(temp_filename)

        cjpeg_command = '{} "{}" pnm:- | {} -optimize -baseline -quality {} > "{}"'.format(self.CONVERT_PATH,
                                                                                           temp_filename,
                                                                                           self.CJPEG_PATH,
                                                                                           self.CJPEG_QUALITY,
                                                                                           new_filename)
        logging.debug(cjpeg_command)
        check_call(cjpeg_command, shell=True)

        os.remove(temp_filename)
        new_file_name = '{}/{}{}'.format(str('/'.join(new_filename.split('/')[:-1])),
                                         str(uuid4()), '.png')
        os.rename(new_filename, new_file_name)
        img = open(new_filename, "rb")

        return img

    def optimize_png(self, new_filename, image_size):
        img = Image.open(self.image_file)
        img.thumbnail(image_size, Image.ANTIALIAS)
        temp_filename = '{}{}'.format(new_filename, '.old.png')
        img.save(temp_filename)

        pngquant_command = '{} -f --quality={} -o"{}" "{}"'.format(self.PNGQUANT_PATH,
                                                                   self.PNGQUANT_QUALITY,
                                                                   new_filename,
                                                                   temp_filename)
        logging.debug(pngquant_command)
        check_call(pngquant_command, shell=True)

        os.remove(temp_filename)
        new_file_name = '{}/{}{}'.format(str('/'.join(new_filename.split('/')[:-1])),
                                         str(uuid4()), '.png')
        os.rename(new_filename, new_file_name)
        img = open(new_file_name, "rb")

        return img

    def optimize_size(self, nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']

        if nbytes == 0:
            return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])
