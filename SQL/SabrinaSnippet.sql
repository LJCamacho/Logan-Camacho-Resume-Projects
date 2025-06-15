CREATE TABLE ALBUM(
AlbumID  INT  NOT NULL  IDENTITY(1,1)  PRIMARY KEY, 
AlbumName  CHAR(50)  NOT NULL,
AlbumSales INT NOT NULL	);

CREATE TABLE TRACK(
TrackID  INT  NOT NULL  IDENTITY(1,1) PRIMARY KEY,
TrackName CHAR(100)  NOT NULL, 
TrackGenre CHAR(100) NOT NULL, 
Duration   INT  NOT NULL,
ReleaseDate DATE  NOT NULL,
AlbumID  INT  NOT NULL,
CONSTRAINT  AL_TRACK_FK  FOREIGN KEY(AlbumID)
REFERENCES ALBUM(AlbumID)
ON UPDATE CASCADE 
ON DELETE CASCADE  );

CREATE TABLE MEDIA (
MediaID 	INT  NOT NULL  IDENTITY(1,1)  PRIMARY KEY, 
TrackVideoClip  CHAR(3)  NOT NULL, 
VideoClipViews  INT  NOT NULL, 
SpotifyStreams  INT  NOT NULL, 
USAPeak INT  NOT NULL,    
TrackID  INT  NOT NULL, 
CONSTRAINT  TRACK_MEDIA_FK  FOREIGN KEY(TrackID)
REFERENCES Track(TrackID)
ON UPDATE CASCADE 
ON DELETE CASCADE);

INSERT INTO ALBUM VALUES ('Short n'' Sweet', 342500);
INSERT INTO ALBUM VALUES ('emails i can''t send',77500);
INSERT INTO ALBUM VALUES ('Singular: Act II', 30000);
INSERT INTO ALBUM VALUES ('Singular: Act I', 40000);
INSERT INTO ALBUM VALUES ('EVOLution', 45000);
INSERT INTO ALBUM VALUES ('Eyes Wide Open', 40000);

INSERT INTO TRACK VALUES 
('Espresso', 'Disco Pop', 175459, '2024-8-23', 1);
INSERT INTO TRACK VALUES
('Please Please Please', 'Country Pop', 186365, '2024-6-6', 1);
INSERT INTO TRACK VALUES
('Sharpest Tool', 'Folk Pop', 218284, '2024-8-23', 1);
INSERT INTO TRACK VALUES
('Bed Chem', 'Synth Pop', 171870, '2024-8-23',1);
INSERT INTO TRACK VALUES
('Lie To Girls', 'Alternative Pop', 202001,'2024-8-23',1);

INSERT INTO TRACK VALUES
('Feather', 'Dance Pop', 185553, '2023-3-17',2);
INSERT INTO TRACK VALUES
('because i liked a boy', 'Alternative Pop', 196458, '2022-7-15',2); 
INSERT INTO TRACK VALUES
('Nonsense', 'R&B', 163648, '2022-7-15',2);
INSERT INTO TRACK VALUES 
('bet u wanna', 'R&B', 191025, '2022-7-15',2);
INSERT INTO TRACK VALUES
('Bad for Business', 'Pop', 188338, '2022-7-15',2);

INSERT INTO TRACK VALUES
('In My Bed', 'Electropop', 189981, '2019-6-7',3);
INSERT INTO TRACK VALUES
('Exhale', 'R&B', 164709, '2019-5-3',3); 
INSERT INTO TRACK VALUES
('I''m Fakin', 'Dance Pop', 175310, '2019-7-12',3);
INSERT INTO TRACK VALUES
('Take You Back', 'Dance Pop', 169058, '2019-7-19',3);
INSERT INTO TRACK VALUES
('Pushing 20', 'Dance Pop', 166234, '2019-3-8',3);



INSERT INTO TRACK VALUES
('Almost Love', 'Dance Pop', 212360, '2018-6-6',4);
INSERT INTO TRACK VALUES
('Sue Me', 'Electropop', 179227, '2018-11-9', 4);
INSERT INTO TRACK VALUES
('prfct','R&B', 166533, '2018-9-11', 4);
INSERT INTO TRACK VALUES
('Paris', 'Electropop', 218080, '2018-10-25', 4);
INSERT INTO TRACK VALUES
('Bad Time', 'Electropop', 184533, '2018-11-2', 4);

INSERT INTO TRACK VALUES
('On Purpose', 'Dance Pop', 238133, '2016-7-29', 5);
INSERT INTO TRACK VALUES
('Thumbs', 'Electropop', 216467, '2016-10-7', 5);
INSERT INTO TRACK VALUES
('Run and Hide', 'R&B', 209640, '2016-9-20', 5);
INSERT INTO TRACK VALUES
('Shadows', 'Pop', 172427, '2016-10-14', 5);
INSERT INTO TRACK VALUES
('Mirage', 'Pop', 205480, '2016-10-14', 5);

