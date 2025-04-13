pipeline {
    agent any

    stages {
        stage('Получение кода') {
            steps {
                sh '''
                    cd /home/ed_8/9_4inrow
                    git pull https://github.com/mntcalm/9_4inrow.git
                    git checkout test
                '''
            }
        }

        stage('Остановка сервера') {
            steps {
                sh '''
                    ps ax | grep 4inRserver_test | grep -v grep | awk '{print $1}' | xargs kill || true
                '''
            }
        }

        stage('Копирование и модификация файлов') {
            steps {
                sh '''
                    cp /home/ed_8/9_4inrow/4inRserver.py /home/ed_8/4inR/test/4inRserver_test.py
                    cp /home/ed_8/9_4inrow/4inR.py /var/www/4in1/4inR_test.py

                    sed -i "s/127.0.0.1/207.182.151.252/g" /var/www/4in1/4inR_test.py
                    sed -i "s/127.0.0.1/207.182.151.252/g" /home/ed_8/4inR/test/4inRserver_test.py

                    sed -i "s/65432/65434/g" /var/www/4in1/4inR_test.py
                    sed -i "s/65432/65434/g" /home/ed_8/4inR/test/4inRserver_test.py
                '''
            }
        }

        stage('Запуск сервера') {
            steps {
                sh '''
                    nohup /usr/bin/python3 /home/ed_8/4inR/test/4inRserver_test.py &
                '''
            }
        }
    }
}
