
CREATE DATABASE presupuesto;

USE presupuesto;

CREATE TABLE cdp (
    id INTEGER PRIMARY KEY  AUTO_INCREMENT,
    numero_documento INTEGER,
    fecha_registro DATETIME,
    fecha_creacion DATETIME,
    tipo_cdp VARCHAR(50),
    estado VARCHAR(50),
    dependencia VARCHAR(50),
    dependencia_descripcion VARCHAR(255),
    rubro VARCHAR(100),
    descripcion VARCHAR(500),
    fuente VARCHAR(100),
    recurso VARCHAR(100),
    sit VARCHAR(50),
    valor_inicial DECIMAL(18, 2),
    valor_operaciones DECIMAL(18, 2),
    valor_actual DECIMAL(18, 2),
    saldo_por_comprometer DECIMAL(18, 2),
    objeto VARCHAR(500),
    solicitud_cdp INTEGER
);


CREATE TABLE crp (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    numero_documento INTEGER,
    fecha_registro DATETIME,
    fecha_creacion DATETIME,
    estado VARCHAR(50),
    dependencia VARCHAR(50),
    dependencia_descripcion VARCHAR(255),
    rubro VARCHAR(100),
    descripcion VARCHAR(500),
    fuente VARCHAR(100),
    recurso VARCHAR(100),
    situacion VARCHAR(50),
    valor_inicial DECIMAL(18, 2),
    valor_operaciones DECIMAL(18, 2),
    valor_actual DECIMAL(18, 2),
    saldo_por_utilizar DECIMAL(18, 2),
    tipo_identificacion VARCHAR(50),
    identificacion VARCHAR(50),
    nombre_razon_social VARCHAR(255),
    medio_de_pago VARCHAR(100),
    tipo_cuenta VARCHAR(50),
    numero_cuenta VARCHAR(50),
    estado_cuenta VARCHAR(50),
    entidad_nit VARCHAR(20),
    entidad_descripcion VARCHAR(255),
    solicitud_cdp INTEGER,
    cdp INTEGER,
    compromisos TEXT,
    cuentas_por_pagar TEXT,
    obligaciones TEXT,
    ordenes_de_pago TEXT,
    reintegros TEXT,
    fecha_documento_soporte DATETIME,
    tipo_documento_soporte VARCHAR(100),
    numero_documento_soporte VARCHAR(100),
    observaciones TEXT
);


CREATE TABLE eje (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    dependecia_de_afectacion_de_gastos VARCHAR(255),
    tipo VARCHAR(5),
    cta VARCHAR(10),
    subc VARCHAR(10),
    objg VARCHAR(10),
    ord VARCHAR(10),
    sord VARCHAR(10),
    item VARCHAR(10),
    sitem VARCHAR(10),
    concepto VARCHAR(255),
    fuente VARCHAR(50),
    situacion VARCHAR(50),
    rec INTEGER,
    recurso VARCHAR(100),
    apropiacion_vigente_dep_gsto DECIMAL(18, 2),
    total_cdp_dep_gstos DECIMAL(18, 2),
    apropiacion_disponible_dep_gsto DECIMAL(18, 2),
    total_cdp_modificacion_dep_gstos DECIMAL(18, 2),
    total_compromiso_dep_gstos DECIMAL(18, 2),
    cdp_por_comprometer_dep_gstos DECIMAL(18, 2),
    total_obligaciones_dep_gstos DECIMAL(18, 2),
    compromiso_por_obligar_dep_gstos DECIMAL(18, 2),
    total_ordenes_pago_dep_gstos DECIMAL(18, 2),
    obligaciones_por_ordenar_dep_gstos DECIMAL(18, 2),
    pagos_dep_gstos DECIMAL(18, 2),
    ordenes_pago_por_pagar_dep_gstos DECIMAL(18, 2),
    total_reintegros_dep_gstos DECIMAL(18, 2)
);


