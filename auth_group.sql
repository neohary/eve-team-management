BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	"name"	varchar(150) NOT NULL UNIQUE
);
INSERT INTO "auth_group" VALUES (1,'后勤官');
INSERT INTO "auth_group" VALUES (2,'CEO');
INSERT INTO "auth_group" VALUES (3,'军团成员');
INSERT INTO "auth_group" VALUES (4,'人事');
INSERT INTO "auth_group" VALUES (5,'待验证');
INSERT INTO "auth_group" VALUES (6,'被拒绝');
INSERT INTO "auth_group" VALUES (7,'统计官');
INSERT INTO "auth_group" VALUES (8,'总监');
COMMIT;
