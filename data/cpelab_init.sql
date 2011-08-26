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
CREATE INDEX nmapos_vendor_idx ON nmapos (n_vendor);
CREATE INDEX nmapos_produc_idx ON nmapos (n_product);

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
CREATE INDEX cpeos_name_idx ON cpeos (cpe_name);
CREATE INDEX cpeos_vendor_idx ON cpeos (cpe_vendor);
CREATE INDEX cpeos_product_idx ON cpeos (cpe_product);

