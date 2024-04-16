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

insert into players(username, email, password_hash) values
('cristian', 'cristian@email.com', '$2b$12$DZUa.I0rNkS6e.dCp.OnmeDODDk8No.2rkhn2lWU0s0JME4Ah/I6O'),
('gieri', 'gieri@email.com', '$2b$12$jrFPXMFZIPP4n3/L/N4glOW3/asgMLEcGxKZyC8YGAcgViVTAZrpK'),
('pietro', 'pietro@email.com', '$2b$12$n/5L4rJbKXj.DAJjgMONGOktzePquyRt/4Zx8KXD1LqqubFHhAuGO'),
('amin', 'amin@email.com', '$2b$12$kH5p0.IBI3WdKPqvX9JHS.cpgocDrAoT0/2KIHsAel7pvWmjtNCY2'),
('leonardo', 'leonardo@email.com', '$2b$12$kuhB4WrX5FTv.VEJ8Fe1i.FFsdKsjZxxMrkh/e5QDNAAaxZC6NDh2'),
('gabbo', 'gabbo@gmail.com', '$2b$12$Ah9Ke.rHg9aVVFzgf95N9unvb1MeOGocxNwXA5RdJG4AnofXd2CJS'),
('cri', 'cri@email.com', '$2b$12$IZwCHhXPHv8hbvnTDweW3OQ47kdqXgAsA/6vtg2WB11t1jl4G3oyK'),
('giuseppe', 'giuseppe@gmail.com', '$2b$12$k0TSE3MXbM7pkvG.6abyHeRWkIso1C1bLwb94hI3zi6Hww2MtXn6C'),
('federico', 'federico@gmail.com', '$2b$12$qUL1apy4Lq/twRt9moyOguqFH4Q9kwxR3C8maDtH/dVD9s1uEGLu2'),
('alberto', 'alberto@email.com', '$2b$12$Ule.f77PYLI/94FyQ3qQpuRfTjDU.lh51HT9xXFJgWeoMrFmMmwqC'),
('edoardo', 'edoardo@email.com', '$2b$12$Gl.qe5ZMxOZ/ivbQbA6hV.oFISJDspvwxl8VF/TYfYfnfPq8gFyEm'),
('giorgio', 'giorgio@email.com', '$2b$12$E0ttNngct8J4H7MTWYQt0O1IrkX8BVBwsNI3Fyq9XRwOJ3tnwUZfm'),
('emanuel', 'emanuel@email.com', '$2b$12$29BPrtSyOOAzC8233myOQuoZcADPrmsRWlZfoUjawUDShJWqUx.Aq'),
('letizia', 'letizia@email.com', '$2b$12$u72K1qqZQByaONROckTx6.Drcbzz3YPHh5TPB27.jxsrmxwSaMwKu'),
('francesca', 'francesca@email.com', '$2b$12$Gc1MyerdoX8oEGFuG1njf.WfNKSavrqNEaVq9SwodVGpNYUM.kYiG'),
('ermenegildo', 'ermenegildo@email.com', '$2b$12$8mYWdTF2d04/YFtN0P8e6.oYpJ5rRvwyINJpSQB3cf3ZoKIG35fZa'),
('gianfranco', 'gianfranco@email.com', '$2b$12$jfvCNNd/d8SmjYqZmmNgA.YzYJ.iilo61geFegba.KCtaIYmcGcBq'),
('maria', 'maria@email.com', '$2b$12$0Ban.pNYZjzcB5Zhn7o/2.3htU.qSlr13qWx3pmhkKGlyD1/RAG/u'),
('mario', 'mario@email.com', '$2b$12$ntONnCr4tGTlwsK5PlB4l.VtJTCQQDLX8yz7g3kbLQ.xEWQGfdKna'),
('luigi', 'luigi@email.com', '$2b$12$NCfvMbIHaBVSEfecMPbxi.XQquLzEpwtCUiH6jSF6tOJzNxkNy8Ye');

