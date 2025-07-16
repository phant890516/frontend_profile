CREATE TABLE `user` (
    `userid` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `authority` INT(1) NOT NULL,
    PRIMARY KEY(`userid`)
);