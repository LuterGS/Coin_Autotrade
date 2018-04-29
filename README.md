# Coinone_CryptoTrade
코인원 자동거래 시스템, python으로 만들고 linux에서 실행하는 것을 전제로 함.


crypto_autotrade_v0.4_2_coinone by LuterGS

가상화폐 자동거래 알고리즘 v0.4_2, 제작자 LuterGS

들어가기에 앞서
	- 해당 알고리즘은 코인원 API v2.0을 기반으로 합니다.
	- 해당 알고리즘은 아직 완전한 상태가 아니며, 문제가 발생할 가능성도 충분히 있습니다.
	- 해당 알고리즘은 파이썬을 이용해 개발되었습니다.
	- 해당 알고리즘은 리눅스로 동작하는 것을 전제로 하며, 작업한 환경은 CentOS 7입니다.
	
프로그램 세팅하기
	파이썬 확장 모듈을 설치해야 합니다. 쓰인 파이썬 모듈은 다음과 같으니, 모두 설치헤주세요.
		- time
		- datetime
		- os
		- sys
		- base64
		- json
		- hashlib
		- hmac
		- httplib2
		- urllib2
		- random
		- smtplib
		- MIMEMultipart
		- MIMEText
		- math
		
	현재 이 폴더를 로컬에다가 넣어주세요. 이 폴더 안에는 
		- buy_sell.py
		- coinone_API.py
		- file_writer.py
		- get_coin.py
		- mail_func.py
		- main.py
		- source_func.py
		- trade.sh
		- userdata.py
		- log (폴더)
		- log_old (폴더)
	
	log폴더 내에 money.txt 파일을 생성해주시고, 투자할 금액만 숫자로 적어주세요. 
		ex) money.txt를 열면, 120000 만 써져있어야 함
	프로그램의 변동성이나 수수료에 유의하여, 원금은 투자금의 103% ~ 106% 정도여야 이상적입니다. 

	userdata.py에 들어가서 사용자 정보를 작성해야 합니다. 입력한 정보는 모두 따옴표로 감싸져야 합니다.
		(ex. str = 'koo04034@gmail.com')
		6번째 줄 input your sender email address에는 메일이 전송될 때 보내는 사람의 주소를 입력해주세요. 각 사이트마다 보안 문제가 있을 수 있으므로, 가급적이면 getter와 겹치지 않게 설정하는 것을 추천합니다.
		10번째 줄 input your email address에는 메일을 받을 주소를 입력해주세요.
		14번째 줄 input your ACCESS TOKEN value에는 자신의 코인원 API v2.0의 ACCESS TOKEN 값을 입력해주세요.
		30번째 줄 input your SECRET KEY value에는 자신의 코인원 API v2.0의 SECRET KEY 값을 입력해주세요.
		
	이제 trade.sh만 실행하시면 됩니다. 해당 파일의 소유권을 chmod 755 명령어를 이용해 바꿔주세요 (chmod 755 trade.sh)
	이후 항시 실행을 위해 리눅스의 nohup을 사용할 것입니다.
	해당 폴더에 위치한 상태에서, 해당 명령어를 입력해주세요. 루트 권한 상태에서 실행하는 것을 추천합니다.
	nohup ./trade.sh > log/nohup.out 2> log/nohup.err < /dev/null &
	반드시 해당 명령어를 정확히 입력해야 하며, trade.sh 및 모든 파이썬 스크립트 파일이 존재하는 폴더에서 명령어를 입력해야 합니다.
	
	
프로그램 종료하기
	먼저, 리눅스 쉘에서 해당 명령어를 입력해주세요
	ps -ef | grep python
	이후 결과에서, 해당 줄을 찾아주세요
	root	숫자A	숫자B	0	19:26(시간)	?	00:00:01(시간)	python main.py
	이후, 해당 명령어를 입력하세요.
	kill 숫자A 숫자 B
	
	예시
		ps -ef | grep python 입력
		root	4312	4313	0	19:22	pts/0	00:00:01	python main.py
		이라는 줄을 찾음
		kill 4312 4313 입력
	
	
	
주의
	코인원 서버의 문제로, ticker나 orderbook을 가져오는 데 에러가 나서 프로그램이 종료되는 경우가 있습니다. 해당 문제를 방지하기 위해 trade.sh 파일을 이용해 무한반복을 했으므로, python 명령어로 main 단독실행은 테스트용으로만 해주시기 바랍니다.
	Email을 보내는 방식은 OS의 localhost가 있음을 전제하고 사용하였으므로, localhost가 없을 경우는 mail_func.py를 직접 수정해주시기 바랍니다.
	
알고리즘 동작 방법
	먼저 (1번)시세 측정 - 15분 휴식 - (2번)시세 측정 - 5분 휴식 - (3번)시세 측정의 방식을 거칩니다.
	1~2번 시세 측정 사이에 0.2% 이상 가치가 하락한 코인을 고릅니다.
	2~3번 시세 측정 사이에 가치가 상승한 코인을 고릅니다.
	두 경우를 모두 만족하는 코인을 선별하고, 랜덤으로 한 코인을 선택해 투자합니다. 만약, 모든 코인이 조건에 맞지 않을 경우, 해당 과정을 반복합니다.
	이후 해당 코인을 투자값만큼 매수합니다. 매수가는 매수 최고가입니다.
	
	이후 해당 코인의 한화 값이 투자값의 100.45%가 되었을 때는 5분마다 시세를 측정해, 가치가 오르거나 조금 하락하면 그대로, 가치가 0.1% 이상 하락하면 매도합니다. 매도가는 빠른 거래를 위해 매수 최고가로 설정했습니다.
	만약, 해당 코인의 한화 값이 투자값의 70%가 되었을 때는 긴급 판단을 요하는 메일을 보내고 프로그램을 종료합니다.
	만약, 매수 후 두시간이 경과함에도 가치가 100.45%에 도달하지 못했을 때는, 해당 코인의 한화 값이 투자값의 99.5% 이상일 때 매도합니다. 매도가는 빠른 거래를 위해 매수 최고가로 설정했습니다.
	만약, 매수 후 18시간이 경과함에도 가치가 99.5%에 도달하지 못했을 때는, 해당 코인의 한화 값이 투자값의 98.5%이상일 때 매도합니다. 매도가는 빠른 거래를 위해 매수 최고가로 설정했습니다.
	
	이 작업을 반복해 투자금의 6% 이상 이익을 보면, 메일을 보냅니다. 해당 메일에는 로그가 첨부됩니다. 이후, 투자금에 번 돈의 75%를 더해 재설정한 후, 현재까지의 과정을 반복합니다. 이 과정을 반복할 때마다 log_old 폴더에 해당 버전을 기록한 로그가 폴더로 저장되며, 새로운 로그가 다시 씌워집니다.
	
		

	
