pipeline {
    agent any

    stages {

        stage('Копирование кода') {
            steps {
                sshagent(['ed_8']) {
                    sh '''
                        scp /var/jenkins_home/workspace/4in1_ppl/4inRserver.py ed_8@207.182.151.252:/home/ed_8/4inR/test/4inRserver_test.py
                        scp /var/jenkins_home/workspace/4in1_ppl/stoper.sh ed_8@207.182.151.252:/home/ed_8/4inR/test/stoper.sh
                        scp /var/jenkins_home/workspace/4in1_ppl/4inR.py ed_8@207.182.151.252:/var/www/4in1/4inR_test.py
                '''
                }
            }
        }

        stage('киляем процесс') {
            steps {
                sshagent(['ed_8']) {
                    sh '''
                        ssh ed_8@207.182.151.252 '
                            /bin/sh /home/ed_8/4inR/test/stoper.sh
                        '
                    '''
                }
            }
        }

        stage('модификация файлов') {
            steps {
                sshagent(['ed_8']) {
                    sh '''
                        ssh ed_8@207.182.151.252 '
                            sed -i "s/127.0.0.1/207.182.151.252/g" /var/www/4in1/4inR_test.py
                            sed -i "s/127.0.0.1/207.182.151.252/g" /home/ed_8/4inR/test/4inRserver_test.py
   
                            sed -i "s/65434/65435/g" /var/www/4in1/4inR_test.py
                            sed -i "s/65434/65435/g" /home/ed_8/4inR/test/4inRserver_test.py
                        '
                    '''
                }
            }
        }

        stage('Запуск сервера') {
            steps {
                sshagent(['ed_8']) {
                    sh '''
                        ssh ed_8@207.182.151.252 '
                    BUILD_ID=dontKillMe nohup /usr/bin/python3 /home/ed_8/4inR/test/4inRserver_test.py > /dev/null 2>&1 &
                    '
                '''
                }
            }
        }
    }
}
