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
    giorno varchar(10),
    entrata timestamp,
    uscita timestamp,
    codice varchar(10),
    valido bool default true,
    PRIMARY KEY (id),
    FOREIGN KEY (codice) REFERENCES utenti(codice)
    
);

insert into utenti (nome, cognome, codice) values( "prova1", "prova1", "aaaaaa");
insert into utenti (nome, cognome, codice) values( "prova2", "prova2", "bbbbbb");
insert into utenti (nome, cognome, codice) values( "prova3", "prova3", "cccccc");