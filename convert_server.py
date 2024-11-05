import os
from flask import Flask, request, jsonify
from pydicom import dcmread
import pydicom
from PIL import Image
import numpy as np
import png

app = Flask(__name__)

@app.route('/convert-dicom', methods=['POST'])
def convert_dicom():
    data = request.json
    s3_key = data.get('s3_key')
    
    if not s3_key:
        return jsonify({"error": "Key missing"}), 400

    # 로컬 경로에서 DICOM 파일 찾기
    local_dicom_path = os.path.join("C:\\", "Users", "heomin", "Desktop", "3-2", "캡스톤", "DicomToPng_server", "dicom", f"{s3_key}")
    try:
        dicom = dcmread(local_dicom_path)

    except FileNotFoundError:
        return jsonify({"error": "DICOM file not found in local directory"}), 404

    # DICOM을 PNG로 변환
    png_path = f"converted_images/{s3_key.split('/')[-1].split('.')[0]}.png"  # 저장할 파일 경로
    mri_to_png(local_dicom_path, png_path)
    return jsonify({"message": "Image converted and saved successfully", "file_path": png_path}), 200


def mri_to_png(mri_file, png_file):
    """ DICOM 이미지를 PNG로 변환 """
    ds = pydicom.dcmread(mri_file)
    # DICOM 데이터 중 픽셀 데이터를 읽어오는 부분. DICOM 픽셀 데이터는 보통 12비트로 표현된다.
    dcm_arr = ds.pixel_array


    image_2d = []
    max_val = 0
    for row in plan.pixel_array:
        pixels = []
        for col in row:
            pixels.append(col)
            if col > max_val: max_val = col
        image_2d.append(pixels)
    
    # Rescaling grey scale between 0-255
    image_2d_scaled = []
    for row in image_2d:
        row_scaled = []
        for col in row:
            col_scaled = int((float(col) / float(max_val)) * 255.0)
            row_scaled.append(col_scaled)
        image_2d_scaled.append(row_scaled)
    
    # Writing the PNG file
    w = png.Writer(shape[0], shape[1], greyscale=True)
    w.write(png_file, image_2d_scaled)


if __name__ == '__main__':
    # Flask 서버를 실행
    app.run(debug=True)
