from flask import Flask, request, render_template, redirect, url_for
import boto3
import requests

app = Flask(__name__)

# S3 연결 설정
# s3 = boto3.client(
#     's3',
#     aws_access_key_id='YOUR_ACCESS_KEY',
#     aws_secret_access_key='YOUR_SECRET_KEY',
#     region_name='YOUR_REGION'
# )
# bucket_name = 'YOUR_BUCKET_NAME'  # S3 버킷 이름

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # 파일 업로드
        if 'file' not in request.files:
            return render_template("upload.html", error="No file selected.")
        
        file = request.files['file']
        if file.filename == '':
            return render_template("upload.html", error="No selected file.")
        
        # S3에 업로드
        s3_key = f"670\\{file.filename}"
        # s3.upload_fileobj(file, bucket_name, s3_key)
        
        # 이미지 변환 서버에 알림
        conversion_server_url = 'http://localhost:5000/convert-dicom'
        data = { "s3_key": s3_key}
        response = requests.post(conversion_server_url, json=data)
        
        if response.status_code == 200:
            return redirect(url_for('upload_file', success="File uploaded and processed successfully."))
        else:
            return render_template("upload.html", error="Failed to notify conversion server.")
    
    return render_template("upload.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
