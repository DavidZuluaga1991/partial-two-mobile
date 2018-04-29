DROP TABLE IF EXISTS `propertary`;

CREATE TABLE `propertary` (
  `id_propertary` INT NOT NULL AUTO_INCREMENT,
  `id_identification` INT NULL,
  `last_name` VARCHAR(45) NULL,
  `firsh_name` VARCHAR(45) NULL,
  PRIMARY KEY (`id_propertary`));

DROP TABLE IF EXISTS `vehicle`;

CREATE TABLE `vehicle` (
  `id_vehicle` INT NOT NULL AUTO_INCREMENT,
  `id_license_plate` VARCHAR(7) NULL,
  `model` VARCHAR(10) NULL,
  `year` VARCHAR(5) NULL,
  `id_propertary` INT NULL,
  PRIMARY KEY (`id_vehicle`),
  INDEX `fk_vehicle_1_idx` (`id_propertary` ASC),
  CONSTRAINT `fk_vehicle_1`
    FOREIGN KEY (`id_propertary`)
    REFERENCES `propertary` (`id_propertary`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

DROP TABLE IF EXISTS `penalty`;

CREATE TABLE `penalty` (
  `idpenalty` INT NOT NULL AUTO_INCREMENT,
  `datepenalty` DATE NULL,
  `idvehicle` INT NULL,
  `descriptionpenalty` VARCHAR(45) NULL,
  `statepenalty` TINYINT(1) NULL,
  `idpropertary` INT NULL,
  PRIMARY KEY (`idpenalty`),
  INDEX `fk_penalty_1_idx` (`idpropertary` ASC),
  INDEX `fk_penalty_2_idx` (`idvehicle` ASC),
  CONSTRAINT `fk_penalty_1`
    FOREIGN KEY (`idpropertary`)
    REFERENCES `propertary` (`id_propertary`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_penalty_2`
    FOREIGN KEY (`idvehicle`)
    REFERENCES `vehicle` (`id_vehicle`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
