import yaml


def load_todo():
    # Путь к файлу todo.yml
    todo_path = '../materials/todo.yml'

    # Загружаем данные из файла
    with open(todo_path, 'r') as file:
        return yaml.load(file, yaml.FullLoader)


def generate_installation_task(package):
    # Генерирует задачу для установки пакета
    return {
        'name': 'Installation modules',
        'ansible.builtin.apt': {
            'name': package
        },
    }


def generate_copy_files_task(src, dest):
    # Генерирует задачу для копирования файлов
    return {
        'name': 'Copying files',
        'ansible.builtin.copy': {
            'src': src,
            'dest': dest,
        },
    }


def generate_run_files_task(cmd):
    # Генерирует задачу для запуска файлов
    return {
        'name': 'Run files',
        'ansible.builtin.shell': {
            'cmd': cmd,
        },
    }


def generate_playbook():
    # Загружаем данные из todo.yml
    todo = load_todo()

    # Генерируем задачи для установки пакетов
    install_tasks = [generate_installation_task(
        package) for package in todo['server']['install_packages']]

    # Генерируем задачи для копирования файлов
    copy_tasks = [generate_copy_files_task(
        'exploit.py', 'exploit.py'), generate_copy_files_task('consumer.py', 'consumer.py')]

    # Генерируем задачи для запуска файлов
    run_tasks = [generate_run_files_task('python exploit.py'), generate_run_files_task(
        f'python consumer.py -e {",".join(todo["bad_guys"])}')]

    # Собираем все задачи в один плейбук
    tasks = install_tasks + copy_tasks + run_tasks
    playbook = [{
        'name': 'Playbook',
        'hosts': 'localhost',
        'become': 'yes',
        'tasks': tasks,
    }]

    return playbook


def save_to_file(playbook, filename='deploy.yml'):
    # Сохраняем плейбук в файл
    with open(filename, 'w') as file:
        yaml.dump(playbook, file, sort_keys=False, default_flow_style=False)


if __name__ == "__main__":
    # Генерируем плейбук и сохраняем его в файл
    playbook = generate_playbook()
    save_to_file(playbook)
