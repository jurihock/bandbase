from app import app

import os
import glob
import subprocess

def safepath(value):

    dirname = os.path.dirname(value)

    return value if dirname else \
           os.path.join(app.config['TEMP'], value)

def compile(data, filename, read=True):

    data_path = safepath(filename)

    with open(data_path, 'w') as file:
        file.write(data)

    try:

        args = \
        [
            'latexmk',
            '-f',
            '-quiet',
            '-xelatex',
            data_path
        ]

        subprocess.check_output(args, cwd=app.config['TEMP'], stderr=subprocess.STDOUT)

        pdf_path = os.path.splitext(data_path)[0] + '.pdf'

        if not read:

            return (pdf_path, None)

        with open(pdf_path, 'rb') as file:

            pdf_data = file.read()

            return (pdf_path, pdf_data)

    except subprocess.CalledProcessError as e:

        raise ValueError('{0}\n$({1})'.format(
            str(e.output).strip(), ' '.join(args)))

def clone(src_filename, dst_filename, read=True):

    src_path = safepath(src_filename)
    dst_path = safepath(dst_filename)

    try:

        args = \
        [
            'pdftk',
            src_path,
            'cat',
            '1-end',
            '1-end',
            'output',
            dst_path
        ]

        subprocess.check_output(args, cwd=app.config['TEMP'], stderr=subprocess.STDOUT)

        if not read:

            return (dst_path, None)

        with open(dst_path, 'rb') as file:

            data = file.read()

            return (dst_path, data)

    except subprocess.CalledProcessError as e:

        raise ValueError('{0}\n$({1})'.format(
            str(e.output).strip(), ' '.join(args)))

def burst(src_filename, dst_filename):

    src_path = safepath(src_filename)
    dst_path = safepath(dst_filename)

    try:

        args = \
        [
            'pdftk',
            src_path,
            'burst',
            'output',
            dst_path
        ]

        subprocess.check_output(args, cwd=app.config['TEMP'], stderr=subprocess.STDOUT)

        return dst_path

    except subprocess.CalledProcessError as e:

        raise ValueError('{0}\n$({1})'.format(
            str(e.output).strip(), ' '.join(args)))

def jam(src_filename, dst_filename, read=True):

    src_path = safepath(src_filename)
    dst_path = safepath(dst_filename)

    try:

        burst_path = os.path.splitext(src_path)[0] + '.page_%03d.pdf'
        burst(src_path, burst_path)

        burst_path = os.path.splitext(src_path)[0] + '.page_*.pdf'
        burst_files = sorted(glob.glob(burst_path))

        args  = [ 'pdfjam' ]
        args += burst_files
        args += \
        [
            '--nup',
            '2x1',
            '--a4paper',
            '--landscape',
            '--outfile',
            dst_path
        ]

        subprocess.check_output(args, cwd=app.config['TEMP'], stderr=subprocess.STDOUT)

        if not read:

            return (dst_path, None)

        with open(dst_path, 'rb') as file:

            data = file.read()

            return (dst_path, data)

    except subprocess.CalledProcessError as e:

        raise ValueError('{0}\n$({1})'.format(
            str(e.output).strip(), ' '.join(args)))

    finally:

        burst_path = os.path.splitext(src_path)[0] + '.page_*.pdf'

        for file in glob.glob(burst_path):
            os.remove(file)

def merge(src_filenames, dst_filename, read=True):

    src_paths = [safepath(src_filename) for src_filename in src_filenames]
    dst_path = safepath(dst_filename)

    try:

        args  = [ 'pdftk' ]
        args += src_paths
        args += \
        [
            'cat',
            'output',
            dst_path
        ]

        subprocess.check_output(args, cwd=app.config['TEMP'], stderr=subprocess.STDOUT)

        if not read:

            return (dst_path, None)

        with open(dst_path, 'rb') as file:

            data = file.read()

            return (dst_path, data)

    except subprocess.CalledProcessError as e:

        raise ValueError('{0}\n$({1})'.format(
            str(e.output).strip(), ' '.join(args)))
