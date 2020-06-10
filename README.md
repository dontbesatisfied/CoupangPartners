파폭 및 파폭 드라이버 설치


# 네이버 블로그 사진 업로드
1. GET https://platform.editor.naver.com/api/blogpc001/v1/photo-uploader/session-key?userId=zxcvzxcv93
위 링크에서 sessionKey를 얻어냄
2. POST https://blog.upphoto.naver.com/{1에서 얻은 세션키}/simpleUpload/807273519?userId=zxcvzxcv93&extractExif=true&extractAnimatedCnt=true&autorotate=true&extractDominantColor=false&type=
위링크에서 폼데이터로 이미지 전송 후 이미지 주소 알아냄
3. POST https://blog.upphoto.naver.com/{1에서 얻은 세션키}/simpleUpload/807273519?userId=zxcvzxcv93&extractExif=true&extractAnimatedCnt=true&autorotate=true&extractDominantColor=false&type=
위링크로 blog_param.json 의 내용을 폼데이터로 전

문제는 1번을 실행할 SE-Authorization header값이 필요