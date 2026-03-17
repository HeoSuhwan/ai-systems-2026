codex cli 설치과정

환경

os : windows
node.js version : 24.14.0
cli 도구 : Codex CLI

설치 과정에서 겪은 문제

1. powershell 보안 정책에 의해 npm 실행이 막혀서 'Set-ExecutionPolicy RemoteSigned' 명령어로 권한 부여함
2. api 탑제 과정에서 windows 환경에서는 set을 사용해야 하는데 export 명령어를 시도해서 오류 발생

실행 확인

설치후 powershell 창에서 codex를 호출 이후 openai 로그인하여 정상동작 되는것 확인

실행 결과

› Hello! 이 디렉토리에 간단한 Python hello world 파일을 만들어줘.
• 이 디렉토리에 간단한 Python hello world 파일을 만들겠습니다. 먼저 현재 폴더 상태를 확인한 뒤 바로 파일을 추가하겠습니
  다.

C:/Users/suhwan-l%USERPROFILE%/test-project 폴더에 python hello world 파일을 생성 요청하였더니 정상적으로 생성되었음