INSERT INTO TRACK VALUES
('Eyes Wide Open', 'Folk Pop', 192720, '2015-4-7', 6);
INSERT INTO TRACK VALUES
('Can''t Blame a Girl for trying', 'Folk Pop', 169307, '2014-3-14', 6);
INSERT INTO TRACK VALUES
('We''ll Be The Stars', 'Folk Pop', 186880, '2015-1-13', 6);
INSERT INTO TRACK VALUES
('Darling I''m a Mess', 'Folk Pop', 179053, '2015-4-14', 6);
INSERT INTO TRACK VALUES
('White Flag', 'Folk Pop', 198387, '2015-4-8', 6);

INSERT INTO MEDIA VALUES
('Yes', 176789086, 1310500749,1, 1);
INSERT INTO MEDIA VALUES
('Yes', 110879296, 799883111, 1, 2);
INSERT INTO MEDIA VALUES
('No', 0, 55698940, 12, 3);
INSERT INTO MEDIA VALUES
('No', 0, 119052743, 7, 4);
INSERT INTO MEDIA VALUES
('No', 0, 36130923, 22,5);

INSERT INTO MEDIA VALUES
('Yes', 88115820, 660019090, 20, 6); 
INSERT INTO MEDIA VALUES
('Yes', 35261970, 248107315, 185, 7);
INSERT INTO MEDIA VALUES
('Yes', 96393517, 998937536, 15, 8); 
INSERT INTO MEDIA VALUES
('No', 0, 43527528, 0, 9);
INSERT INTO MEDIA VALUES
('No', 0, 33553631, 0, 10);

INSERT INTO MEDIA VALUES
('Yes', 13071264, 39012841, 0, 11);
INSERT INTO MEDIA VALUES
('Yes', 8327548, 54306954, 0, 12);
INSERT INTO MEDIA VALUESS
('No', 0, 24883036, 0, 13);
INSERT INTO MEDIA VALUES
('No', 0, 5693698, 0, 14);
INSERT INTO MEDIA VALUES
('No', 0, 18119777, 0, 15);

INSERT INTO MEDIA VALUES
('Yes', 49717933, 45559372, 0, 16);
INSERT INTO MEDIA VALUES 
('Yes',59598448, 246105336, 0, 17);
INSERT INTO MEDIA VALUES
('No',0 ,11245366, 0, 18);
INSERT INTO MEDIA VALUES
('Yes', 22572446, 52306733, 0, 19);
INSERT INTO MEDIA VALUES
('No', 0, 22572446, 0, 20);


/*Which songs (name of song) have a video clip(aka a music video)? -> Use join or subquery*/

SELECT T.TrackName
FROM TRACK AS T, MEDIA AS M
WHERE T.TrackID=M.TrackID AND M.TrackVideoClip='Yes';

/*Which songs reach a USA peak of 5 or less (making this the most streamed songs in the US)*/

SELECT T.TrackName, M.USAPeak
FROM TRACK AS T, MEDIA AS M
WHERE T.TrackID=M.TrackID AND M.USAPeak<=5 AND M.USAPeak != 0; 
/* USAPeak of 0 means it never made the charts*/

/*Which Album has the most sales? (Making it her most popular album)*/
SELECT AlbumName, AlbumSales
FROM ALBUM
WHERE AlbumSales=(SELECT MAX(AlbumSales) FROM ALBUM);

/*longest Song in miliseconds*/

SELECT TrackName, Duration
FROM TRACK
WHERE Duration=(SELECT MAX(Duration) FROM TRACK);

/*What's the name of the song that has a videoclip and the most views? -> Use join or subquery*/

SELECT T.TrackName, M.TrackVideoClip, M.VideoClipViews
FROM TRACK AS T, MEDIA AS M
WHERE T.TrackID=M.TrackID AND M.TrackVideoClip='Yes' AND M.VideoClipViews=(SELECT MAX(VideoClipViews) FROM MEDIA);


/*Count the number of tracks in each album 
SELECT A.AlbumName, COUNT(SELECT T
FROM TRACK AS T, MEDIA AS M
WHERE T.TrackID=M.TrackID AND M.TrackVideoClip='Yes' AND M.VideoClipViews=(SELECT MAX(VideoClipViews) FROM MEDIA);*/

/*Which songs belong to the “short n’ sweet” album has a genre of country pop?*/

SELECT TrackName, TrackGenre
FROM TRACK
WHERE AlbumID=1 AND TrackGenre='Country Pop';

