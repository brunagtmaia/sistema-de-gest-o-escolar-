
create table aluno (
	id int not null auto_increment,
    codigo_aluno int,
    nome_aluno varchar(100),
    endereco_aluno varchar(200),
    cidade_aluno varchar(50),
    primary key (id)
);

create table professor(
codigo_prof int not null auto_increment, 
nome_prof varchar(100) not null,
end_prof varchar(150) not null,
cidade_prof varchar(30) not null,
primary key(codigo_prof)
);

create table disciplina(
disc_codigo int not null auto_increment,
disc_nome varchar(100) not null,
curso_nome varchar(100) not null,
n_aulas int not null,
primary key (disc_codigo)
);

create table professor_disciplina ( 
disc_codigo int not null,
prof_numero int not null,  
ano int,
primary key (disc_codigo, prof_numero, ano),
foreign key (disc_codigo) references disciplina(disc_codigo),
foreign key (prof_numero) references professor(codigo_prof)
);

create table matricula( 
aluno_numero int not null,
disc_codigo int not null,
ano int not null,
primary key(aluno_numero, disc_codigo, ano),
FOREIGN KEY (aluno_numero) REFERENCES aluno(id),
foreign key (disc_codigo) references disciplina(disc_codigo)
);


select id from aluno;
select * from professor;
select * from disciplina;