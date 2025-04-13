pipeline {
    agent any

    stages {
        stage('Остановка сервера') {
            steps {
                sshagent(['ed_8']) {
                    sh '''
                        ssh ed_8@207.182.151.252 '
                            echo "Процессы перед завершением:"
                            pgrep -af 4inRserver_test
                            pkill -f 4inRserver_test || true
                            echo "Процессы после завершения:"
                            pgrep -af 4inRserver_test
                            pkill -f 4inRserver_test || true
                        '
                    '''
                }
            }
        }

        stage('Копирование кода') {
            steps {
                sshagent(['ed_8']) {
                    sh '''
                        scp /var/jenkins/workspace/4in1_ppl/4inRserver.py ed_8@207.182.151.252:/home/ed_8/4inR/test/4inRserver_test.py
                        scp /var/jenkins/workspace/4in1_ppl/4inR.py ed_8@207.182.151.252:/var/www/4in1/4inR_test.py
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
   
                            sed -i "s/65432/65434/g" /var/www/4in1/4inR_test.py
                            sed -i "s/65432/65434/g" /home/ed_8/4inR/test/4inRserver_test.py
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
                    nohup /usr/bin/python3 /home/ed_8/4inR/test/4inRserver_test.py &
                    '
                '''
                }
            }
        }
    }
}
