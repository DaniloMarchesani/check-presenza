create database checkPresenze;
use checkPresenze;
create table utenti(
	id integer auto_increment,
    nome varchar(30),
    cognome varchar(30),
    codice varchar(10) unique,
    presente bool default false,
    PRIMARY KEY (id)
);

create table presenze(
	id integer auto_increment,
    entrata timestamp,
    uscita timestamp,
    codice varchar(10),
    valido bool default false,
    PRIMARY KEY (id),
    FOREIGN KEY (codice) REFERENCES utenti(codice)
    
);