/*
 * CPELab db initialization script
 */


/* --- TABLES CREATION --- */
DROP TABLE IF EXISTS nmapos;
DROP TABLE IF EXISTS cpeos;

CREATE TABLE nmapos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  n_title VARCHAR(80) NOT NULL,
  n_vendor VARCHAR(30) DEFAULT NULL,
  n_product VARCHAR(30) DEFAULT NULL,
  n_version VARCHAR(20) DEFAULT NULL,
  n_devtype VARCHAR(20) DEFAULT NULL
);

CREATE TABLE cpeos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cpe_title VARCHAR(80) NOT NULL,
  cpe_name VARCHAR(80) UNIQUE NOT NULL,
  cpe_part CHAR NOT NULL,
  cpe_vendor VARCHAR(30) NOT NULL,
  cpe_product VARCHAR(30) NOT NULL,
  cpe_version VARCHAR(20) NOT NULL,
  cpe_update VARCHAR(10) DEFAULT NULL,
  cpe_edition VARCHAR(10) DEFAULT NULL,
  cpe_language VARCHAR(10) DEFAULT NULL,
  deprecated BOOLEAN DEFAULT FALSE,
  last_update DATE DEFAULT (date())
);

