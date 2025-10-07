

-- Таблица: корпуса
CREATE TABLE buildings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,              -- название корпуса
    address TEXT                             -- адрес корпуса
);

-- Таблица: местоположения (помещения в корпусах)
CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    building_id INT REFERENCES buildings(id), -- ссылка на корпус
    room_number VARCHAR(50),                  -- номер помещения
    description TEXT                          -- описание
);

-- Таблица: отделы/кабинеты
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,              -- название отдела
    location_id INT REFERENCES locations(id) -- ссылка на местоположение
);

-- Таблица: сотрудники
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,         -- полное имя
    position VARCHAR(255),                   -- должность
    contact_info VARCHAR(255)                -- контактная информация
);

CREATE TABLE roles(
    id SERIAL PRIMARY KEY,
    name_role VARCHAR(50) DEFAULT 'user'         -- роль: 'admin', 'teacher', 'technician'
);

-- Таблица: пользователи (для авторизации)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE,               -- уникальный ID пользователя в Telegram
    employee_id INT REFERENCES employees(id), -- ссылка на сотрудника
    username VARCHAR(255) UNIQUE,            -- имя пользователя
    password_hash VARCHAR(255),              -- хэш пароля
    role INT REFERENCES roles(id),           -- ссылка на роль
    is_active BOOLEAN DEFAULT TRUE,          -- активен ли пользователь
    created_at TIMESTAMP DEFAULT NOW(),      -- дата создания
    last_login TIMESTAMP                     -- дата последнего входа
);

-- Таблица: типы устройств
CREATE TABLE device_types (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(100) UNIQUE NOT NULL   -- тип устройства
);

-- Таблица: статусы устройств
CREATE TABLE statuses (
    id SERIAL PRIMARY KEY,
    status_name VARCHAR(50) UNIQUE NOT NULL  -- статус устройства
);

-- Таблица: устройства
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),                        -- название/модель
    serial_number VARCHAR(255),               -- серийный номер
    inventory_number VARCHAR(255),            -- инвентарный номер
    purchase_date DATE,                       -- дата приобретения
    warranty_end DATE,                        -- гарантия до
    status_id INT REFERENCES statuses(id),    -- ссылка на статус
    department_id INT REFERENCES departments(id), -- ссылка на отдел
    employee_id INT REFERENCES employees(id), -- ответственное лицо
    device_type_id INT REFERENCES device_types(id), -- тип устройства
    ip_address INET                           -- IP-адрес (если есть)
);

-- Таблица: статусы тикетов
CREATE TABLE ticket_statuses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL          -- например: "открыт", "в работе", "закрыт"
);

-- Таблица: тикеты (заявки на ремонт/неисправность)
CREATE TABLE tickets (
    id SERIAL PRIMARY KEY,
    device_id INT REFERENCES devices(id),     -- устройство, по которому тикет
    user_id INT REFERENCES users(id),         -- пользователь, создавший тикет
    assigned_to INT REFERENCES users(id),     -- пользователь, которому назначен тикет (необязательно)
    title VARCHAR(255) NOT NULL,              -- заголовок тикета
    description TEXT,                         -- описание проблемы
    status_id INT REFERENCES ticket_statuses(id), -- статус тикета
    created_at TIMESTAMP DEFAULT NOW(),       -- дата создания
    updated_at TIMESTAMP DEFAULT NOW(),       -- дата обновления
    resolved_at TIMESTAMP                     -- дата закрытия тикета (если закрыт)
);

-- Таблица: журнал изменений
CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    device_id INT REFERENCES devices(id),     -- устройство
    user_id INT REFERENCES users(id),         -- кто совершил действие
    action VARCHAR(100),                      -- действие
    timestamp TIMESTAMP DEFAULT NOW(),        -- время
    description TEXT                          -- описание
);



