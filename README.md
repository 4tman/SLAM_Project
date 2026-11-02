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
- SLAM-пакет: slam_toolbox

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


1 Окно(запуск симуляционной среды Gazebo):

```bash
gz sim src/robot_description/urdf/robot.urdf
```

2 Окно(запуск 3д визуализации в Rviz2):
```bash
ros2 launch robot_description two_wheel_launch.launch.py 
```

3 Окно(запуск конфиг файлов мостов gz-ros2(скорость время лидар))
```bash
ros2 run ros_gz_bridge parameter_bridge \
  --ros-args \
  -p config_file:=$HOME/slam_project/src/robot_description/config/gz_bridge.yaml
```

4 Окно(запуск tf2)
```
ros2 run robot_description tf2_trans
```

5 Окно (slam toolbox)
```bash
 ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true
```

!необходимо в рвизе добавить фрейм map (из вкладки by topic)

## Карта

В репозитории приведена примерная сохранённая карта:

- `my_map.pgm` — изображение occupancy grid map
- `my_map.yaml` — параметры карты: разрешение, origin, пороговые значения и ссылка на `.pgm`

для сохранения собственной карты
```bash
 ros2 run nav2_map_server map_saver_cli \
  -f "$HOME/slam_project/2map"
```

Для использования карты в Nav2:

```bash
ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=my_map.yaml
```

## Статус

Проект находится в разработке.

- [x] Создан ROS 2 workspace
- [x] Добавлено описание робота
- [x] Сохранена тестовая SLAM-карта
- [x] Настроен рабочий SLAM узел 
- [x] Подключён и проверен источник данных лидара
- [x] Последовательно структурированы необходимые для работы ноды
- [x] Разработан конфиг файл для запуска всех мостов
- [ ] Все ноды упакованы в единый лаунч файл
- [ ] написан единый лаунч для запуска "1 кнопкой"
- [ ] Настроена Nav2-навигация

## Автор

4t

## Лицензия
