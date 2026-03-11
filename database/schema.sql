-- =============================================================
-- Sistema de Gestión de Clientes - Schema SQL
-- Base de datos: gestion_clientes
-- =============================================================

CREATE DATABASE IF NOT EXISTS gestion_clientes
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE gestion_clientes;

-- -------------------------------------------------------------
-- Tabla: usuarios
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    nombre        VARCHAR(100)                        NOT NULL,
    email         VARCHAR(100)                        NOT NULL UNIQUE,
    password_hash VARCHAR(255)                        NOT NULL,
    rol           ENUM('admin', 'empleado')           DEFAULT 'empleado',
    activo        BOOLEAN                             DEFAULT TRUE,
    created_at    TIMESTAMP                           DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP                           DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- Tabla: clientes
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clientes (
    id             INT AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(100)                             NOT NULL,
    apellido       VARCHAR(100)                             NOT NULL,
    email          VARCHAR(100)                             UNIQUE,
    telefono       VARCHAR(20),
    direccion      TEXT,
    ciudad         VARCHAR(100),
    tipo_cliente   ENUM('regular', 'premium', 'vip')       DEFAULT 'regular',
    notas          TEXT,
    activo         BOOLEAN                                  DEFAULT TRUE,
    created_at     TIMESTAMP                                DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMP                                DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    created_by     INT,
    CONSTRAINT fk_clientes_usuario FOREIGN KEY (created_by) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- Tabla: auditoria
-- -------------------------------------------------------------
CREATE TABLE IF NOT EXISTS auditoria (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id        INT,
    accion            VARCHAR(50)   NOT NULL,
    tabla_afectada    VARCHAR(50)   NOT NULL,
    registro_id       INT,
    datos_anteriores  JSON,
    datos_nuevos      JSON,
    ip_address        VARCHAR(45),
    created_at        TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_auditoria_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -------------------------------------------------------------
-- Datos iniciales: usuario admin
-- Email: admin@sistema.com  |  Password: admin123
-- -------------------------------------------------------------
INSERT INTO usuarios (nombre, email, password_hash, rol, activo)
VALUES (
    'Administrador',
    'admin@sistema.com',
    '$2b$12$LJ3m4ys3Lk0TSwMCCGq0QOCalBvMKiP0pNJFIEMLBfPBMmNEoMJiW',
    'admin',
    TRUE
);
