# Kubernetes / K8S
...

# Helm
...

## Установить нужные утилиты

### 1. Установить helm

### 2. Установить helmfile

### 3. Установить плагины


#### HELM
    helm plugin install https://github.com/aslafy-z/helm-git --version 0.11.2
    export HELM_DIFF_COLOR=true
    helm plugin install https://github.com/databus23/helm-diff --version v3.5.0
    helm plugin install https://github.com/jkroepke/helm-secrets --version v3.14.0

### 4 Установить sops
https://github.com/mozilla/sops/releases

### 5 импортировать приватный ключ из gitlab сi из раздела variables

поместить взятый из переменных окружения приватный ключ в файл private
gpg --import < privateИспользование helmfile


#### 5.1 Перейти в папку проекта, затем в папку helm в консоли

#### 5.2 Положить здесь файл .env с таким содержимым:
    ------------- .env (экспортируются обязательные для запуска helm переменные, можно найти по слову required - они должны быть в файле .env)
    # Reset all _VARIABLES
    for v in $(printenv | awk -F= '/^(HELMFILE|CHART|CI|HELM|DOCKER_IMAGE)_/{print $1}'); do
      unset "$v"
    done
    export HELMFILE_GOCCY_GOYAML=true
    export HELMFILE_TIMEOUT=120
    export HELM_DIFF_COLOR=true
    export CI_ENVIRONMENT_URL=https://localhost
    export DOCKER_IMAGE_TAG=1.1.1
    -------------

#### 5.3 Файл .env комитить не нунжо

#### 5.4 Подгружаем файл .env в текущей сессии в консоли
. ./.env

#### 5.5 запускаем сборку шаблона

reviews - это название окружения, есть такая папка в папке helm
backend - это название релиза
helmfile template -e reviews
можно так
helmfile template -e reviews -lname=backend
если видим в консоли что то про bitnami и команда зависла, то control +c и по новой

