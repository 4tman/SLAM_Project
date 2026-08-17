# SLAM Project

ROS 2 проект для построения и визуализации карты окружения с использованием SLAM.

## Возможности

- Построение occupancy grid map в ROS 2
- Сохранение карты в формате `.pgm` и `.yaml`
- Использование описания робота из пакета `robot_description`
- Подготовка к интеграции навигации и автономного движения

## Структура проекта

```text
SLAM_PROJECT/
├── src/
│   └── robot_description/   # URDF/Xacro, launch-файлы, meshes и конфигурация робота
├── my_map.pgm               # Изображение сохранённой occupancy grid map
├── my_map.yaml              # Метаданные карты
├── .gitignore
└── README.md
```

> Каталоги `build/`, `install/` и `log/` создаются автоматически командой `colcon build` и не хранятся в Git.

## Требования

- Ubuntu 22.04
- ROS 2 Humble
- `colcon`
- [Укажи используемый SLAM-пакет: slam_toolbox / Cartographer / другой]
- [Укажи используемый лидар или источник данных]

## Сборка

Перейдите в корень workspace:

```bash
cd ~/SLAM_PROJECT
```

Соберите пакеты:

```bash
colcon build --symlink-install
```

Подключите окружение workspace:

```bash
source install/setup.bash
```

## Запуск

[Напиши здесь точную команду, которой ты запускаешь проект.]

Пример:

```bash
ros2 launch robot_description [имя_launch_файла].launch.py
```

## Карта

В репозитории приведена примерная сохранённая карта:

- `my_map.pgm` — изображение occupancy grid map
- `my_map.yaml` — параметры карты: разрешение, origin, пороговые значения и ссылка на `.pgm`

Для использования карты в Nav2:

```bash
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=my_map.yaml
```

## Статус

Проект находится в разработке.

- [x] Создан ROS 2 workspace
- [x] Добавлено описание робота
- [x] Сохранена тестовая SLAM-карта
- [ ] Подключён и проверен источник данных лидара
- [ ] Настроен SLAM-узел
- [ ] Настроена Nav2-навигация
- [ ] Добавлена документация по запуску

## Автор

4t

## Лицензия

[Выбери лицензию позже: MIT, Apache-2.0, GPL-3.0 или укажи, что проект пока без лицензии.]

#потом доделаю