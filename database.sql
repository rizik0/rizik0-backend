create table players(
    username varchar(255) primary key,
    email varchar(255) not null,
    password_hash varchar(255) not null
);

create table games(
    id auto_increment primary key,
    player1 varchar(255) not null,
    player2 varchar(255) not null,
    player3 varchar(255) not null,
    winner varchar(255) not null,
    winner_goal varchar(255) not null,

    foreign key(player1) references players(username),
    foreign key(player2) references players(username),
    foreign key(player3) references players(username),
    foreign key(winner) references players(username)
);

